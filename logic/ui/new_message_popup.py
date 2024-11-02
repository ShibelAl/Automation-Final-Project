from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from logic.ui.base_page_app import BasePageApp
from infra.config_provider import ConfigProvider


class NewMessagePopUp(BasePageApp):
    ADD_SUBJECT = '//input[@placeholder = "Add subject"]'
    TO_INPUT_FIELD = '(//input[@placeholder = "Type the name of a team, a project, or people"])[1]'
    MESSAGE_BODY = '//p[@class = "ProsemirrorEditor-paragraph"]'
    SEND_BUTTON = '//div[text() = "Send"]'
    VIEW_MESSAGE_LINK = '//a[@class = "PrimaryNavigationLink"]'
    TITLE_FIELD_IN_VIEW_MESSAGE_MODE = '//textarea[@placeholder = "Write a message title"]'
    CLOSE_NEW_MESSAGE_POPUP_BUTTON = '//div[@class = "FocusTrap"]//div[@aria-label = "Close"]'
    CLOSE_DRAFT_MESSAGE_BUTTON = '//div[contains(@class, "collapsed")]//div[@aria-label = "Close"]'
    DELETE_BUTTON_CLOSING_DRAFT = '//div[text() = "Delete message"]'

    def __init__(self, driver):
        super().__init__(driver)
        self._message_receiver = None
        self._config = ConfigProvider.load_config_json()

    def fill_add_subject_field(self, subject):
        """
        This function fills the subject/title of the message with the parameter "subject"
        :param subject: a string that represents the subject of the message.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, self.ADD_SUBJECT))
        ).send_keys(subject)

    def add_message_receiver_email(self, email):
        """
        Inserts the email of the receiver of the message using the "email" parameter.
        :param email: a string that represents the email of the receiver.
        """
        self._message_receiver = WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, self.TO_INPUT_FIELD))
        )
        self._message_receiver.send_keys(email)
        self._message_receiver.send_keys(Keys.RETURN)

    def fill_message_content(self, message):
        """
        Fills the message content - the body of the message, using the message parameter.
        :param message: a string that represents the message to be sent.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, self.MESSAGE_BODY))
        ).send_keys(message)
        sleep(self._config["ui_update_time"])  # Allow time for the action to complete and UI to update

    def click_on_send_button(self):
        """
        Clicks on "send" button to send the message.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.SEND_BUTTON))
        ).click()

    def click_on_view_message_link(self):
        """
        Clicks on the link that shows in a pop-up after sending a message, after pressing
        on it, the user should see the message that he has sent.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.VIEW_MESSAGE_LINK))
        ).click()

    def view_message_title_is_visible(self):
        """
        Checks if the title is visible in the message after pressing on the link
        that shows the user the message he has sent.
        :return: True, if the message title is visible, False otherwise.
        """
        return WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.visibility_of_element_located((By.XPATH, self.TITLE_FIELD_IN_VIEW_MESSAGE_MODE))
        ).is_displayed()

    def view_message_title_text(self):
        """
        :return: The title of the message as text.
        """
        return WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.visibility_of_element_located((By.XPATH, self.TITLE_FIELD_IN_VIEW_MESSAGE_MODE))
        ).text

    def close_new_message_popup(self):
        """
        Closes the message pop-up by clicking on the x sign.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.element_to_be_clickable((By.XPATH, self.CLOSE_NEW_MESSAGE_POPUP_BUTTON))
        ).click()

    def click_on_to_field_in_message_popup(self):
        """
        Clicks on the "To" field, in order to fill it with the input afterward.
        """
        WebDriverWait(self._driver, self._config["wait_time"]).until(
            ec.presence_of_element_located((By.XPATH, self.TO_INPUT_FIELD))
        ).click()

    def close_draft_message(self):
        """
        Closes a draft message - if there was any - by clicking on the x sign.
        If there wasn't a draft message, a Timeout exception will appear, so the function will
        just pass, that means there is no draft message, carry on.
        """
        try:
            WebDriverWait(self._driver, self._config["ui_update_time"]).until(
                ec.element_to_be_clickable((By.XPATH, self.CLOSE_DRAFT_MESSAGE_BUTTON))
            ).click()
            sleep(self._config["ui_update_time"])
            WebDriverWait(self._driver, self._config["ui_update_time"]).until(
                ec.element_to_be_clickable((By.XPATH, self.DELETE_BUTTON_CLOSING_DRAFT))
            ).click()
            self.click_on_to_field_in_message_popup()
        except TimeoutException:
            pass
