from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from infra.ui.base_page import BasePage


class NewProjectPage(BasePage):
    BLANK_PROJECT_BUTTON = '//div[@class = "DashedTile DashedTile--large FlowPickerTile-dashedTile"]'
    WAIT_TIME = 20

    def __init__(self, driver):
        super().__init__(driver)

    def click_on_blank_project_button(self):
        """
        Clicks on the "Blank project" button.
        """
        WebDriverWait(self._driver, self.WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, self.BLANK_PROJECT_BUTTON))
        ).click()
        WebDriverWait(self._driver, self.WAIT_TIME).until(
            EC.url_to_be("https://app.asana.com/0/projects/new/blank"))
