import unittest
from infra.jira_handler import JiraHandler
from infra.test_failure_handler import TestFailureHandler
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.api.projects import Projects


class TestProjects(unittest.TestCase):
    def setUp(self):
        """
        Sets up the test cases by initializing necessary components.
        """
        self._config = ConfigProvider.load_config_json()
        self._api_request = APIWrapper()
        self.jira_handler = JiraHandler()
        self.projects = Projects(self._api_request)

    @TestFailureHandler.handle_test_failure
    def test_create_a_project(self):
        """
        Tests creating a new project and verifying it is added to the list of existing projects.

        The test performs the following steps:
        1. Generates a random project name.
        2. Creates a new project with the generated name.
        3. Retrieves the list of existing projects.
        4. Asserts that the new project was successfully created.
        5. Asserts that the new project is in the list of existing projects.
        """
        # Arrange
        new_project_name = Utils.generate_random_string()

        # Act
        new_project = self.projects.create_a_project(new_project_name)
        existing_projects = self.projects.get_multiple_projects()

        # Assert
        self.assertEqual(new_project.status, 201)
        self.assertIn(new_project_name, self.projects.projects_names(existing_projects.data),
                      f"{new_project_name} not found in existing projects.")

    @TestFailureHandler.handle_test_failure
    def test_delete_project(self):
        """
        Tests deleting a project and verifying it is removed from the list of existing projects.

        The test performs the following steps:
        1. Generates a random project name.
        2. Creates a new project with the generated name.
        3. Deletes the created project.
        4. Retrieves the list of existing projects.
        5. Asserts that the new project was successfully created.
        6. Asserts that the new project is not in the list of existing projects after deletion.
        """
        # Arrange
        new_project_name = Utils.generate_random_string()
        new_project = self.projects.create_a_project(new_project_name)
        new_project_gid = new_project.data["data"]["gid"]

        # Act
        deleting_a_project = self.projects.delete_a_project(int(new_project_gid))
        existing_projects = self.projects.get_multiple_projects()

        # Assert
        self.assertEqual(deleting_a_project.status, 200)
        self.assertNotIn(new_project_name, self.projects.projects_names(existing_projects.data),
                         f"{new_project_name} not found in existing projects.")
