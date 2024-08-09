class BasePage:

    def __init__(self, driver):
        self._driver = driver

    def refresh_page(self):
        """
        This function refreshes the page.
        """
        self._driver.refresh()

    def go_back(self):
        """
        Navigates the browser to the previous page in the history.
        """
        self._driver.back()