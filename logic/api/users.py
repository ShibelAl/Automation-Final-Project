from infra.config_provider import ConfigProvider
from logic.api.entities.user import UserEntity


class Users:
    REQUEST_URL_ENDPOINT = "users?workspace=1207971857090881"
    MY_WORKSPACE = "1207971857090881"

    def __init__(self, request):
        """
        Initializes with a request object.

        :param request: The request object used to make API calls.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()
        self._secret = ConfigProvider().load_secret_json()

    def get_workspace_users(self):
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}"
        return self._request.get_request(url, self._secret['headers_without_content'])

    @staticmethod
    def user_in_workspace(user_name, workspace_users):
        """
        Check if a user with the given name is present in the workspace users list.

        :param user_name: The name of the user to check for.
        :param workspace_users: The list of workspace users.
        :return: True if the user is in the workspace, False otherwise.
        """
        for user in workspace_users["data"]:
            if user["name"] == user_name:
                return True
        return False

    @staticmethod
    def users_gids_in_workspace(workspace_users):
        return [user["gid"] for user in workspace_users["data"]]
