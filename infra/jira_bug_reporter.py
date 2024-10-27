import logging
import traceback
from infra.logging_setup import LoggingSetup  # Ensure logging is properly set up

LoggingSetup()


class JiraBugReporter:
    @staticmethod
    def report_bug(description=None, priority="Medium", labels=None, components=None):
        """
        Static decorator to handle test failures, log errors, and report an issue to JIRA.
        Allows a custom description to be specified, or defaults to a detailed error trace.
        """
        def decorator(test_method):
            def wrapper(self):
                test_name = test_method.__name__
                try:
                    result = test_method(self)
                    logging.info(f"{test_name} - passed successfully")
                    return result
                except AssertionError as e:
                    # use custom description if provided (from the test decorator), otherwise use error trace
                    error_trace = traceback.format_exc()
                    issue_description = description or f"Test failed with error:\n{error_trace}"

                    # log the error
                    logging.error(f"{test_name} - assertion error")

                    # report the issue to JIRA
                    self.jira_handler.create_bug_issue(
                        project_key=self._config['jira_key'],
                        summary=f"Test Failure: {test_name}",
                        description=issue_description,
                        priority=priority,
                        labels=labels,
                        components=components,
                    )
                    raise e

                except Exception as e:
                    logging.exception(f"{test_name} - {e}\n")
                    raise e

            return wrapper

        return decorator
