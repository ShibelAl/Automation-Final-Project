from jira import JIRA
from infra.config_provider import ConfigProvider


class JiraHandler:

    def __init__(self):
        self._config_provider = ConfigProvider()
        self._config = self._config_provider.load_config_json()
        self._secret = self._config_provider.load_secret_json()
        self._auth_jira = JIRA(
            basic_auth=(self._config['jira_email'],
                        self._secret['jira_token']),
            options={'server': self._config['jira_url']}
        )

    def create_issue(self, project_key, summary, description, issue_type="Bug"):
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type}
        }
        return self._auth_jira.create_issue(fields=issue_dict)
