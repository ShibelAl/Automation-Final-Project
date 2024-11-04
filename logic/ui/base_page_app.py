from infra.ui.selenium_helpers import By, TimeoutException, WebDriverWait, ec
from infra.config_provider import ConfigProvider
from infra.ui.base_page import BasePage


class BasePageApp(BasePage):
    CREATE_BUTTON = '//div[@aria-label = "Create"]'
    PROJECT_BUTTON_IN_CREATE = '//span[contains(@class, "LeftIconItemStructure-label") and text() = "Project"]'
    MESSAGE_BUTTON_IN_CREATE = '//span[text() = "Message"]'
    BLANK_PROJECT_BUTTON = '//div[@class = "DashedTile DashedTile--large FlowPickerTile-dashedTile"]'
    POP_UP_AFTER_PRESSING_CREATE = '//div[contains(@class, "LayerPositioner-layer")]'
    CLOSE_DRAFT_MESSAGE_BUTTON = '//div[contains(@class, "collapsed")]//div[@aria-label = "Close"]'
    DELETE_BUTTON_CLOSING_DRAFT = '//div[text() = "Delete message"]'
    PROJECT_LIST = '//div[contains(@class, "projects")]//div[contains(@class, "RightClickMenu")]//a'
    GOALS_BUTTON = '//span[text() = "Goals"]'

    def __init__(self, driver):
        super().__init__(driver)
        self._config = ConfigProvider.load_config_json()

    def click_on_create_button(self):
        """
        Clicks on Create button.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.CREATE_BUTTON))
        ).click()

    def click_on_project_button_in_create(self):
        """
        Clicks on project button. This button appears after pressing
        on Create.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.PROJECT_BUTTON_IN_CREATE))
        ).click()

    def click_on_message_button_in_create(self):
        """
        Click on message button. This button appears after pressing
        on Create.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.MESSAGE_BUTTON_IN_CREATE))
        ).click()

    def open_new_project(self):
        """
        Clicks on Create and then on project, this function opens a new project.
        """
        self.click_on_create_button()
        self.click_on_project_button_in_create()

    def pop_up_after_pressing_create_is_displayed(self):
        """
        This function checks if the pop-up that has 5 options (Task, Project, Portfolio...)
        appears after pressing on Create.
        :return: True, if the small pop-up appears after pressing on Create. False otherwise.
        """
        return WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.visibility_of_element_located((By.XPATH, self.POP_UP_AFTER_PRESSING_CREATE))
        ).is_displayed()

    def blank_project_button_is_displayed(self):
        """
        This function checks if the "Blank project" button in displayed.
        This button should appear after pressing on Create -> Project.
        :return: True, if the "Blank project" button appears, False otherwise.
        """
        return WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, self.BLANK_PROJECT_BUTTON))
        ).is_displayed()

    def close_draft_message(self):
        """
        Closes a draft message - if there was any - by clicking on the x sign.
        If there wasn't a draft message, a Timeout exception will appear, so the function will
        just pass, that means there is no draft message, carry on.
        """
        try:
            if WebDriverWait(self._driver, self._config["ui_update_time"]).until(
                ec.element_to_be_clickable((By.XPATH, self.CLOSE_DRAFT_MESSAGE_BUTTON))
            ).is_displayed():
                WebDriverWait(self._driver, self._config["ui_update_time"]).until(
                    ec.element_to_be_clickable((By.XPATH, self.CLOSE_DRAFT_MESSAGE_BUTTON))
                ).click()
            if WebDriverWait(self._driver, self._config["ui_update_time"]).until(
                    ec.element_to_be_clickable((By.XPATH, self.DELETE_BUTTON_CLOSING_DRAFT))
            ).is_displayed():
                WebDriverWait(self._driver, self._config["ui_update_time"]).until(
                    ec.element_to_be_clickable((By.XPATH, self.DELETE_BUTTON_CLOSING_DRAFT))
                ).click()
        except TimeoutException:
            pass

    def project_is_displayed(self, project_name):
        """
        Checks if a project with the specified name is displayed in the project list.
        :param project_name: The name of the project to check.
        :return: True if the project is displayed, False otherwise.
        """
        projects = WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_all_elements_located((By.XPATH, self.PROJECT_LIST))
        )
        for project in projects:
            if project_name in project.get_attribute("aria-label"):
                return True
        return False

    def project_is_not_displayed(self, project_name):
        """
        Checks if a project with the specified name is not displayed in the project list.

        :param project_name: The name of the project to check.
        :return: True if the project is not displayed, False otherwise.
        """
        try:
            WebDriverWait(self._driver, self._config["wait_time"]).until(
                lambda driver: all(
                    project_name not in project.get_attribute("aria-label")
                    for project in driver.find_elements(By.XPATH, self.PROJECT_LIST)
                )
            )
            return True
        except TimeoutException:
            return False

    def click_on_goals_button(self):
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.GOALS_BUTTON))
        ).click()

