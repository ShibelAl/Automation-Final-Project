import traceback
from infra.config_provider import ConfigProvider
from infra.logging_setup import logger
from infra.jira_handler import JiraHandler


class JiraBugReporter:
    _jira_handler = JiraHandler()
    _config = ConfigProvider().load_config_json()

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
                    logger.info(f"{test_name} - passed successfully")
                    return result
                except AssertionError as e:
                    # use custom description if provided (from the test decorator), otherwise use error trace
                    error_trace = traceback.format_exc()
                    issue_description = description or f"Test failed with error:\n{error_trace}"

                    # log the error
                    logger.error(f"{test_name} - assertion error")

                    # report the issue to jira
                    JiraBugReporter._jira_handler.create_bug_issue(
                        project_key=JiraBugReporter._config['jira_key'],
                        summary=f"Test Failure: {test_name}",
                        description=issue_description,
                        priority=priority,
                        labels=labels,
                        components=components,
                    )
                    raise e

                except Exception as e:
                    logger.error(f"{test_name} - **Check XPATH validity.")
                    raise e

            return wrapper

        return decorator
