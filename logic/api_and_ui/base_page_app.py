from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from infra.ui.base_page import BasePage


class BasePageApp(BasePage):
    """
    This class extends the BasePage class and provides methods to interact with the project list
    in the application's UI.
    """
    PROJECT_LIST = '//div[contains(@class, "projects")]//div[contains(@class, "RightClickMenu")]//a'
    GOALS_BUTTON = '//span[text() = "Goals"]'
    CREATE_BUTTON = '//div[@aria-label = "Create"]'
    PROJECT_BUTTON_IN_CREATE = '//div[@class = "MenuItemA11y Omnibutton-menuItem Omnibutton-project"]'
    MESSAGE_BUTTON_IN_CREATE = '//span[text() = "Message"]'
    BLANK_PROJECT_BUTTON = '//div[@class = "DashedTile DashedTile--large FlowPickerTile-dashedTile"]'
    POP_UP_AFTER_PRESSING_CREATE = '//div[contains(@class, "LayerPositioner-layer")]'

    def __init__(self, driver):
        """
        Initializes the BasePageApp class.

        :param driver: The WebDriver instance used to interact with the web browser.
        """
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

    def project_is_displayed(self, project_name):
        """
        Checks if a project with the specified name is displayed in the project list.

        :param project_name: The name of the project to check.
        :return: True if the project is displayed, False otherwise.
        """
        projects = WebDriverWait(self._driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, self.PROJECT_LIST))
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
        projects = WebDriverWait(self._driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, self.PROJECT_LIST))
        )
        for project in projects:
            if project_name in project.get_attribute("aria-label"):
                return False
        return True

    def click_on_goals_button(self):
        WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.GOALS_BUTTON))
        ).click()
