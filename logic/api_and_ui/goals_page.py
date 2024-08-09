from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from logic.api_and_ui.base_page_app import BasePageApp


class GoalsPage(BasePageApp):
    """
    Page object representing the Goals page in the application.
    """
    GOALS_XPATH = '//div[@class = "SortableList-sortableItemContainer"]'
    GOAL_NAME_CONTAINER = '//span[contains(@class, "GoalCardWithProgressBar-name")'
    WAIT_TIME = 20

    def __init__(self, driver):
        """
        Initializes the GoalsPage object.

        :param driver: The WebDriver instance to interact with the browser.
        """
        super().__init__(driver)

    def goal_is_displayed(self):
        """
        Checks if any goal is displayed on the Goals page.

        :return: True if a goal is displayed, False otherwise.
        """
        return WebDriverWait(self._driver, self.WAIT_TIME).until(
            EC.presence_of_all_elements_located((By.XPATH, self.GOALS_XPATH))
        )[0].is_displayed()

    def goal_is_not_displayed(self):
        """
        Checks if the goals element is not visible or not present on the Goals page.

        :return: True if the goals element is not visible, False if it is still visible.
        """
        try:
            # Wait until the element is either invisible or not present at all
            element_invisible = WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.invisibility_of_element_located((By.XPATH, self.GOALS_XPATH))
            )
            return element_invisible  # Will return True if the element is not visible
        except TimeoutException:
            # If the wait times out, that means the element is still visible
            return False

    def is_goal_name(self, goal_name):
        """
        Checks if the goal name displayed on the page matches the provided goal name.

        :param goal_name: The name of the goal to check.
        :return: True if the goal name matches, False otherwise.
        """
        try:
            goal_name_element = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                f"{self.GOAL_NAME_CONTAINER} and text()='{goal_name}']"))
            )
            # return True if the goal name matches
            return goal_name_element.is_displayed()

        except TimeoutException:
            return False

