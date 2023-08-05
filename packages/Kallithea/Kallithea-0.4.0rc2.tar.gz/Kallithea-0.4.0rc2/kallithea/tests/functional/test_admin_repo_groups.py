from kallithea.model.db import Repository
from kallithea.model.meta import Session
from kallithea.model.repo_group import RepoGroupModel
from kallithea.tests.base import TestController, url
from kallithea.tests.fixture import Fixture


fixture = Fixture()


class TestRepoGroupsController(TestController):

    def test_case_insensitivity(self):
        self.log_user()
        group_name = u'newgroup'
        response = self.app.post(url('repos_groups'),
                                 fixture._get_repo_group_create_params(group_name=group_name,
                                                                 _authentication_token=self.authentication_token()))
        # try to create repo group with swapped case
        swapped_group_name = group_name.swapcase()
        response = self.app.post(url('repos_groups'),
                                 fixture._get_repo_group_create_params(group_name=swapped_group_name,
                                                                 _authentication_token=self.authentication_token()))
        response.mustcontain('already exists')

        RepoGroupModel().delete(group_name)
        Session().commit()
