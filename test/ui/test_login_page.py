import logging
import unittest
from logic.ui.login_page import LoginPage
from infra.config_provider import ConfigProvider
from infra.ui.browser_wrapper import BrowserWrapper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class TestLoginPage(unittest.TestCase):
    HOME_PAGE_URL = "https://app.asana.com/0/home/1207971857090891"

    def setUp(self):
        """
        Sets up the testing environment, opens the browser on the login page.
        Works automatically.
        """
        self.browser = BrowserWrapper()
        self.config = ConfigProvider.load_config_json()
        self.secret = ConfigProvider.load_secret_json()
        self.driver = self.browser.get_driver(self.config["base_url_app"])

    def tearDown(self):
        """
        Closes the browser after completing the test.
        Works automatically.
        """
        self.driver.quit()

    def test_correct_login_flow(self):
        """
        This function tests if after inserting a correct email and password
        the main page of the website appears.
        """
        logging.info("Test correct login flow - Test started")
        # Arrange
        login_page = LoginPage(self.driver)
        # Act
        login_page.login_flow(self.config["asana_email"], self.secret["asana_password"])
        WebDriverWait(self.driver, 10).until(ec.url_to_be(self.HOME_PAGE_URL))
        # Assert
        self.assertEqual(self.driver.current_url, self.HOME_PAGE_URL)
