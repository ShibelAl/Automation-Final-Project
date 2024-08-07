from infra.config_provider import ConfigProvider
from logic.api.entities.membership import MembershipEntity


class Memberships:
    REQUEST_URL_ENDPOINT = "memberships"

    def __init__(self, request):
        """
        Initializes with a request object.

        :param request: The request object used to make API calls.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()
        self._secret = ConfigProvider().load_secret_json()

    def add_a_membership(self, project_gid, user_gid):
        """
        Adds a membership to a project for a specified user.

        :param project_gid: The global ID of the project.
        :param user_gid: The global ID of the user.
        :return: The response from the API call to add a membership.
        """
        request_body = MembershipEntity(project_gid, user_gid)
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}"
        return self._request.post_request(url, self._secret['headers_with_content'], request_body.to_dict())

    def get_a_membership(self, membership_gid):
        """
        Retrieves the details of a membership by its global ID.

        :param membership_gid: The global ID of the membership.
        :return: The response from the API call to get the membership details.
        """
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}/{membership_gid}"
        return self._request.get_request(url, self._secret['headers_without_content'])
