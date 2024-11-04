from infra.ui.selenium_helpers import By, Keys, WebDriverWait, ec
from infra.config_provider import ConfigProvider
from logic.ui.base_page_app import BasePageApp


class GoalsPage(BasePageApp):
    ADD_GOAL_BUTTON = '//div[text() = "Add goal"]'
    NEW_GOAL_PANEL = '//div[contains(@class, "ModalPaneWithBuffer-pane")]'
    GOAL_TITLE_INPUT = '//input[@id = "create_goal_dialog_name_input"]'
    GOAL_TITLE_INPUT_VALUE = '//input[@value ='
    PRIVACY_DROPDOWN = '//div[contains(@class, "GoalPrivacyOptions") and contains(@id, "lui")]'
    PRIVACY_DROPDOWN_ELEMENTS = '//a[@data-testid = "static-menu-item-base"]'
    PRIVACY_DROPDOWN_VALUE = '//div[@class = "GoalPrivacyOptions-dropdownButtonLabel" and text() ='
    MEMBERS_INPUT_FIELD = '//input[contains(@class, "TokenizerInput-input")]'
    MEMBERS_INPUT_FIELD_VALUE = (f'//span[@class = "TypographyPresentation TypographyPresentation--overflowTruncate" '
                                 f'and text() =')
    SAVE_GOAL_BUTTON = '//div[text() = "Save goal"]'
    GOALS_LIST = '//div[@class = "SortableList-sortableItemContainer"]'
    GOAL_NAME_CONTAINER = '//span[contains(@class, "GoalCardWithProgressBar-name")'

    def __init__(self, driver):
        """
        Initialize the GoalsPageExpanded class with a WebDriver instance.

        :param driver: WebDriver instance used for interacting with the browser.
        """
        super().__init__(driver)
        self._privacy_dropdown = None
        self._config = ConfigProvider.load_config_json()

    def click_on_add_goal_button(self):
        """
        Clicks the 'Add goal' button to start the process of adding a new goal.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.ADD_GOAL_BUTTON))
        ).click()

    def is_new_goal_panel_displayed(self):
        """
        Checks if the new goal panel is displayed.

        :return: True if the new goal panel is displayed, False otherwise.
        """
        return WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, self.NEW_GOAL_PANEL))
        ).is_displayed()

    def fill_goal_title_input(self, goal_title):
        """
        Fills in the goal title input field with the specified title.

        :param goal_title: The title to set for the new goal.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, self.GOAL_TITLE_INPUT))
        ).send_keys(goal_title)

    def goal_title_value_is_visible(self, goal_title):
        """
        Checks if the specified goal title is visible in the input field.

        :param goal_title: The title of the goal to check.
        :return: True if the goal title is visible, False otherwise.
        """
        return WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.visibility_of_element_located((By.XPATH, f"{self.GOAL_TITLE_INPUT_VALUE}'{goal_title}']"))
        ).is_displayed()

    def click_on_privacy_dropdown(self):
        """
        Clicks the privacy dropdown to reveal the privacy options.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.PRIVACY_DROPDOWN))
        ).click()

    def select_privacy_dropdown_by_index(self, index):
        """
        Selects an option from the privacy dropdown by its index.

        :param index: The index of the option to select.
        """
        self.click_on_privacy_dropdown()
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_all_elements_located((By.XPATH, self.PRIVACY_DROPDOWN_ELEMENTS))
        )[index].click()

    def privacy_dropdown_value_is_displayed(self, value):
        """
        Checks if the selected privacy value is correct (Public or Private).

        :param value: 0 for Public, 1 for Private.
        :return: True if the privacy value is correct, False otherwise.
        """
        value = "Public" if value == 0 else "Private"

        return WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, f"{self.PRIVACY_DROPDOWN_VALUE}'{value}']"))
        ).is_displayed()

    def fill_members_input_field(self, member):
        """
        Fills in the members input field with the specified member name.

        :param member: The member name to add to the goal.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, self.MEMBERS_INPUT_FIELD))
        ).click()
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, self.MEMBERS_INPUT_FIELD))
        ).send_keys(member)
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, self.MEMBERS_INPUT_FIELD))
        ).send_keys(Keys.RETURN)

    def members_field_value_is_correct(self, member):
        """
        Checks if the specified member name is correctly displayed in the members field.

        :param member: The member name to check.
        :return: True if the member name is correct, False otherwise.
        """
        return WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, f"{self.MEMBERS_INPUT_FIELD_VALUE}'{member}']"))
        ).is_displayed()

    def click_on_save_goal_button(self):
        """
        Clicks the 'Save goal' button to save the new goal.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.SAVE_GOAL_BUTTON))
        ).click()

    def click_on_save_goal_non_clickable_button(self):
        """
        Attempts to click the 'Save goal' button even if it is not clickable.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, self.SAVE_GOAL_BUTTON))
        ).click()

    def create_goal_flow(self, goal_title, dropdown_options_index, member_name):
        """
        Executes the complete flow for creating a goal, including filling out the goal title,
        selecting privacy options, adding members, and saving the goal.

        :param goal_title: The title of the new goal.
        :param dropdown_options_index: The index of the privacy option to select.
        :param member_name: The name of the member to add to the goal.
        """
        self.click_on_add_goal_button()
        self.fill_goal_title_input(goal_title)
        self.select_privacy_dropdown_by_index(dropdown_options_index)
        self.fill_members_input_field(member_name)
        self.click_on_save_goal_button()
        self.go_back()

    def goal_is_displayed(self):
        """
        Checks if any goal is displayed on the Goals page.

        :return: True if a goal is displayed, False otherwise.
        """
        return WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_all_elements_located((By.XPATH, self.GOALS_LIST))
        )[0].is_displayed()

    def goal_is_not_displayed(self):
        """
        Checks if the goals element is not visible or not present on the Goals page.

        :return: True if the goals element is not visible, False if it is still visible.
        """
        # Wait until the element is either invisible or not present at all
        element_invisible = WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.invisibility_of_element_located((By.XPATH, self.GOALS_LIST))
        )
        return element_invisible  # Will return True if the element is not visible

    def is_goal_name(self, goal_name):
        """
        Checks if the goal name displayed on the page matches the provided goal name.

        :param goal_name: The name of the goal to check.
        :return: True if the goal name matches, False otherwise.
        """
        goal_name_element = WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH,
                                            f"{self.GOAL_NAME_CONTAINER} and text()='{goal_name}']"))
        )
        # return True if the goal name matches
        return goal_name_element.is_displayed()
