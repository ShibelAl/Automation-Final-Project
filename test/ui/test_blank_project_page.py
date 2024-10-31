import unittest
from infra.jira_handler import JiraHandler
from infra.jira_bug_reporter import JiraBugReporter
from infra.ui.browser_wrapper import BrowserWrapper
from infra.config_provider import ConfigProvider
from logic.ui.base_page_app import BasePageApp
from logic.ui.new_project_page import NewProjectPage
from logic.ui.blank_project_page import BlankProjectPage


class TestNewProjectPage(unittest.TestCase):

    def setUp(self):
        """
        Sets up the testing environment, completes the login process to enter to the main page,
        and creates a new blank project.
        """
        self.browser = BrowserWrapper()
        self.jira_handler = JiraHandler()
        self.config = ConfigProvider.load_config_json()
        self.secret = ConfigProvider.load_secret_json()
        self.driver = self.browser.get_driver(self.config["base_url_app"])
        self.base_page_app = BasePageApp(self.driver)
        self.base_page_app.open_new_project()
        self.new_project_page = NewProjectPage(self.driver)
        self.new_project_page.click_on_blank_project_button()

    def tearDown(self):
        """
        Closes the browser after completing the test.
        """
        self.browser.close_browser()

    @JiraBugReporter.report_bug(
        description="After typing the name of the project in the blank project template, it should appear in the "
                    "template header, but it didn't appear.",
        priority="Medium",
        labels=["UI", "Project"]
    )
    def test_blank_project_header_text_appears(self):
        """
        This function tests if the project name appears in the project template header.
        """
        # Arrange
        blank_project_page = BlankProjectPage(self.driver)

        # Act
        blank_project_page.fill_project_name_input()

        # Assert
        self.assertTrue(blank_project_page.project_name_is_displayed())
