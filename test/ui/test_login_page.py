import unittest
from infra.jira_bug_reporter import JiraBugReporter
from logic.ui.login_page import LoginPage
from infra.config_provider import ConfigProvider
from infra.ui.browser_wrapper import BrowserWrapper


class TestLoginPage(unittest.TestCase):

    def setUp(self):
        """
        Sets up the testing environment, opens the browser on the login page.
        Works automatically.
        """
        self._browser = BrowserWrapper()
        self._config = ConfigProvider.load_config_json()
        self._secret = ConfigProvider.load_secret_json()
        self._driver = self._browser.get_driver(self._config["base_url_app"], login=True)
        self._login_page = LoginPage(self._driver)

    def tearDown(self):
        """
        Closes the browser after completing the test.
        Works automatically.
        """
        self._browser.close_browser()

    @JiraBugReporter.report_bug(
        description="The login flow is not functioning correctly. After entering a correct email and password, "
                    "the main page of the website should be displayed, but it is not.",
        priority="Highest",
        labels=["Login", "Authentication", "UI"]
    )
    def test_correct_login_flow(self):
        """
        This function tests if after inserting a correct email and password
        the main page of the website appears.
        """
        # Act
        self._login_page.login_flow(self._config["asana_email"], self._secret["asana_password"])

        # Assert
        self.assertEqual(self._driver.current_url, self._config["base_url_app"])

    @JiraBugReporter.report_bug(
        description="When a wrong email is entered, the login page shouldn't show an option to enter the password, "
                    "this test didn't pass because after entering a wrong email, the password field is rendered.",
        priority="Highest",
        labels=["Login", "Authentication", "UI"]
    )
    def test_wrong_email_in_login(self):
        """
        This function tests if when inserting a wrong email, then
        the login page prevents entering the website, as it should.
        """
        # Act
        self._login_page.fill_email_input(self._config["wrong_email"])
        self._login_page.click_on_continue_button()

        # Assert
        self.assertFalse(self._login_page.password_input_field_is_displayed())

    @JiraBugReporter.report_bug(
        description="A correct email and a WRONG password are entered in the login process, but the website "
                    "redirected the user to the home page, even though the password is wrong.",
        priority="Highest",
        labels=["Login", "Authentication", "Critical", "UI"]
    )
    def test_wrong_password_in_login(self):
        """
        This function tests if when inserting a correct email and wrong password,
        then the login page prevents entering the website.
        """
        # Act
        self._login_page.login_flow(self._config["asana_email"], self._config["wrong_password"])

        # Assert
        self.assertNotEqual(self._driver.current_url, self._config["base_url_app"])
