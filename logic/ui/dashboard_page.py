import string
from time import sleep
from infra.ui.selenium_helpers import By, ActionChains, WebDriverWait, ec
from infra.config_provider import ConfigProvider
from logic.ui.base_page_app import BasePageApp


class DashboardPage(BasePageApp):
    INCOMPLETE_TASKS_GREEN_CHART = '//h5[contains(text(), "Incomplete tasks")]'
    ADD_BUTTON_IN_ADD_CHART_POPUP = '//div[text() = "Add"]'
    ADD_CHART_BUTTON = '//div[contains(@class, "PageToolbarStructure")]//div[@role = "button"]'
    PROJECTS_BY_STATUS = '(//div[@class = "CardGalleryCategory-card"][3])'
    LEFT_CHART_HEADER_TITLE_WRAPPER = '//h6[contains(text(), "Incomplete tasks")]'
    RIGHT_CHART_HEADER_TITLE_WRAPPER = '//h6[contains(text(), "Projects by project")]'
    ADD_FILTER_BUTTON = '//div[@role="button" and text()="Add filter"]'
    DATE_BUTTON_IN_FILTER = '//span[contains(text(), "Date")]'
    COMPLETION_DATE_BUTTON = '//span[contains(text(), "Completion date")]'
    DATE_FILTER_NUMBER_INPUT = '//input[@type = "number"]'

    def __init__(self, driver):
        super().__init__(driver)
        self._left_chart_header = None
        self._right_chart_header = None
        self._config = ConfigProvider.load_config_json()

    def click_on_incomplete_tasks_green_chart(self):
        """
        Clicks on the "Incomplete tasks by project" button/picture.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.INCOMPLETE_TASKS_GREEN_CHART))
        ).click()

    def fill_date_filter_input_field_with_all_punctuations(self):
        """
        Fills the input field with each punctuation/whitespace character,
        one by one, after scrolling to make the input field visible.

        This function only works on 'Incomplete tasks by project' chart.
        *** Just for training purposes.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.visibility_of_element_located((By.XPATH, self.ADD_FILTER_BUTTON))
        )
        add_filter_button_element = self._driver.find_element(By.XPATH, self.ADD_FILTER_BUTTON)

        # scroll down to the element and click it
        action = ActionChains(self._driver)
        action.move_to_element(add_filter_button_element).click().perform()

        # click on the other buttons to reach the input field
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.DATE_BUTTON_IN_FILTER))
        ).click()

        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.COMPLETION_DATE_BUTTON))
        ).click()

        # list of non_numeric characters to fill in the input field
        non_numeric_chars = list(string.punctuation + " \t\n")

        input_field = WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.DATE_FILTER_NUMBER_INPUT))
        )

        failing_chars = []

        # filling each character in non_numeric_chars into the input field
        for char in non_numeric_chars:
            input_field.clear()  # clear the field before entering the next character
            input_field.send_keys(char)

            # get the current value of the input field and check if the character is present
            current_value = input_field.get_attribute("value")

            # if the character is present, add it to the failing_chars list
            if char in current_value:
                failing_chars.append(char)

            input_field.clear()

        return failing_chars

    def click_on_create_button_in_add_chart_popup(self):
        """
        Clicks on "Create" button in add to chart pop-up.
        This button appears after pressing on "Add chart".
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.ADD_BUTTON_IN_ADD_CHART_POPUP))
        ).click()

    def click_on_add_chart_button(self):
        """
        Clicks on add chart button in the dashboard page.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.ADD_CHART_BUTTON))
        ).click()

    def click_on_projects_by_status(self):
        """
        Clicks on "Projects by status" button/picture (circular chart).
        This button appears after pressing on "Add chart"
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.PROJECTS_BY_STATUS))
        ).click()

    def add_two_charts_flow(self):
        """
        This function adds the "Incomplete tasks by project" green chart, and then adds a new
        chart, that is the "Projects by status" circular chart.
        """
        self.click_on_incomplete_tasks_green_chart()
        self.click_on_create_button_in_add_chart_popup()
        self.click_on_add_chart_button()
        self.click_on_projects_by_status()
        self.click_on_create_button_in_add_chart_popup()
        sleep(self._config["ui_update_time"])  # allow time for the action to complete and UI to update

    def drag_left_chart_to_right(self):
        """
        This function drags the left chart (green chart) and drops it in the right
        (on the circular chart). It uses the ActionChains module.
        """
        self._left_chart_header = WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.LEFT_CHART_HEADER_TITLE_WRAPPER)))

        self._right_chart_header = WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.RIGHT_CHART_HEADER_TITLE_WRAPPER)))

        ac = ActionChains(self._driver)
        ac.drag_and_drop(self._left_chart_header, self._right_chart_header).perform()
        sleep(self._config["ui_update_time"])  # allow time for the action to complete and UI to update

    def get_chart_location(self, chart_position):
        """
        :param chart_position: legally, can contain 'left' or 'right', and if not, the function
        raises a value error.
        :return: the location of the chart_position parameter. It takes the location
        from the "location" attribute, as a dictionary that consists of x and y coordinates.
        """
        if chart_position == 'left':
            chart_element = WebDriverWait(self._driver, self._config["wait_time"]).until(
                ec.element_to_be_clickable((By.XPATH, self.LEFT_CHART_HEADER_TITLE_WRAPPER)))

        elif chart_position == 'right':
            chart_element = WebDriverWait(self._driver, self._config["wait_time"]).until(
                ec.element_to_be_clickable((By.XPATH, self.RIGHT_CHART_HEADER_TITLE_WRAPPER)))

        else:
            raise ValueError("Invalid chart position specified. Use 'left' or 'right'.")

        return chart_element.location
