from infra.config_provider import ConfigProvider
from logic.api.entities.task import TaskEntity


class Tasks:
    """
    A class to handle tasks-related operations, such as creating, updating, and deleting tasks.
    """
    REQUEST_URL_ENDPOINT = "tasks"
    QUERY_PARAM = "?project="

    def __init__(self, request):
        """
        Initializes with a request object.

        :param request: The request object used to make API calls.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()
        self._secret = ConfigProvider().load_secret_json()

    def create_a_task(self, task_name, project_gid):
        """
        Creates a new task in the specified project.

        :param task_name: The name of the task to be created.
        :param project_gid: The global ID of the project in which to create the task.
        :return: The response from the API call to create the task.
        """
        body = TaskEntity(task_name, project_gid)
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}"
        return self._request.post_request(url, self._secret['headers_with_content'], body.to_dict())

    def get_multiple_tasks(self, project_gid):
        """
        Retrieves multiple tasks for the specified project.

        :param project_gid: The global ID of the project for which to retrieve tasks.
        :return: The response from the API call to get the tasks.
        """
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}{self.QUERY_PARAM}{project_gid}"
        return self._request.get_request(url, self._secret['headers_without_content'])

    def delete_a_task(self, task_gid):
        """
        Deletes a task with the specified global ID.

        :param task_gid: The global ID of the task to be deleted.
        :return: The response from the API call to delete the task.
        """
        url = f"{self._config['base_url_api']}{self.REQUEST_URL_ENDPOINT}/{task_gid}"
        return self._request.delete_request(url, self._secret['headers_without_content'])

    @staticmethod
    def tasks_names(existing_tasks):
        """
        Extracts the names of tasks from the given list of tasks.

        :param existing_tasks: The list of existing tasks.
        :return: A list of task names.
        """
        return [task['name'] for task in existing_tasks['data']]
