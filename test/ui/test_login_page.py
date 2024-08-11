import unittest
from selenium.common import TimeoutException
from infra.jira_handler import JiraHandler
from infra.test_failure_handler import TestFailureHandler
from logic.ui.login_page import LoginPage
from infra.config_provider import ConfigProvider
from infra.ui.browser_wrapper import BrowserWrapper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class TestLoginPage(unittest.TestCase):
    HOME_PAGE_URL = "https://app.asana.com/0/home/1207971857090891"
    WAIT_TIME = 20
    NEGATIVE_TEST_WAIT_TIME = 5

    def setUp(self):
        """
        Sets up the testing environment, opens the browser on the login page.
        Works automatically.
        """
        self.browser = BrowserWrapper()
        self.jira_handler = JiraHandler()
        self.config = ConfigProvider.load_config_json()
        self.secret = ConfigProvider.load_secret_json()
        self.driver = self.browser.get_driver(self.config["base_url_app"])

    def tearDown(self):
        """
        Closes the browser after completing the test.
        Works automatically.
        """
        self.driver.quit()

    @TestFailureHandler.handle_test_failure
    def test_correct_login_flow(self):
        """
        This function tests if after inserting a correct email and password
        the main page of the website appears.
        """
        # Arrange
        login_page = LoginPage(self.driver)

        # Act
        login_page.login_flow(self.config["asana_email"], self.secret["asana_password"])
        WebDriverWait(self.driver, self.WAIT_TIME).until(ec.url_to_be(self.HOME_PAGE_URL))

        # Assert
        self.assertEqual(self.driver.current_url, self.HOME_PAGE_URL)

    @TestFailureHandler.handle_test_failure
    def test_wrong_password_in_login(self):
        """
        This function tests if when inserting a correct email and wrong password,
        then the login page prevents entering the website, as it should.
        """
        # Arrange
        login_page = LoginPage(self.driver)

        # Act
        login_page.login_flow(self.config["asana_email"], self.config["wrong_password"])
        try:
            WebDriverWait(self.driver, self.NEGATIVE_TEST_WAIT_TIME).until(ec.url_to_be(self.HOME_PAGE_URL))
        except TimeoutException:

            # Assert
            self.assertNotEqual(self.driver.current_url, self.HOME_PAGE_URL)

    @TestFailureHandler.handle_test_failure
    def test_wrong_email_in_login(self):
        """
        This function tests if when inserting a wrong email, then
        the login page prevents entering the website, as it should.
        """
        # Arrange
        login_page = LoginPage(self.driver)

        # Act
        login_page.fill_email_input(self.config["wrong_email"])
        login_page.click_on_continue_button()
        try:
            WebDriverWait(self.driver, self.NEGATIVE_TEST_WAIT_TIME).until(ec.url_to_be(self.HOME_PAGE_URL))
        except TimeoutException:

            # Assert
            self.assertNotEqual(self.driver.current_url, self.HOME_PAGE_URL)
