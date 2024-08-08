from infra.config_provider import ConfigProvider
from logic.api.entities.goal import GoalEntity


class Goals:
    REQUEST_URL_ENDPOINT = "goals"
    URL_QUERY = "?workspace="
    MY_WORKSPACE = "1207971857090881"

    def __init__(self, request):
        """
        Initializes the Goals class with a request object, configuration, and secret data.

        :param request: An instance of the request handler for making HTTP requests.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()
        self._secret = ConfigProvider().load_secret_json()

    def get_goals(self, workspace):
        """
        Retrieves all goals for a specified workspace.

        :param workspace: The workspace identifier for which to retrieve goals.
        :return: A response object containing the list of goals.
        """
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}{self.URL_QUERY}{workspace}"
        return self._request.get_request(url, self._secret['headers_without_content'])

    def create_a_goal(self, goal_name, workspace, time_period):
        """
        Creates a new goal in the specified workspace.

        :param goal_name: The name of the goal to be created.
        :param workspace: The workspace identifier where the goal will be created.
        :param time_period: The time period associated with the goal.
        :return: A response object from the goal creation request.
        """
        body = GoalEntity(goal_name, workspace, time_period)
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}"
        return self._request.post_request(url, self._secret['headers_with_content'], body.to_dict())

    def delete_a_goal(self, goal_gid):
        """
        Deletes a goal by its unique identifier (gid).

        :param goal_gid: The unique identifier of the goal to be deleted.
        :return: A response object from the goal deletion request.
        """
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}/{goal_gid}"
        return self._request.delete_request(url, self._secret['headers_without_content'])

    def update_a_goal(self, goal_gid, goal_name, workspace):
        """
        Updates an existing goal's name and workspace.

        :param goal_gid: The unique identifier of the goal to be updated.
        :param goal_name: The new name for the goal.
        :param workspace: The new workspace for the goal.
        :return: A response object from the goal update request.
        """
        body = GoalEntity(goal_name, workspace)
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}/{goal_gid}"
        return self._request.put_request(url, self._secret['headers_with_content'], body.to_dict())

    @staticmethod
    def goals_names(existing_goals):
        """
        Extracts the names of all goals from the provided goals data.

        :param existing_goals: A dictionary containing the existing goal's data.
        :return: A list of goal names.
        """
        return [goal['name'] for goal in existing_goals['data']]

    def delete_all_goals(self, workspace_gid):
        """
        Deletes all goals in the specified workspace.

        :param workspace_gid: The unique identifier (GID) of the workspace from which to delete all goals.
        :type workspace_gid: str

        :return: A list of responses for each delete operation.
        :rtype: list
        """
        response = self.get_goals(workspace_gid)
        goals = response.data['data']

        if not goals:
            raise ValueError("No goals found in the specified workspace.")

        delete_responses = []
        for goal in goals:
            goal_gid = goal['gid']
            delete_response = self.delete_a_goal(goal_gid)
            delete_responses.append(delete_response)

        return delete_responses

