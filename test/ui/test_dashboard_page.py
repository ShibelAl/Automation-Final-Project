import unittest
from infra.jira_bug_reporter import JiraBugReporter
from logic.ui.page_manager import PageManager
from logic.utils.enums import ChartLocationOptions


class TestDashboardPage(unittest.TestCase):

    def setUp(self):
        """
        Sets up the testing environment, completes the login process to enter to the main page,
        and creates a new blank project. Works automatically.
        """
        self.page_manager = PageManager()
        self.dashboard_page = self.page_manager.go_to_dashboard_page()

    def tearDown(self):
        """
        Closes the browser after completing the test.
        """
        self.page_manager.close_browser()

    @JiraBugReporter.report_bug(
        description="The drag-and-drop functionality for recommended charts on the dashboard page is not "
                    "operating as intended. When attempting to drag one chart and drop it onto another, "
                    "the two charts should switch places, but they do not.",
        priority="Medium",
        labels=["UI", "drag_and_drop", "Charts", "Dashboard"]
    )
    def test_recommended_charts_drag_and_drop_feature(self):
        """
        This function tests the drag and drop feature in the dashboard page for the "Recommended" charts.
        It uses "get_chart_location()" that returns the location of the chart in the page.
        """
        # Arrange
        self.dashboard_page.add_two_charts_flow()

        # Capture initial state
        initial_left_chart_location = self.dashboard_page.get_chart_location(ChartLocationOptions.LEFT.value)
        initial_right_chart_location = self.dashboard_page.get_chart_location(ChartLocationOptions.RIGHT.value)

        # Act
        self.dashboard_page.drag_left_chart_to_right()

        # Capture final state
        final_left_chart_location = self.dashboard_page.get_chart_location(ChartLocationOptions.LEFT.value)
        final_right_chart_location = self.dashboard_page.get_chart_location(ChartLocationOptions.RIGHT.value)

        # Assert
        self.assertDictEqual(final_left_chart_location, initial_right_chart_location,
                             "Left chart was not successfully moved to the right position.")
        self.assertDictEqual(final_right_chart_location, initial_left_chart_location,
                             "Right chart was not successfully moved to the left position.")

    def test_fill_date_filter_input_field_with_all_punctuations(self):
        """
        This test only works on 'Incomplete tasks by project' chart.
        Just for training purposes.
        """
        self.dashboard_page.click_on_incomplete_tasks_green_chart()
        failing_chars = self.dashboard_page.fill_date_filter_input_field_with_all_punctuations()

        # assert that no characters appear in the input field
        self.assertEqual(failing_chars, [],
                         f"The following characters should not appear in the input field: {failing_chars}")
