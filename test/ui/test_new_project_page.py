import unittest
from infra.jira_bug_reporter import JiraBugReporter
from logic.ui.page_manager import PageManager


class TestNewProjectPage(unittest.TestCase):

    def setUp(self):
        """
        Sets up the testing environment.
        """
        self.page_manager = PageManager()
        self.new_project_page = self.page_manager.go_to_new_project_page()

    def tearDown(self):
        """
        Closes the browser after completing the test.
        """
        self.page_manager.close_browser()

    @JiraBugReporter.report_bug(
        description="The button that is supposed to take the user to the new blank project template doesn't work,"
                    "it is supposed to change the URL to the new page of blank project.",
        priority="Highest",
        labels=["UI", "Project", "Blank_Project"]
    )
    def test_blank_project_button(self):
        """
        Tests if the "blank project" button works when creating new project,
        asserting that the current url is the expected url after pressing the button.
        """
        # Act
        self.new_project_page.click_on_blank_project_button()

        # Assert
        self.assertEqual(self.page_manager.get_driver().current_url,
                         self.page_manager.get_config("new_blank_project_page_url"))
