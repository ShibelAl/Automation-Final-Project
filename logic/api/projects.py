from infra.utils import Utils
from infra.config_provider import ConfigProvider
from logic.api.entities.project import ProjectEntity


class Projects:
    """
    A class to handle projects-related operations, like creating, updating and deleting projects.
    """
    REQUEST_URL_ENDPOINT = "projects"
    MY_WORKSPACE = "1207971857090881"

    def __init__(self, request):
        """
        Initializes with a request object.

        :param request: The request object used to make API calls.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()
        self._secret = ConfigProvider().load_secret_json()

    def get_multiple_projects(self):
        """
        Retrieves multiple projects using the request object.

        :return: The response from the API call to get multiple projects.
        """
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}"
        return self._request.get_request(url, self._secret['projects_headers'])

    def create_a_project(self):
        """
        Creates a new project in the website.
        """
        body = ProjectEntity(Utils.generate_random_string(), self.MY_WORKSPACE)
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}"
        return self._request.post_request(url, self._secret['projects_headers'], body.to_dict())
