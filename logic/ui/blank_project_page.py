from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from infra.config_provider import ConfigProvider
from infra.ui.base_page import BasePage
from infra.utils import Utils


class BlankProjectPage(BasePage):
    PROJECT_NAME_FIELD = '//input[contains(@class, "ProjectNameInput")]'
    CREATE_PROJECT_BUTTON = '//div[text() = "Create project"]'
    PROJECT_NAME_HEADER = '//h5[contains(@class, "projectNameHeader")]'

    def __init__(self, driver):
        super().__init__(driver)
        self._project_name_field = None
        self._create_project_button = None
        self._project_name_header = None
        self._config = ConfigProvider.load_config_json()

    def fill_project_name_input(self, name=Utils.generate_random_string()):
        """
        Fills the project name input field. It fills the field with a random string as default,
        but if given a string in the name parameter then it will fill the input field with name.

        :param name: is a randomly generated string as default, represents the user input if given.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, self.PROJECT_NAME_FIELD))
        ).send_keys(name)

    def project_name_is_displayed(self):
        """
        Checks if the project name is displayed in the project template header,
        the project template appears right near the project name input field.

        :return: True, if the project name is displayed in the project template header, False otherwise.
        """
        project_name = WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.visibility_of_element_located((By.XPATH, self.PROJECT_NAME_HEADER)))
        return project_name.is_displayed()

    def get_header_project_name_text(self):
        """
        This function is used to check if the project name that the user inserts is
        showing in the project template as is, without changes.

        :return: The project name that is in the header of the project template.
        """
        return WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.visibility_of_element_located((By.XPATH, self.PROJECT_NAME_HEADER))
        ).text

    def click_on_create_project(self):
        """
        Clicks on "Create project" button. this button in clickable just after inserting
        the project name (or at least one character in the project name input).
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.CREATE_PROJECT_BUTTON))
        ).click()

    def create_project_flow(self, name=Utils.generate_random_string()):
        """
        This function fills the project name field, and then clicks on "Create project"
        """
        self.fill_project_name_input(name)
        self.click_on_create_project()
