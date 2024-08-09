import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from infra.ui.base_page import BasePage


class BasePageApp(BasePage):
    CREATE_BUTTON = '//div[@aria-label = "Create"]'
    PROJECT_BUTTON_IN_CREATE = '//div[@class = "MenuItemA11y Omnibutton-menuItem Omnibutton-project"]'
    MESSAGE_BUTTON_IN_CREATE = '//span[text() = "Message"]'
    BLANK_PROJECT_BUTTON = '//div[@class = "DashedTile DashedTile--large FlowPickerTile-dashedTile"]'
    POP_UP_AFTER_PRESSING_CREATE = '//div[contains(@class, "LayerPositioner-layer")]'

    def __init__(self, driver):
        super().__init__(driver)

    def click_on_create_button(self):
        """
        Clicks on Create button.
        """
        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.CREATE_BUTTON))
        ).click()

    def click_on_project_button_in_create(self):
        """
        Clicks on project button. This button appears after pressing
        on Create.
        """
        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.PROJECT_BUTTON_IN_CREATE))
        ).click()

    def click_on_message_button_in_create(self):
        """
        Click on message button. This button appears after pressing
        on Create.
        """
        WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.MESSAGE_BUTTON_IN_CREATE))
        ).click()

    def open_new_project(self):
        """
        Clicks on Create and then on project, this function opens a new project.
        """
        logging.info("Creating a new project, without specifying the project details")
        self.click_on_create_button()
        self.click_on_project_button_in_create()

    def pop_up_after_pressing_create_is_displayed(self):
        """
        This function checks if the pop-up that has 5 options (Task, Project, Portfolio...)
        appears after pressing on Create.
        :return: True, if the small pop-up appears after pressing on Create. False otherwise.
        """
        return WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.POP_UP_AFTER_PRESSING_CREATE))
        ).is_displayed()

    def blank_project_button_is_displayed(self):
        """
        This function checks if the "Blank project" button in displayed.
        This button should appear after pressing on Create -> Project.
        :return: True, if the "Blank project" button appears, False otherwise.
        """
        return WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.BLANK_PROJECT_BUTTON))
        ).is_displayed()
