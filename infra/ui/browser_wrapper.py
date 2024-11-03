from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import EdgeOptions
from selenium.webdriver import FirefoxOptions
from infra.config_provider import ConfigProvider
from selenium.common.exceptions import WebDriverException
from infra.logging_setup import logger


class BrowserWrapper:
    """
    Wrapper class for managing Selenium WebDriver instances based on browser type
    and login status. It supports Chrome, Edge, and Firefox browsers.

    :ivar _driver (webdriver): The Selenium WebDriver instance.
    :ivar _config (dict): Configuration data loaded from a JSON file via ConfigProvider.
    """
    def __init__(self):
        """
        Initializes the BrowserWrapper instance by loading browser configuration
        settings from a JSON file.
        """
        self._driver = None
        self._config = ConfigProvider().load_config_json()

    def get_driver(self, url, login=False):
        """
        Initializes and returns a WebDriver instance for the specified URL.

        :param url: The URL to open with the WebDriver.
        :param login: Indicates whether the WebDriver should be initialized without a logged-in session.
        If True, a fresh session is provided, which is useful for accessing login pages without any pre-existing
        session. If False, provides a pre-configured, logged-in session.
        :return: The initialized Selenium WebDriver instance.
        :raises WebDriverException: If there is an error in initializing the WebDriver.
        :raises AttributeError: If the specified browser is invalid.
        """
        try:
            if self._config["browser"] == "Chrome":
                if not login:
                    chrome_options = ChromeOptions()
                    chrome_options.add_argument(self._config["logged_in_google_chrome_path"])

                    self._driver = webdriver.Chrome(options=chrome_options)
                else:
                    self._driver = webdriver.Chrome()

            elif self._config["browser"] == "Edge":
                if not login:
                    edge_options = EdgeOptions()
                    edge_options.add_argument(self._config["logged_in_microsoft_edge_path"])

                    self._driver = webdriver.Edge(options=edge_options)
                else:
                    self._driver = webdriver.Edge()

            elif self._config["browser"] == "Firefox":
                if not login:
                    firefox_options = FirefoxOptions()
                    firefox_options.profile = self._config["logged_in_firefox_path"]

                    self._driver = webdriver.Firefox(options=firefox_options)
                else:
                    self._driver = webdriver.Firefox()

            # open the provided URL
            self._driver.get(url)
            self._driver.maximize_window()

            return self._driver

        except WebDriverException:
            logger.error("Could not load web driver")

        except AttributeError:
            logger.error("Web driver name is not valid")

    def close_browser(self):
        """
        Closes the active WebDriver session if it exists.
        """
        if self._driver:
            self._driver.quit()
            self._driver = None
        else:
            logger.warning("No active browser session to close.")
