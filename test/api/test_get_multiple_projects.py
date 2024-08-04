import unittest
from infra.api.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.api.get_multiple_projects import GetMultipleProjects


class TestContactAPI(unittest.TestCase):
    """
    A test case to retrieve multiple projects.
    """
    def setUp(self):
        """
        Sets up the test cases by initializing necessary components.
        """
        self._config = ConfigProvider.load_config_json()
        self._api_request = APIWrapper()
        self.projects = GetMultipleProjects(self._api_request)
        self.projects_response = self.projects.get_multiple_projects()

    def test_getting_multiple_projects(self):
        """
        Tests retrieving multiple projects from the API.

        :assert: Asserts that the response status code is 200.
        """
        # Act
        response_body = self.projects_response.json()
        # Assert
        print(response_body)
        self.assertEqual(self.projects_response.status_code, 200)
