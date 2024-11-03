from infra.ui.selenium_helpers import By, TimeoutException, WebDriverWait, ec
from time import sleep
from infra.config_provider import ConfigProvider
from infra.ui.base_page import BasePage


class LoginPage(BasePage):
    GMAIL_INPUT = ('//input[@class = "TextInputBase SizedTextInput SizedTextInput--medium TextInput '
                   'TextInput--medium LoginEmailForm-emailInput"]')
    CONTINUE_BUTTON = '//div[text() = "Continue"]'
    PASSWORD_INPUT = '//input[@autocomplete = "current-password"]'
    LOGIN_BUTTON = '//div[text() = "Log in"]'

    def __init__(self, driver):
        super().__init__(driver)
        self._config = ConfigProvider.load_config_json()

    def fill_email_input(self, email):
        """
        Fills the email input in the login page with the received parameter "email".
        :param email: string / email expression that the tester inserts to put in the email input
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.GMAIL_INPUT))
        ).send_keys(email)

    def click_on_continue_button(self):
        """
        Clicks on the continue button when inserting the email in the login.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.CONTINUE_BUTTON))
        ).click()

    def fill_password_input(self, password):
        """
        Fills the password input with the parameter "password".
        :param password: a parameter that is represents the password in the login page.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.PASSWORD_INPUT))
        ).send_keys(password)

    def click_on_login_button(self):
        """
        Clicks on the login button after filling the password.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.LOGIN_BUTTON))
        ).click()

    def login_flow(self, email, password):
        """
        Does the login process completely.
        :param email: a string that represents an email.
        :param password: a string that represents the password for the email.
        """
        self.fill_email_input(email)
        self.click_on_continue_button()
        self.fill_password_input(password)
        self.click_on_login_button()
        sleep(self._config["ui_update_time"])

    def password_input_field_is_displayed(self):
        """
        Checks whether the password input form is currently displayed on the page.
        :return: True if the password input form is displayed, False otherwise.
        """
        try:
            result = WebDriverWait(self._driver, self._config["wait_time"]).until(
                ec.visibility_of_element_located((By.XPATH, self.PASSWORD_INPUT))
            ).is_displayed()
            return result
        except TimeoutException:
            return False
