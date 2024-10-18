from infra.config_provider import ConfigProvider
from logic.api.entities.workspace import WorkspaceEntity
from logic.api.entities.workspace_user import WorkspaceUserEntity


class Workspaces:
    URL_ENDPOINT = "workspaces/"
    PATH_PARAM = "/addUser"

    def __init__(self, request):
        """
        Initializes with a request object.

        :param request: The request object used to make API calls.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()
        self._secret = ConfigProvider().load_secret_json()

    def add_a_user_to_workspace(self, user_name):
        request_body = WorkspaceUserEntity(user_name)
        url = (f"{self._config['base_url_api']}{self.URL_ENDPOINT}{self._config['my_workspace_gid']}"
               f"{self.PATH_PARAM}")
        return self._request.post_request(url, self._secret['headers_without_content'], request_body.to_dict())

    def update_a_workspace_name(self, workspace_name):
        request_body = WorkspaceEntity(workspace_name)
        url = f"{self._config['base_url_api']}{self.URL_ENDPOINT}{self._config['my_workspace_gid']}"
        return self._request.put_request(url, self._secret['headers_with_content'], request_body.to_dict())

    def get_workspace(self, workspace_gid):
        url = f"{self._config['base_url_api']}{self.URL_ENDPOINT}{workspace_gid}"
        return self._request.get_request(url, self._secret['headers_without_content'])
