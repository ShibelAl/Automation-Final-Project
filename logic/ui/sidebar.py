from infra.ui.selenium_helpers import By, WebDriverWait, ec
from infra.config_provider import ConfigProvider
from infra.ui.base_page import BasePage


class SideBar(BasePage):
    REPORTING_BUTTON = '//a[@aria-label = "Reporting"]'

    def __init__(self, driver):
        super().__init__(driver)
        self._config = ConfigProvider().load_config_json()

    def click_on_reporting_button(self):
        """
        This function clicks on the "Reporting" button that appears in the sidebar.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.REPORTING_BUTTON))
        ).click()
