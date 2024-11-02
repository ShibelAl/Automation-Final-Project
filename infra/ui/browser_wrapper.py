from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import EdgeOptions
from selenium.webdriver import FirefoxOptions
from infra.config_provider import ConfigProvider
from selenium.common.exceptions import WebDriverException
from infra.logging_setup import logger


class BrowserWrapper:

    def __init__(self):
        self._driver = None
        self.config = ConfigProvider().load_config_json()

    def get_driver(self, url):
        try:
            if self.config["browser"] == "Chrome":
                chrome_options = ChromeOptions()
                chrome_options.add_argument(self.config["logged_in_google_chrome_path"])

                self._driver = webdriver.Chrome(options=chrome_options)

            elif self.config["browser"] == "Edge":
                edge_options = EdgeOptions()
                edge_options.add_argument(self.config["logged_in_microsoft_edge_path"])

                self._driver = webdriver.Edge(options=edge_options)

            elif self.config["browser"] == "Firefox":
                firefox_options = FirefoxOptions()
                firefox_options.profile = self.config["logged_in_firefox_path"]

                self._driver = webdriver.Firefox(options=firefox_options)

            # open the provided URL
            self._driver.get(url)
            self._driver.maximize_window()
            return self._driver

        except WebDriverException:
            logger.error("Could not load web driver")

        except AttributeError:
            logger.error("Web driver name is not valid")

    def close_browser(self):
        if self._driver:
            self._driver.quit()
