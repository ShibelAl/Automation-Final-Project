import logging
import unittest
from infra.ui.browser_wrapper import BrowserWrapper
from infra.config_provider import ConfigProvider
from logic.ui.login_page import LoginPage
from logic.ui.base_page_app import BasePageApp


class TestBasePageApp(unittest.TestCase):
    FUNCTION_BUG = "Bug in the function"

    def setUp(self):
        """
        Sets up the testing environment, opens the browser on the login page,
        and completes the login process to enter to the main page.
        Works automatically.
        """
        logging.info("Base page app - Test Started")
        self.browser = BrowserWrapper()
        self.config = ConfigProvider.load_config_json()
        self.secret = ConfigProvider.load_secret_json()
        self.driver = self.browser.get_driver(self.config["base_url"])
        self.login_page = LoginPage(self.driver)
        self.login_page.login_flow(self.config["asana_email"], self.secret["asana_password"])

    def tearDown(self):
        """
        Closes the browser after completing the test.
        Works automatically.
        """
        self.driver.quit()

    def test_create_button(self):
        """
        Tests if the pop-up that contains the 5 options (task, project, portfolio...)
        appears when pressing the create button.
        """
        logging.info("Test create button - test started")
        # Arrange
        base_page_app = BasePageApp(self.driver)
        # Act
        base_page_app.click_on_create_button()
        try:
            # Assert
            self.assertTrue(base_page_app.pop_up_after_pressing_create_is_displayed())
        except AssertionError:
            raise AssertionError("assertion error")

    def test_opening_new_project_window(self):
        """
        Tests if when pressing on create -> project, the page
        for creating a new project appears (according to the url)
        """
        logging.info("Test opening new project window - test started")
        # Arrange
        base_page_app = BasePageApp(self.driver)
        # Act
        base_page_app.open_new_project()
        # Assert
        self.assertEqual(self.driver.current_url, "https://app.asana.com/0/projects/new")
