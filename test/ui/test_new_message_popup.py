import logging
import unittest
from infra.ui.browser_wrapper import BrowserWrapper
from infra.config_provider import ConfigProvider
from logic.ui.login_page import LoginPage
from logic.ui.base_page_app import BasePageApp
from logic.ui.new_message_popup import NewMessagePopUp
from infra.utils import Utils


class TestNewMessagePopUp(unittest.TestCase):
    def setUp(self):
        """
        Sets up the testing environment, completes the login process to enter to the main page,
        opens a new message pop-up and deletes the previous draft (if there was any).
        Works automatically.
        """
        self.browser = BrowserWrapper()
        self.config = ConfigProvider.load_config_json()
        self.secret = ConfigProvider.load_secret_json()
        self.driver = self.browser.get_driver(self.config["base_url"])
        self.login_page = LoginPage(self.driver)
        self.login_page.login_flow(self.config["asana_email"], self.secret["asana_password"])
        self.base_page_app = BasePageApp(self.driver)
        self.base_page_app.click_on_create_button()
        self.base_page_app.click_on_message_button_in_create()
        self.message_popup = NewMessagePopUp(self.driver)
        self.message_popup.close_draft_message()

    def tearDown(self):
        """
        Closes the browser after completing the test.
        Works automatically.
        """
        self.driver.quit()

    def test_sent_message_title_is_visible(self):
        """
        This function tests if the title in the message that has been sent is visible.
        """
        logging.info("Test sent message title is visible - test started")
        # Arrange
        self.message_popup.add_message_receiver_email(self.config["asana_email"])
        # Act
        self.message_popup.fill_add_subject_field(Utils.generate_random_string())
        self.message_popup.fill_message_content(Utils.generate_random_string())
        self.message_popup.click_on_send_button()
        self.message_popup.click_on_view_message_link()
        # Assert
        self.assertTrue(self.message_popup.view_message_title_is_visible())

    def test_sent_message_title_is_correct(self):
        """
        This function tests if the title of the message that has been sent is identical
        to the title that the user inserted when sending the message.
        """
        logging.info("Test sent message title is correct - test started")
        # Arrange
        self.message_popup.add_message_receiver_email(self.config["asana_email"])
        subject = Utils.generate_random_string()
        # Act
        self.message_popup.fill_add_subject_field(subject)
        self.message_popup.fill_message_content(Utils.generate_random_string())
        self.message_popup.click_on_send_button()
        self.message_popup.click_on_view_message_link()
        # Assert
        self.assertEqual(self.message_popup.view_message_title_text(), subject)
