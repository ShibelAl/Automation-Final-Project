import unittest
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from infra.jira_bug_reporter import JiraBugReporter
from logic.api.goals import Goals
from logic.ui.page_manager import PageManager
from logic.api.time_periods import TimePeriods
from logic.utils.logic_utils import LogicUtils


class TestGoals(unittest.TestCase):
    """
    Test class for validating the creation, deletion, and updating of goals within a project using Asana's UI and API.
    """
    def setUp(self):
        """
        Sets up the test environment before each test.

        Initializes the browser, loads configuration and secret data, and logs into the application.
        Also sets up the necessary API and UI components for testing goals.
        """
        self.page_manager = PageManager()
        self.goals_page = self.page_manager.go_to_goals_page()
        self._api_request = APIWrapper()
        self._goals = Goals(self._api_request)
        self._time_periods = TimePeriods(self._api_request)
        self.workspace_gid = self.page_manager.get_config("my_workspace_gid")
        self.goal_created = False

    def tearDown(self):
        """
        Deletes all goals in the workspace if existed, and then closes the webdriver.
        """
        if self.goal_created:
            # wait for goals to be present in the workspace before deletion
            LogicUtils.wait_for_goals_to_exist(self._goals, self.page_manager.get_config('my_workspace_gid'))
            self._goals.delete_all_goals(self.page_manager.get_config('my_workspace_gid'))

        self.page_manager.close_browser()

    @JiraBugReporter.report_bug()
    def test_create_a_goal(self):
        """
        Tests the creation of a new goal via the API and verifies its presence in the UI.

        Steps:
        1. Click on the "Goals" button in the UI.
        2. Generate a random goal name and select a random time period.
        3. Create the goal using the API.
        4. Verify that the new goal is displayed in the UI.
        """
        # Arrange
        new_goal_name = Utils.generate_random_string()
        time_period = self._time_periods.get_random_time_period(self.workspace_gid)

        # Act
        self._goals.create_a_goal(new_goal_name, self.workspace_gid, time_period)
        self.goal_created = True

        # Assert
        self.assertTrue(self.goals_page.goal_is_displayed())

    @JiraBugReporter.report_bug()
    def test_delete_a_goal(self):
        """
        Tests the creation and deletion of a goal via the API and verifies its absence in the UI.

        Steps:
        1. Generate a random goal name and select a random time period.
        2. Create the goal using the API.
        3. Delete the goal using the API.
        4. Verify that the goal is no longer displayed in the UI.
        """
        # Arrange
        new_goal_name = Utils.generate_random_string()
        time_period = self._time_periods.get_random_time_period(self.workspace_gid)
        new_goal = self._goals.create_a_goal(new_goal_name, self.workspace_gid, time_period)
        new_goal_gid = new_goal.data['data']['gid']

        # Act
        self._goals.delete_a_goal(int(new_goal_gid))

        # Assert
        self.assertTrue(self.goals_page.goal_is_not_displayed())

    @JiraBugReporter.report_bug()
    def test_update_goal_name(self):
        """
        Tests the creation and updating of a goal via the API and verifies the updated goal name in the UI.

        Steps:
        1. Generate an initial random goal name and select a random time period.
        2. Create the goal using the API.
        3. Update the goal name using the API.
        4. Verify that the goal name in the UI is updated to the new name.
        """
        # Arrange
        initial_goal_name = Utils.generate_random_string()
        time_period = self._time_periods.get_random_time_period(self.workspace_gid)
        initial_goal = self._goals.create_a_goal(initial_goal_name, self.workspace_gid, time_period)
        self.goal_created = True
        initial_goal_gid = initial_goal.data['data']['gid']
        new_goal_name = Utils.generate_random_string()

        # Act
        self._goals.update_a_goal(initial_goal_gid, new_goal_name, self.workspace_gid)

        # Assert
        self.assertTrue(self.goals_page.is_goal_name(new_goal_name))


if __name__ == '__main__':
    unittest.main()
