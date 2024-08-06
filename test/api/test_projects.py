import unittest
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.api.projects import Projects


class TestProjects(unittest.TestCase):
    """
    A test case to retrieve multiple projects.
    """
    def setUp(self):
        """
        Sets up the test cases by initializing necessary components.
        """
        self._config = ConfigProvider.load_config_json()
        self._api_request = APIWrapper()
        self.projects = Projects(self._api_request)

    def test_create_a_project(self):
        """
        Test creating a new project and verifying it is added to the list of existing projects.
        """
        # Arrange
        new_project_name = Utils.generate_random_string()

        # Act
        new_project = self.projects.create_a_project(new_project_name)
        existing_projects = self.projects.get_multiple_projects()

        # Assert
        self.assertEqual(new_project.status_code, 201)
        self.assertEqual(existing_projects.status_code, 200)
        self.assertIn(new_project_name, self.projects.projects_names(existing_projects.json()),
                      f"{new_project_name} not found in existing projects.")
