import unittest
from infra.jira_bug_reporter import JiraBugReporter
from infra.api.api_wrapper import APIWrapper
from infra.utils import Utils
from logic.api.goals import Goals
from logic.utils.logic_utils import LogicUtils
from logic.ui.page_manager import PageManager


class TestGoalsPage(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment.

        Initializes the browser and WebDriver, loads the configuration and secrets,
        and navigates to the Goals page in the Asana app.
        Prepares the API client and Goals logic for interacting with the Asana API.
        """
        self.page_manager = PageManager()
        self.goals_page = self.page_manager.go_to_goals_page()
        self._api_request = APIWrapper()
        self._goals = Goals(self._api_request)
        self._goal_created = False  # A flag to track if a goal was created

    def tearDown(self):
        """
        Waits for new goals to exist before attempting to delete them.
        Deletes all goals in the workspace if existed, and then closes the webdriver.
        """
        # first we check if the test created any goals before attempting to delete it.
        if self._goal_created:
            # wait for goals to be present in the workspace before deletion
            LogicUtils.wait_for_goals_to_exist(self._goals, self.page_manager.get_config('my_workspace_gid'))
            self._goals.delete_all_goals(self.page_manager.get_config('my_workspace_gid'))

        self.page_manager.close_browser()

    @JiraBugReporter.report_bug(
        description="'Add goal' button doesn't work, pressing it doesn't display the 'Add company goal' panel.",
        priority="Highest",
        labels=["UI", "Goals"]
    )
    def test_click_on_add_goal_button(self):
        """
        Test the functionality of clicking the 'Add goal' button.

        This method ensures that clicking the 'Add goal' button displays the new goal panel.
        """
        # Act
        self.goals_page.click_on_add_goal_button()

        # Assert
        self.assertTrue(self.goals_page.is_new_goal_panel_displayed())

    @JiraBugReporter.report_bug(
        description="The input that inserted in the goal title form didn't appear on the screen.",
        priority="High",
        labels=["UI", "Goals"]
    )
    def test_fill_goal_title_input(self):
        """
        Test filling in the goal title input field.

        This method verifies that the goal title input field is correctly populated with a generated title.
        """
        # Arrange
        self.goals_page.click_on_add_goal_button()
        goal_title = Utils.generate_random_string()

        # Act
        self.goals_page.fill_goal_title_input(goal_title)

        # Assert
        self.assertTrue(self.goals_page.goal_title_value_is_visible(goal_title))

    @JiraBugReporter.report_bug(
        description="The expected privacy option doesn't appear in the privacy dropdown.",
        priority="High",
        labels=["UI", "Goals"]
    )
    def test_privacy_dropdown(self):
        """
        Test selecting an option from the privacy dropdown.

        This method ensures that a valid privacy option (Public or Private) is selected and displayed.
        """
        # Arrange
        self.goals_page.click_on_add_goal_button()
        dropdown_element_pick = LogicUtils.generate_random_binary()

        # Act
        self.goals_page.select_privacy_dropdown_by_index(dropdown_element_pick)

        # Assert
        self.assertTrue(self.goals_page.privacy_dropdown_value_is_displayed(dropdown_element_pick))

    @JiraBugReporter.report_bug(
        description="'Save goal' button clicked and changed the URL when it shouldn't do so, "
                    "because Goal title is empty.",
        priority="Medium",
        labels=["UI", "Goals"]
    )
    def test_save_goal_button_does_not_work_feature(self):
        """
        Test clicking the 'Save goal' button when it is not clickable.

        This method verifies that attempting to click the 'Save goal' button when it is not clickable
        does not change the current URL.
        """
        # Arrange
        self.goals_page.click_on_add_goal_button()

        # Act
        self.goals_page.click_on_save_goal_non_clickable_button()

        # Assert
        self.assertEqual(self.page_manager.get_driver().current_url, self.page_manager.get_config('goals_page_url'))

    @JiraBugReporter.report_bug(
        description="Test failed in the goal creation flow.",
        priority="High",
        labels=["UI", "Goals"]
    )
    def test_create_goal_flow(self):
        """
        Test the complete goal creation flow - the goal is assigned to the default workspace
        user, specified in the config file.

        This method verifies the entire process of creating a goal, including setting the title,
        selecting privacy options, adding members, and saving the goal.
        """
        # Arrange
        goal_title = Utils.generate_random_string()
        dropdown_element_pick = LogicUtils.generate_random_binary()
        member_name = self.page_manager.get_config('default_workspace_member')

        # Act
        self.goals_page.create_goal_flow(goal_title, dropdown_element_pick, member_name)
        self._goal_created = True

        # Assert
        self.assertTrue(self.goals_page.goal_is_displayed())
