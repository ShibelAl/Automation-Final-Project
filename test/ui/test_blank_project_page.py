import unittest
from infra.jira_bug_reporter import JiraBugReporter
from infra.utils import Utils
from logic.ui.page_manager import PageManager


class TestNewProjectPage(unittest.TestCase):

    def setUp(self):
        """
        Sets up the testing environment.
        """
        self.page_manager = PageManager()
        self.blank_project_page = self.page_manager.go_to_blank_project_page()

    def tearDown(self):
        """
        Closes the browser after completing the test.
        """
        self.page_manager.close_browser()

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
        # Act
        self.blank_project_page.fill_project_name_input()

        # Assert
        self.assertTrue(self.blank_project_page.project_name_is_displayed())

    @JiraBugReporter.report_bug(
        description="After typing a random project name in the blank project template, the header should display the "
                    "correct project name, but it displays incorrectly.",
        priority="Medium",
        labels=["UI", "Project"]
    )
    def test_blank_project_header_is_correct(self):
        """
        This function tests if the project header displays the correct name after typing a random name
        into the project name input field.
        """
        # Arrange
        random_name = Utils.generate_random_string()

        # Act
        self.blank_project_page.fill_project_name_input(random_name)

        # Assert
        self.assertEqual(self.blank_project_page.get_header_project_name_text(), random_name)
