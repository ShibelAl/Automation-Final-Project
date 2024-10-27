import unittest
from infra.jira_handler import JiraHandler
from infra.jira_bug_reporter import TestFailureHandler
from infra.ui.browser_wrapper import BrowserWrapper
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.api.goals import Goals
from logic.api_and_ui.goals_page import GoalsPage
from logic.api.time_periods import TimePeriods
from logic.api_and_ui.base_page_app import BasePageApp
from logic.ui.login_page import LoginPage


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
        self._browser = BrowserWrapper()
        self._config = ConfigProvider.load_config_json()
        self._secret = ConfigProvider.load_secret_json()
        self.jira_handler = JiraHandler()
        self._driver = self._browser.get_driver(self._config["base_url_app"])
        self._login_page = LoginPage(self._driver)
        self._login_page.login_flow(self._config["asana_email"], self._secret["asana_password"])
        self._base_page_app = BasePageApp(self._driver)
        self._goals_page = GoalsPage(self._driver)
        self._api_request = APIWrapper()
        self._goals = Goals(self._api_request)
        self._time_periods = TimePeriods(self._api_request)

    def tearDown(self):
        """
        Cleans up the test environment after each test.

        Attempts to delete all goals in the workspace. If no goals are found, an appropriate message is printed.
        Finally, quits the WebDriver.
        """
        try:
            # Attempt to delete all goals in the workspace
            self._goals.delete_all_goals(self._config['my_workspace_gid'])
        except ValueError as e:
            # Print an error message if no goals are found
            if str(e) == "No goals found in the specified workspace.":
                print("No goals to delete in the workspace.")
            else:
                # Raise any unexpected exceptions
                raise
        self._driver.quit()

    @TestFailureHandler.handle_test_failure
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
        self._base_page_app.click_on_goals_button()
        new_goal_name = Utils.generate_random_string()
        time_period = self._time_periods.get_random_time_period(self._config['my_workspace_gid'])

        # Act
        self._goals.create_a_goal(new_goal_name, self._config['my_workspace_gid'], time_period)

        # Assert
        self.assertTrue(self._goals_page.goal_is_displayed())

    @TestFailureHandler.handle_test_failure
    def test_delete_a_goal(self):
        """
        Tests the creation and deletion of a goal via the API and verifies its absence in the UI.

        Steps:
        1. Click on the "Goals" button in the UI.
        2. Generate a random goal name and select a random time period.
        3. Create the goal using the API.
        4. Delete the goal using the API.
        5. Verify that the goal is no longer displayed in the UI.
        """
        # Arrange
        self._base_page_app.click_on_goals_button()
        new_goal_name = Utils.generate_random_string()
        time_period = self._time_periods.get_random_time_period(self._config['my_workspace_gid'])
        new_goal = self._goals.create_a_goal(new_goal_name, self._config['my_workspace_gid'], time_period)
        new_goal_gid = new_goal.data['data']['gid']

        # Act
        self._goals.delete_a_goal(int(new_goal_gid))

        # Assert
        self.assertTrue(self._goals_page.goal_is_not_displayed())

    @TestFailureHandler.handle_test_failure
    def test_update_goal_name(self):
        """
        Tests the creation and updating of a goal via the API and verifies the updated goal name in the UI.

        Steps:
        1. Click on the "Goals" button in the UI.
        2. Generate an initial random goal name and select a random time period.
        3. Create the goal using the API.
        4. Update the goal name using the API.
        5. Verify that the goal name in the UI is updated to the new name.
        """
        # Arrange
        self._base_page_app.click_on_goals_button()
        initial_goal_name = Utils.generate_random_string()
        time_period = self._time_periods.get_random_time_period(self._config['my_workspace_gid'])
        initial_goal = self._goals.create_a_goal(initial_goal_name, self._config['my_workspace_gid'], time_period)
        initial_goal_gid = initial_goal.data['data']['gid']
        new_goal_name = Utils.generate_random_string()

        # Act
        self._goals.update_a_goal(initial_goal_gid, new_goal_name, self._config['my_workspace_gid'])

        # Assert
        self.assertTrue(self._goals_page.is_goal_name(new_goal_name))


if __name__ == '__main__':
    unittest.main()
