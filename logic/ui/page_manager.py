from infra.config_provider import ConfigProvider
from infra.ui.browser_wrapper import BrowserWrapper
from logic.ui.base_page_app import BasePageApp
from logic.ui.sidebar import SideBar
from logic.ui.reporting_page import ReportingPage
from logic.ui.dashboard_page import DashboardPage


class PageManager:
    def __init__(self):
        self._browser = BrowserWrapper()
        self._config = ConfigProvider.load_config_json()
        self._driver = self._browser.get_driver(self._config["base_url_app"])

    def get_config(self, key):
        return self._config[f"{key}"]

    def get_driver(self):
        return self._driver

    def close_browser(self):
        self._browser.close_browser()

    def go_to_base_page_app(self):
        """
        Navigates to the home page - AKA base page app.

        :return: BasePageApp instance representing the home page.
        """
        return BasePageApp(self._driver)

    def go_to_dashboard_page(self):
        """
        Navigates directly to the dashboard page.

        :return: DashboardPage instance representing the dashboard page.
        """
        sidebar = SideBar(self._driver)
        sidebar.click_on_reporting_button()

        reporting_page = ReportingPage(self._driver)
        reporting_page.go_to_dashboard_page()

        return DashboardPage(self._driver)
