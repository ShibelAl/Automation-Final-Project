import unittest
from infra.jira_bug_reporter import JiraBugReporter
from logic.ui.page_manager import PageManager


class TestBasePageApp(unittest.TestCase):

    def setUp(self):
        """
        Sets up the testing environment, opens the browser on the home page.
        """
        self.page_manager = PageManager()
        self.base_page_app = self.page_manager.go_to_base_page_app()

    def tearDown(self):
        """
        Closes the browser after completing the test.
        """
        self.page_manager.close_browser()

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
        description="After pressing on 'Create' in the upper left side of the page, and then 'Project', "
                    "the new page for creating a new project didn't appear in the screen.",
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
        self.assertEqual(self.page_manager.get_driver().current_url,
                         self.page_manager.get_config("create_project_page_url"))
