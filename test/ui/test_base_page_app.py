import unittest
from infra.jira_handler import JiraHandler
from infra.jira_bug_reporter import JiraBugReporter
from infra.ui.browser_wrapper import BrowserWrapper
from infra.config_provider import ConfigProvider
from logic.ui.base_page_app import BasePageApp


class TestBasePageApp(unittest.TestCase):
    CREATE_PROJECT_PAGE_LINK = "https://app.asana.com/0/projects/new"

    def setUp(self):
        """
        Sets up the testing environment, opens the browser on the home page.
        """
        self.browser = BrowserWrapper()
        self.jira_handler = JiraHandler()
        self.config = ConfigProvider.load_config_json()
        self.secret = ConfigProvider.load_secret_json()
        self.driver = self.browser.get_driver(self.config["base_url_app"])
        self.base_page_app = BasePageApp(self.driver)

    def tearDown(self):
        """
        Closes the browser after completing the test.
        """
        self.browser.close_browser()

    @JiraBugReporter.report_bug(
        description="After pressing on 'Create' in the upper left side of the page, a small, white pop-up "
                    "should appear with options for creating a task/project etc, and it didn't appear.",
        priority="Highest",
        labels=["UI", "Create", "Blocker"]
    )
    def test_create_button(self):
        """
        Tests if the pop-up that contains the 5 options (task, project, portfolio...)
        appears when pressing the create button.
        """
        # Act
        self.base_page_app.click_on_create_button()

        # Assert
        self.assertTrue(self.base_page_app.pop_up_after_pressing_create_is_displayed())

    @JiraBugReporter.report_bug(
        description="After pressing on 'Create' in the upper left side of the page, and then 'Project', the new page "
                    "for creating a new project didn't appear in the screen.",
        priority="Highest",
        labels=["UI", "Project", "Blocker"]
    )
    def test_opening_new_project_window(self):
        """
        Tests if when pressing on create -> project, the page
        for creating a new project appears (according to the url)
        """
        # Act
        self.base_page_app.open_new_project()

        # Assert
        self.assertEqual(self.driver.current_url, self.CREATE_PROJECT_PAGE_LINK)
