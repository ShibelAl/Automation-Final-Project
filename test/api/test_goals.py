import unittest
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.api.goals import Goals
from logic.api.time_periods import TimePeriods


class TestGoals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Sets up the test cases by initializing necessary components.
        """
        cls._config = ConfigProvider.load_config_json()
        cls._api_request = APIWrapper()
        cls.goals = Goals(cls._api_request)
        cls.time_periods = TimePeriods(cls._api_request)

    @classmethod
    def tearDownClass(cls):
        """
        Cleans up the test environment by attempting to delete all goals
        in the workspace after all tests have been executed. Handles the
        case where no goals are present gracefully.
        """
        try:
            # Attempt to delete all goals in the workspace
            cls.goals.delete_all_goals(cls._config['my_workspace_gid'])

        except ValueError as e:
            # Print an error message if no goals are found
            if str(e) == "No goals found in the specified workspace.":
                print("No goals to delete in the workspace.")
            else:
                # Re-raise any unexpected exceptions
                raise

    def test_create_a_goal(self):
        """
        Tests the creation of a new goal and verifies that the goal is successfully created
        and is present in the list of existing goals.
        """
        # Arrange
        new_goal_name = Utils.generate_random_string()
        time_period = self.time_periods.get_random_time_period(self._config['my_workspace_gid'])

        # Act
        new_goal = self.goals.create_a_goal(new_goal_name, self._config['my_workspace_gid'], time_period)
        existing_goals = self.goals.get_goals(self._config['my_workspace_gid'])

        # Assert
        self.assertEqual(new_goal.status, 201)
        self.assertIn(new_goal_name, self.goals.goals_names(existing_goals.data),
                      f"{new_goal_name} not found in existing projects.")

    def test_delete_a_goal(self):
        """
        Tests the deletion of a goal and verifies that the goal is successfully deleted
        and is no longer present in the list of existing goals.
        """
        # Arrange
        new_goal_name = Utils.generate_random_string()
        time_period = self.time_periods.get_random_time_period(self._config['my_workspace_gid'])
        new_goal = self.goals.create_a_goal(new_goal_name, self._config['my_workspace_gid'], time_period)
        new_goal_gid = new_goal.data['data']['gid']

        # Act
        deleting_a_goal = self.goals.delete_a_goal(int(new_goal_gid))
        existing_projects = self.goals.get_goals(self._config['my_workspace_gid'])

        # Assert
        self.assertEqual(deleting_a_goal.status, 200)
        self.assertNotIn(new_goal_name, self.goals.goals_names(existing_projects.data),
                         f"{new_goal_name} found in existing projects after deletion.")

    def test_update_a_goal(self):
        """
        Tests the update of an existing goal's name and verifies that the name is successfully updated.
        """
        # Arrange
        initial_goal_name = Utils.generate_random_string()
        time_period = self.time_periods.get_random_time_period(self._config['my_workspace_gid'])
        initial_goal = self.goals.create_a_goal(initial_goal_name, self._config['my_workspace_gid'], time_period)
        initial_goal_gid = initial_goal.data['data']['gid']
        new_goal_name = Utils.generate_random_string()

        # Act
        updated_goal = self.goals.update_a_goal(initial_goal_gid, new_goal_name, self._config['my_workspace_gid'])

        # Assert
        self.assertEqual(updated_goal.status, 200)
        self.assertEqual(updated_goal.data['data']['name'], new_goal_name)
