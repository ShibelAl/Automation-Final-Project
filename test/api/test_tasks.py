import unittest
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.api.projects import Projects
from logic.api.tasks import Tasks


class TestProjects(unittest.TestCase):
    def setUp(self):
        """
        Sets up the test cases by initializing necessary components.
        """
        self._config = ConfigProvider.load_config_json()
        self._api_request = APIWrapper()
        self.projects = Projects(self._api_request)
        self.tasks = Tasks(self._api_request)

    def test_create_a_task(self):
        """
        Tests creating a new task and verifying it is added to the list of existing tasks.
        """
        # Arrange
        new_project_name = Utils.generate_random_string()
        new_project = self.projects.create_a_project(new_project_name)
        new_project_gid = new_project.data['data']['gid']
        new_task_name = Utils.generate_random_string()

        # Act
        new_task = self.tasks.create_a_task(new_task_name, new_project_gid)
        existing_tasks = self.tasks.get_multiple_tasks(new_project_gid)

        # Assert
        self.assertEqual(new_project.status, 201)
        self.assertEqual(new_task.status, 201)
        self.assertEqual(existing_tasks.status, 200)
        self.assertIn(new_task_name, self.tasks.tasks_names(existing_tasks.data),
                      f"{new_task_name} not found in existing tasks.")

    def test_delete_a_task(self):
        """
        Tests deleting a task and verifying it is removed from the list of existing tasks.
        """
        # Arrange
        new_project_name = Utils.generate_random_string()
        new_project = self.projects.create_a_project(new_project_name)
        new_project_gid = new_project.data['data']['gid']

        new_task_name = Utils.generate_random_string()
        new_task = self.tasks.create_a_task(new_task_name, new_project_gid)
        new_task_gid = new_task.data['data']['gid']

        # Act
        deleting_a_task = self.tasks.delete_a_task(int(new_task_gid))
        existing_tasks = self.tasks.get_multiple_tasks(new_project_gid)

        # Assert
        self.assertEqual(new_project.status, 201)
        self.assertEqual(new_task.status, 201)
        self.assertEqual(existing_tasks.status, 200)
        self.assertEqual(deleting_a_task.status, 200)
        self.assertNotIn(new_task_name, self.tasks.tasks_names(existing_tasks.data),
                         f"{new_task_name} not found in existing tasks.")
