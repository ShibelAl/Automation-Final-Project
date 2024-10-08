import unittest
from infra.jira_handler import JiraHandler
from infra.test_failure_handler import TestFailureHandler
from logic.ui.login_page import LoginPage
from infra.config_provider import ConfigProvider
from infra.ui.browser_wrapper import BrowserWrapper
from logic.ui.base_page_app import BasePageApp
from logic.ui.new_project_page import NewProjectPage


class TestNewProjectPage(unittest.TestCase):
    BLANK_PAGE_URL = "https://app.asana.com/0/projects/new/blank"

    def setUp(self):
        """
        Sets up the testing environment, completes the login process to enter to the main page,
        and clicks on create -> project. Works automatically.
        """
        self.browser = BrowserWrapper()
        self.jira_handler = JiraHandler()
        self.config = ConfigProvider.load_config_json()
        self.secret = ConfigProvider.load_secret_json()
        self.driver = self.browser.get_driver(self.config["base_url_app"])
        self.login_page = LoginPage(self.driver)
        self.login_page.login_flow(self.config["asana_email"], self.secret["asana_password"])
        self.base_page_app = BasePageApp(self.driver)
        self.base_page_app.open_new_project()

    def tearDown(self):
        """
        Closes the browser after completing the test.
        Works automatically.
        """
        self.driver.quit()

    @TestFailureHandler.handle_test_failure
    def test_blank_project_button(self):
        """
        Tests if the "blank project" button works when creating new project,
        asserting that the current url is the expected url after pressing the button.
        """
        # Arrange
        new_project_page = NewProjectPage(self.driver)

        # Act
        new_project_page.click_on_blank_project_button()

        # Assert
        self.assertEqual(self.driver.current_url, self.BLANK_PAGE_URL)
