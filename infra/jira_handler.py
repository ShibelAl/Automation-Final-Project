from jira import JIRA
from infra.config_provider import ConfigProvider


class JiraHandler:
    def __init__(self):
        self._config_provider = ConfigProvider()
        self._config = self._config_provider.load_config_json()
        self._secret = self._config_provider.load_secret_json()
        self._auth_jira = JIRA(
            basic_auth=(self._config['jira_email'], self._secret['jira_token']),
            options={'server': self._config['jira_url']}
        )

    def create_bug_issue(self, project_key, summary, description, issue_type="Bug",
                         priority="Medium", labels=None, components=None, attachments=None):
        """
        Create a JIRA issue and optionally attach files.
        """
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
            'priority': {'name': priority},
        }

        if labels:
            issue_dict['labels'] = labels
        if components:
            issue_dict['components'] = [{'name': comp} for comp in components]

        # Create the issue in JIRA
        new_issue = self._auth_jira.create_issue(fields=issue_dict)

        # If attachments are provided, upload them to the new issue
        if attachments:
            for file_path in attachments:
                self._auth_jira.add_attachment(issue=new_issue.key, attachment=file_path)

        return new_issue
