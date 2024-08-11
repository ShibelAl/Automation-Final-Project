import logging
from infra.logging_setup import LoggingSetup  # it appears not used, without it logging fails


class TestFailureHandler:
    @staticmethod
    def handle_test_failure(test_method):
        def wrapper(self):
            try:
                test_method(self)
            except AssertionError as e:
                test_name = test_method.__name__
                logging.error(f"{test_name} - assertion error")
                self.jira_handler.create_issue(self._config['jira_key'], test_name, f"Bug in {test_name}")
                raise e
        return wrapper
