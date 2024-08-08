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

    def __init__(self, driver):
        """
        Initializes the BasePageApp class.

        :param driver: The WebDriver instance used to interact with the web browser.
        """
        super().__init__(driver)

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
