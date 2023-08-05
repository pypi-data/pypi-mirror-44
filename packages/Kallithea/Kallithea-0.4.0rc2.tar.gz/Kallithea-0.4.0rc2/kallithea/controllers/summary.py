# -*- coding: utf-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
kallithea.controllers.summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Summary controller for Kallithea

This file was forked by the Kallithea project in July 2014.
Original author and date, and relevant copyright and licensing information is below:
:created_on: Apr 18, 2010
:author: marcink
:copyright: (c) 2013 RhodeCode GmbH, and others.
:license: GPLv3, see LICENSE.md for more details.
"""

import traceback
import calendar
import logging
import itertools
from time import mktime
from datetime import timedelta, date

from tg import tmpl_context as c, request
from tg.i18n import ugettext as _
from webob.exc import HTTPBadRequest

from beaker.cache import cache_region, region_invalidate

from kallithea.lib.vcs.exceptions import ChangesetError, EmptyRepositoryError, \
    NodeDoesNotExistError
from kallithea.config.conf import ALL_READMES, ALL_EXTS, LANGUAGES_EXTENSIONS_MAP
from kallithea.model.db import Statistics, CacheInvalidation, User
from kallithea.lib.utils2 import safe_int, safe_str
from kallithea.lib.auth import LoginRequired, HasRepoPermissionLevelDecorator
from kallithea.lib.base import BaseRepoController, render, jsonify
from kallithea.lib.vcs.backends.base import EmptyChangeset
from kallithea.lib.markup_renderer import MarkupRenderer
from kallithea.lib.celerylib.tasks import get_commits_stats
from kallithea.lib.compat import json
from kallithea.lib.vcs.nodes import FileNode
from kallithea.lib.page import RepoPage

log = logging.getLogger(__name__)

README_FILES = [''.join([x[0][0], x[1][0]]) for x in
                    sorted(list(itertools.product(ALL_READMES, ALL_EXTS)),
                           key=lambda y:y[0][1] + y[1][1])]


class SummaryController(BaseRepoController):

    def __get_readme_data(self, db_repo):
        repo_name = db_repo.repo_name
        log.debug('Looking for README file')

        @cache_region('long_term', '_get_readme_from_cache')
        def _get_readme_from_cache(key, kind):
            readme_data = None
            readme_file = None
            try:
                # gets the landing revision! or tip if fails
                cs = db_repo.get_landing_changeset()
                if isinstance(cs, EmptyChangeset):
                    raise EmptyRepositoryError()
                renderer = MarkupRenderer()
                for f in README_FILES:
                    try:
                        readme = cs.get_node(f)
                        if not isinstance(readme, FileNode):
                            continue
                        readme_file = f
                        log.debug('Found README file `%s` rendering...',
                                  readme_file)
                        readme_data = renderer.render(readme.content,
                                                      filename=f)
                        break
                    except NodeDoesNotExistError:
                        continue
            except ChangesetError:
                log.error(traceback.format_exc())
                pass
            except EmptyRepositoryError:
                pass

            return readme_data, readme_file

        kind = 'README'
        valid = CacheInvalidation.test_and_set_valid(repo_name, kind)
        if not valid:
            region_invalidate(_get_readme_from_cache, None, '_get_readme_from_cache', repo_name, kind)
        return _get_readme_from_cache(repo_name, kind)

    @LoginRequired(allow_default_user=True)
    @HasRepoPermissionLevelDecorator('read')
    def index(self, repo_name):
        p = safe_int(request.GET.get('page'), 1)
        size = safe_int(request.GET.get('size'), 10)
        collection = c.db_repo_scm_instance
        c.cs_pagination = RepoPage(collection, page=p, items_per_page=size)
        page_revisions = [x.raw_id for x in list(c.cs_pagination)]
        c.cs_comments = c.db_repo.get_comments(page_revisions)
        c.cs_statuses = c.db_repo.statuses(page_revisions)

        if request.authuser.is_default_user:
            username = ''
        else:
            username = safe_str(request.authuser.username)

        _def_clone_uri = _def_clone_uri_by_id = c.clone_uri_tmpl
        if '{repo}' in _def_clone_uri_by_id:
            _def_clone_uri_by_id = _def_clone_uri_by_id.replace('{repo}', '_{repoid}')
        elif '_{repoid}' in _def_clone_uri:
            _def_clone_uri = _def_clone_uri.replace('_{repoid}', '{repo}')
        else:
            log.error("Configured clone_uri_tmpl %r has no '{repo}' or '_{repoid}' and cannot toggle to use repo id URLs", c.clone_uri_tmpl)

        c.clone_repo_url = c.db_repo.clone_url(user=username,
                                                uri_tmpl=_def_clone_uri)
        c.clone_repo_url_id = c.db_repo.clone_url(user=username,
                                                uri_tmpl=_def_clone_uri_by_id)

        if c.db_repo.enable_statistics:
            c.show_stats = True
        else:
            c.show_stats = False

        stats = Statistics.query() \
            .filter(Statistics.repository == c.db_repo) \
            .scalar()

        c.stats_percentage = 0

        if stats and stats.languages:
            c.no_data = False is c.db_repo.enable_statistics
            lang_stats_d = json.loads(stats.languages)

            lang_stats = ((x, {"count": y,
                               "desc": LANGUAGES_EXTENSIONS_MAP.get(x)})
                          for x, y in lang_stats_d.items())

            c.trending_languages = (
                sorted(lang_stats, reverse=True, key=lambda k: k[1])[:10]
            )
        else:
            c.no_data = True
            c.trending_languages = []

        c.enable_downloads = c.db_repo.enable_downloads
        c.readme_data, c.readme_file = \
            self.__get_readme_data(c.db_repo)
        return render('summary/summary.html')

    @LoginRequired()
    @HasRepoPermissionLevelDecorator('read')
    @jsonify
    def repo_size(self, repo_name):
        if request.is_xhr:
            return c.db_repo._repo_size()
        else:
            raise HTTPBadRequest()

    @LoginRequired(allow_default_user=True)
    @HasRepoPermissionLevelDecorator('read')
    def statistics(self, repo_name):
        if c.db_repo.enable_statistics:
            c.show_stats = True
            c.no_data_msg = _('No data ready yet')
        else:
            c.show_stats = False
            c.no_data_msg = _('Statistics are disabled for this repository')

        td = date.today() + timedelta(days=1)
        td_1m = td - timedelta(days=calendar.mdays[td.month])
        td_1y = td - timedelta(days=365)

        ts_min_m = mktime(td_1m.timetuple())
        ts_min_y = mktime(td_1y.timetuple())
        ts_max_y = mktime(td.timetuple())
        c.ts_min = ts_min_m
        c.ts_max = ts_max_y

        stats = Statistics.query() \
            .filter(Statistics.repository == c.db_repo) \
            .scalar()
        c.stats_percentage = 0
        if stats and stats.languages:
            c.no_data = False is c.db_repo.enable_statistics
            lang_stats_d = json.loads(stats.languages)
            c.commit_data = json.loads(stats.commit_activity)
            c.overview_data = json.loads(stats.commit_activity_combined)

            lang_stats = ((x, {"count": y,
                               "desc": LANGUAGES_EXTENSIONS_MAP.get(x)})
                          for x, y in lang_stats_d.items())

            c.trending_languages = (
                sorted(lang_stats, reverse=True, key=lambda k: k[1])[:10]
            )
            last_rev = stats.stat_on_revision + 1
            c.repo_last_rev = c.db_repo_scm_instance.count() \
                if c.db_repo_scm_instance.revisions else 0
            if last_rev == 0 or c.repo_last_rev == 0:
                pass
            else:
                c.stats_percentage = '%.2f' % ((float((last_rev)) /
                                                c.repo_last_rev) * 100)
        else:
            c.commit_data = {}
            c.overview_data = ([[ts_min_y, 0], [ts_max_y, 10]])
            c.trending_languages = {}
            c.no_data = True

        recurse_limit = 500  # don't recurse more than 500 times when parsing
        get_commits_stats(c.db_repo.repo_name, ts_min_y, ts_max_y, recurse_limit)
        return render('summary/statistics.html')
