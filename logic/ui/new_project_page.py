from infra.ui.selenium_helpers import By, WebDriverWait, ec
from infra.config_provider import ConfigProvider
from infra.ui.base_page import BasePage


class NewProjectPage(BasePage):
    BLANK_PROJECT_BUTTON = '//div[@class = "DashedTile DashedTile--large FlowPickerTile-dashedTile"]'

    def __init__(self, driver):
        super().__init__(driver)
        self._config = ConfigProvider.load_config_json()

    def click_on_blank_project_button(self):
        """
        Clicks on the "Blank project" button.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.BLANK_PROJECT_BUTTON))
        ).click()
