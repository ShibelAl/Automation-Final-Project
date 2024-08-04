from infra.config_provider import ConfigProvider


class GetMultipleProjects:
    """
    A class to retrieve multiple projects from Asana.
    """
    REQUEST_URL_ENDPOINT = "projects"

    def __init__(self, request):
        """
        Initializes with a request object.

        :param request: The request object used to make API calls.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()

    def get_multiple_projects(self):
        """
        Retrieves multiple projects using the request object.

        :return: The response from the API call to get multiple projects.
        """
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}"
        return self._request.get_request(url, self._config['get_multiple_projects_headers'])
