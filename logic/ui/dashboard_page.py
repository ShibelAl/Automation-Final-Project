import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from logic.ui.base_page_app import BasePageApp


class DashboardPage(BasePageApp):
    INCOMPLETE_TASKS_GREEN_CHART = '//h5[contains(text(), "Incomplete tasks")]'
    CREATE_BUTTON_IN_ADD_CHART_POPUP = '//div[text() = "Create"]'
    PROJECTS_BY_STATUS = '(//div[@class = "CardGalleryCategory-card"][3])'
    ADD_CHART_BUTTON = '//div[contains(@class, "PageToolbarStructure")]//div[@role = "button"]'
    LEFT_CHART_HEADER_TITLE_WRAPPER = '//h6[contains(text(), "Incomplete tasks")]'
    RIGHT_CHART_HEADER_TITLE_WRAPPER = '//h6[contains(text(), "Projects by project")]'

    def __init__(self, driver):
        super().__init__(driver)
        self._left_chart_header = None
        self._right_chart_header = None

    def click_on_incomplete_tasks_green_chart(self):
        """
        Clicks on the "Incomplete tasks by project" button/picture.
        """
        WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.INCOMPLETE_TASKS_GREEN_CHART))
        ).click()

    def click_on_create_button_in_add_chart_popup(self):
        """
        Clicks on "Create" button in add to chart pop-up.
        This button appears after pressing on "Add chart".
        """
        WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.CREATE_BUTTON_IN_ADD_CHART_POPUP))
        ).click()

    def click_on_add_chart_button(self):
        """
        Clicks on add chart button in the dashboard page.
        """
        WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.ADD_CHART_BUTTON))
        ).click()

    def click_on_projects_by_status(self):
        """
        Clicks on "Projects by status" button/picture (circular chart).
        This button appears after pressing on "Add chart"
        """
        WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.PROJECTS_BY_STATUS))
        ).click()

    def add_two_charts_flow(self):
        """
        This function adds the "Incomplete tasks by project" green chart, and then adds a new
        chart, that is the "Projects by status" circular chart.
        """
        logging.info("Adding two charts")
        self.click_on_incomplete_tasks_green_chart()
        self.click_on_create_button_in_add_chart_popup()
        self.click_on_add_chart_button()
        self.click_on_projects_by_status()
        self.click_on_create_button_in_add_chart_popup()
        time.sleep(2)  # Allow time for the action to complete and UI to update

    def drag_left_chart_to_right(self):
        """
        This function drags the left chart (green chart) and drops it in the right
        (on the circular chart). It uses the ActionChains module.
        """
        self._left_chart_header = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.LEFT_CHART_HEADER_TITLE_WRAPPER))
        )
        self._right_chart_header = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.RIGHT_CHART_HEADER_TITLE_WRAPPER))
        )
        ac = ActionChains(self._driver)
        ac.drag_and_drop(self._left_chart_header, self._right_chart_header).perform()
        time.sleep(1)  # Allow time for the action to complete and UI to update

    def get_chart_location(self, chart_position):
        """
        :param chart_position: legally, can contain 'left' or 'right', and if not, the function
        raises a value error.
        :return: the location of the chart_position parameter. It takes the location
        from the "location" attribute, as a dictionary that consists of x and y coordinates.
        """
        if chart_position == 'left':
            chart_element = self._driver.find_element(By.XPATH, self.LEFT_CHART_HEADER_TITLE_WRAPPER)
        elif chart_position == 'right':
            chart_element = self._driver.find_element(By.XPATH, self.RIGHT_CHART_HEADER_TITLE_WRAPPER)
        else:
            raise ValueError("Invalid chart position specified. Use 'left' or 'right'.")
        time.sleep(1)

        return chart_element.location
