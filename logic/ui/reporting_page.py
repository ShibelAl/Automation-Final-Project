from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from infra.config_provider import ConfigProvider
from infra.ui.base_page import BasePage


class ReportingPage(BasePage):
    CREATE_BUTTON = '//div[@class = "DomainDashboardIndexToolbar"]//div[@aria-haspopup = "menu"]'
    DASHBOARD_BUTTON_IN_CREATE = '//div[contains(@class, "ThemeableItemBackgroundStructure--isHighlighted")]'

    def __init__(self, driver):
        super().__init__(driver)
        self._config = ConfigProvider.load_config_json()

    def click_on_create_button(self):
        """
        Clicks on "Create" button to create a new dashboard.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.CREATE_BUTTON))
        ).click()

    def click_on_dashboard_button(self):
        """
        Clicks on "Dashboard" button. This button appears after pressing on "Create".
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.DASHBOARD_BUTTON_IN_CREATE))
        ).click()

    def go_to_dashboard_page(self):
        """
        Goes to dashboard page, the page that contains all the charts the user have picked.
        First it clicks on "Create" and then it clicks on "Dashboard".
        """
        self.click_on_create_button()
        self.click_on_dashboard_button()
