from infra.config_provider import ConfigProvider
from infra.ui.browser_wrapper import BrowserWrapper
from logic.ui.base_page_app import BasePageApp
from logic.ui.sidebar import SideBar
from logic.ui.new_project_page import NewProjectPage
from logic.ui.blank_project_page import BlankProjectPage
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

    def go_to_blank_project_page(self):
        """
        Navigates to the blank project page.
        First, go to base page app, and open a new project, and then pick the blank project option.

        :return: BlankProjectPage instance representing the blank project page.
        """
        self.go_to_base_page_app().open_new_project()
        NewProjectPage(self._driver).click_on_blank_project_button()

        return BlankProjectPage(self._driver)

    def go_to_dashboard_page(self):
        """
        Navigates directly to the dashboard page.

        :return: DashboardPage instance representing the dashboard page.
        """
        SideBar(self._driver).click_on_reporting_button()
        ReportingPage(self._driver).go_to_dashboard_page()

        return DashboardPage(self._driver)
