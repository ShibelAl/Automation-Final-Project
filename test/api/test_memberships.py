import unittest
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.api.projects import Projects
from logic.api.workspaces import Workspaces
from logic.api.memberships import Memberships


class TestMemberships(unittest.TestCase):
    def setUp(self):
        """
        Sets up the test cases by initializing necessary components.
        """
        self._config = ConfigProvider.load_config_json()
        self._api_request = APIWrapper()
        self.projects = Projects(self._api_request)
        self.workspaces = Workspaces(self._api_request)
        self.memberships = Memberships(self._api_request)

    def test_create_a_membership(self):
        """
        Tests the creation of a membership by performing the following steps:
        1. Creates a new project.
        2. Adds a new user to the workspace.
        3. Adds the user to the project as a member.
        4. Verifies that the project and membership creation were successful.
        5. Checks that the membership exists by comparing IDs.
        """
        # Arrange
        new_project_name = Utils.generate_random_string()
        new_project = self.projects.create_a_project(new_project_name)

        new_user_name = f"{Utils.generate_random_string()}@gmail.com"
        new_user = self.workspaces.add_a_user_to_workspace(new_user_name)

        new_project_gid = new_project.data['data']['gid']
        new_user_gid = new_user.data['data']['gid']

        # Act
        new_membership = self.memberships.add_a_membership(new_project_gid, new_user_gid)
        current_project_memberships = self.memberships.get_a_membership(int(new_membership.data['data']['gid']))

        # Assert
        self.assertEqual(new_membership.status, 201)
        self.assertEqual(new_membership.data['data']['gid'], current_project_memberships.data['data']['gid'])
