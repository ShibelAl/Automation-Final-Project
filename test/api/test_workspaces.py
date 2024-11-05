import unittest
from infra.jira_bug_reporter import JiraBugReporter
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.api.workspaces import Workspaces
from logic.api.projects import Projects
from logic.api.users import Users


class TestWorkspaces(unittest.TestCase):
    GMAIL = "@gmail.com"

    def setUp(self):
        """
        Sets up the test cases by initializing necessary components.
        """
        self._config = ConfigProvider.load_config_json()
        self._api_request = APIWrapper()
        self.workspaces = Workspaces(self._api_request)
        self.projects = Projects(self._api_request)
        self.users = Users(self._api_request)

    @JiraBugReporter.report_bug(
        description="Adding a user to the workspace fails or doesn't return the correct status code.",
        priority="High",
        labels=["API", "User", "Workspace", "Addition"]
    )
    def test_add_user_to_workspace(self):
        """
        Tests adding a new user to the workspace and verifying the user is added successfully.

        The test performs the following steps:
        1. Generates a random user email.
        2. Adds the new user to the workspace.
        3. Retrieves the list of users in the workspace.
        4. Extracts the new user's global ID.
        5. Extracts the list of user global IDs from the workspace.
        6. Asserts that the new user was successfully added.
        7. Asserts that the new user's global ID is in the list of user global IDs in the workspace.
        """
        # Arrange
        new_user_name = f"{Utils.generate_random_string()}{self.GMAIL}"

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

    @JiraBugReporter.report_bug(
        description="Updating the workspace name fails or doesn't reflect the change in retrieved workspace details.",
        priority="High",
        labels=["API", "Workspace", "Update"]
    )
    def test_update_workspace_name(self):
        """
        Tests updating the name of a workspace and verifying the update is successful.

        The test performs the following steps:
        1. Generates a random workspace name.
        2. Updates the workspace with the new name.
        3. Retrieves the updated workspace details.
        4. Asserts that the workspace name update was successful.
        5. Asserts that the retrieved workspace details match the updated name.
        """
        # Arrange
        new_workspace_name = Utils.generate_random_string()

        # Act
        updated_workspace = self.workspaces.update_a_workspace_name(new_workspace_name)
        workspace_gid = updated_workspace.data["data"]["gid"]
        workspace_details_after_updating = self.workspaces.get_workspace(workspace_gid)

        # Assert
        self.assertEqual(updated_workspace.status, 200)
        self.assertEqual(workspace_details_after_updating.data["data"]["name"], new_workspace_name)
