import unittest
from infra.jira_bug_reporter import JiraBugReporter
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.api.projects import Projects


class TestProjects(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Sets up the test cases by initializing necessary components.
        """
        cls._config = ConfigProvider.load_config_json()
        cls._api_request = APIWrapper()
        cls._projects = Projects(cls._api_request)

    @classmethod
    def tearDownClass(cls):
        """
        Cleans up the test environment by deleting the most recently created project.
        Fetches all projects in the workspace and deletes the first one in the list.
        """
        try:
            # Fetch all projects
            existing_projects = cls._projects.get_multiple_projects()
            if not existing_projects.data['data']:
                print("tearDownClass - No projects found to delete.")
                return

            # Assume the first project is the one created in the test (if only one project was created)
            first_project_gid = existing_projects.data['data'][0]['gid']

            # Attempt to delete the first project
            deleting_a_project = cls._projects.delete_a_project(first_project_gid)
            if deleting_a_project.status == 200:
                print(f"tearDownClass - Successfully deleted project with gid: {first_project_gid}")
            else:
                print(f"tearDownClass - Failed to delete project. Status: {deleting_a_project.status}")

        except Exception as e:
            print(f"tearDownClass - Exception occurred while deleting project: {e}")

    @JiraBugReporter.report_bug(
        description="Creating a project does not add it to the list of existing projects.",
        priority="Highest",
        labels=["API", "Project", "Creation"]
    )
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
        new_project = self._projects.create_a_project(new_project_name)
        existing_projects = self._projects.get_multiple_projects()

        # Assert
        self.assertEqual(new_project.status, 201)
        self.assertIn(new_project_name, self._projects.projects_names(existing_projects.data),
                      f"{new_project_name} not found in existing projects.")

    @JiraBugReporter.report_bug(
        description="Deleting a project does not remove it from the list of existing projects "
                    "or fails to delete it entirely.",
        priority="Highest",
        labels=["API", "Project", "Deletion"]
    )
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
        new_project = self._projects.create_a_project(new_project_name)
        new_project_gid = new_project.data["data"]["gid"]

        # Act
        deleting_a_project = self._projects.delete_a_project(int(new_project_gid))
        existing_projects = self._projects.get_multiple_projects()

        # Assert
        self.assertEqual(deleting_a_project.status, 200)
        self.assertNotIn(new_project_name, self._projects.projects_names(existing_projects.data),
                         f"{new_project_name} not found in existing projects.")
