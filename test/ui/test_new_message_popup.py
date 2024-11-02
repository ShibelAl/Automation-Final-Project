import unittest
from infra.jira_bug_reporter import JiraBugReporter
from logic.ui.page_manager import PageManager
from infra.utils import Utils


class TestNewMessagePopUp(unittest.TestCase):
    def setUp(self):
        """
        Sets up the testing environment.
        """
        self.page_manager = PageManager()
        self.message_popup = self.page_manager.go_to_new_message_popup()

    def tearDown(self):
        """
        Closes the browser after completing the test.
        """
        self.page_manager.close_browser()

    @JiraBugReporter.report_bug(
        description="The title of a sent message is not visible to the user after sending. "
                    "The message title should be displayed in the message view.",
        priority="High",
        labels=["UI", "message", "message_title"]
    )
    def test_sent_message_title_is_visible(self):
        """
        This function tests if the title in the message that has been sent is visible.
        """
        # Arrange
        self.message_popup.add_message_receiver_email(self.page_manager.get_config("asana_email"))

        # Act
        self.message_popup.fill_add_subject_field(Utils.generate_random_string())
        self.message_popup.fill_message_content(Utils.generate_random_string())
        self.message_popup.click_on_send_button()
        self.message_popup.click_on_view_message_link()

        # Assert
        self.assertTrue(self.message_popup.view_message_title_is_visible())

    @JiraBugReporter.report_bug(
        description="The title of the sent message does not match the title entered by the user. "
                    "The displayed title should be identical to the title inputted when the message was sent.",
        priority="High",
        labels=["UI", "message", "message_title"]
    )
    def test_sent_message_title_is_correct(self):
        """
        This function tests if the title of the message that has been sent is identical
        to the title that the user inserted when sending the message.
        """
        # Arrange
        self.message_popup.add_message_receiver_email(self.page_manager.get_config("asana_email"))
        subject = Utils.generate_random_string()

        # Act
        self.message_popup.fill_add_subject_field(subject)
        self.message_popup.fill_message_content(Utils.generate_random_string())
        self.message_popup.click_on_send_button()
        self.message_popup.click_on_view_message_link()

        # Assert
        self.assertEqual(self.message_popup.view_message_title_text(), subject)
