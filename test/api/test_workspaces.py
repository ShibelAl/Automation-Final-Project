import unittest
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.api.workspaces import Workspaces
from logic.api.projects import Projects
from logic.api.users import Users


class TestWorkspaces(unittest.TestCase):
    """
    A test case to retrieve multiple projects.
    """
    def setUp(self):
        """
        Sets up the test cases by initializing necessary components.
        """
        self._config = ConfigProvider.load_config_json()
        self._api_request = APIWrapper()
        self.workspaces = Workspaces(self._api_request)
        self.projects = Projects(self._api_request)
        self.users = Users(self._api_request)

    def test_add_user_to_workspace(self):
        # Arrange
        new_user_name = f"{Utils.generate_random_string()}@gmail.com"

        # Act
        new_user = self.workspaces.add_a_user_to_workspace(new_user_name)
        workspace_users = self.users.get_workspace_users().data

        # Extract the new user's gid
        new_user_gid = new_user.data["data"]["gid"]
        # Extract the list of user gids from the workspace_users
        workspace_user_gids = self.users.users_gids_in_workspace(workspace_users)

        # Assert
        self.assertEqual(new_user.status, 200)
        self.assertIn(new_user_gid, workspace_user_gids)

    def test_update_workspace_name(self):
        # Arrange
        new_workspace_name = Utils.generate_random_string()

        # Act
        updated_workspace = self.workspaces.update_a_workspace_name(new_workspace_name)
        workspace_gid = updated_workspace.data["data"]["gid"]
        workspace_details_after_updating = self.workspaces.get_workspace(workspace_gid)

        # Assert
        self.assertEqual(updated_workspace.status, 200)
        self.assertEqual(workspace_details_after_updating.status, 200)
        self.assertEqual(workspace_details_after_updating.data["data"]["name"], new_workspace_name)
