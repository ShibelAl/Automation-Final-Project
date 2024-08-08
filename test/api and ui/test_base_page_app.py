import unittest

from infra.ui.browser_wrapper import BrowserWrapper
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.api.projects import Projects
from logic.api_and_ui.base_page_app import BasePageApp
from logic.ui.login_page import LoginPage


class TestProjects(unittest.TestCase):
    """
    This class contains test cases for creating and deleting projects,
    and verifying their presence in the UI.
    """

    def setUp(self):
        """
        Sets up the test cases by initializing necessary components.
        """
        self.browser = BrowserWrapper()
        self.config = ConfigProvider.load_config_json()
        self.secret = ConfigProvider.load_secret_json()
        self.driver = self.browser.get_driver(self.config["base_url_app"])
        self.login_page = LoginPage(self.driver)
        self.login_page.login_flow(self.config["asana_email"], self.secret["asana_password"])
        self.base_page_app = BasePageApp(self.driver)
        self._api_request = APIWrapper()
        self.projects = Projects(self._api_request)

    def tearDown(self):
        """
        Tear down the test cases by quitting the WebDriver.
        """
        self.driver.quit()

    def test_create_a_project(self):
        """
        Tests creating a new project and verifying it is added to the list of existing projects.
        """
        # Arrange
        new_project_name = Utils.generate_random_string()

        # Act
        new_project = self.projects.create_a_project(new_project_name)

        # Assert
        self.assertEqual(new_project.status, 201)
        self.assertTrue(self.base_page_app.project_is_displayed(new_project_name),
                        f"The project '{new_project_name}' was not found in the project list.")

    def test_create_and_delete_a_project(self):
        """
        Tests creating and deleting a project and verifying it is removed from the list of existing projects.
        """
        # Arrange
        new_project_name = Utils.generate_random_string()

        # Act
        new_project = self.projects.create_a_project(new_project_name)

        # Delete the project
        new_project_gid = new_project.data["data"]["gid"]
        deleted_project = self.projects.delete_a_project(new_project_gid)

        # Assert
        self.assertEqual(deleted_project.status, 200)
        self.assertTrue(self.base_page_app.project_is_not_displayed(new_project_name),
                        f"The project '{new_project_name}' was found in the project list after deletion.")


if __name__ == '__main__':
    unittest.main()
