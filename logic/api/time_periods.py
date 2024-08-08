import random
from infra.config_provider import ConfigProvider


class TimePeriods:
    """
    A class to interact with time periods within a workspace.
    """
    REQUEST_URL_ENDPOINT = "time_periods"
    WORKSPACE_QUERY = "?workspace="
    OPT_FIELDS = "&opt_fields="
    MY_WORKSPACE = "1207971857090881"

    def __init__(self, request):
        """
        Initializes with a request object.

        :param request: The request object used to make API calls.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()
        self._secret = ConfigProvider().load_secret_json()

    def get_time_periods(self, workspace_gid):
        """
        Retrieves the time periods associated with the specified workspace.

        :param workspace_gid: The unique identifier (GID) of the workspace for which to retrieve time periods.
        :return: The API response containing the list of time periods for the given workspace.
        """
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}{self.WORKSPACE_QUERY}{workspace_gid}"
        return self._request.get_request(url, self._secret['headers_without_content'])

    def get_random_time_period(self, workspace):
        """
        Retrieves a random time period's 'gid' from the list of time periods for the given workspace.

        :param workspace: The workspace identifier to get time periods from.
        :return: A random 'gid' from the list of time periods.
        """
        response = self.get_time_periods(workspace)
        time_periods = response.data['data']

        if not time_periods:
            raise ValueError("No time periods found for the given workspace.")

        random_time_period = random.choice(time_periods)
        return random_time_period['gid']
