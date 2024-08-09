from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from infra.ui.base_page import BasePage


class SideBar(BasePage):
    REPORTING_BUTTON = '//a[@aria-label = "Reporting"]'

    def __init__(self, driver):
        super().__init__(driver)
        self._reporting_button = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.REPORTING_BUTTON))
        )

    def click_on_reporting_button(self):
        """
        This function clicks on the "Reporting" button that appears in the sidebar.
        """
        self._reporting_button.click()
