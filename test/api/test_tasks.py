import unittest
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.api.projects import Projects
from logic.api.tasks import Tasks


class TestTasks(unittest.TestCase):
    """
    This class contains test cases for creating, verifying, and deleting tasks,
    ensuring that tasks are correctly added to and removed from projects.
    """

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
        Tests creating a new task and verifying it was successfully created.

        Essential steps:
        1. Generate a random project name and create a new project.
        2. Generate a random task name and create a new task within the project.
        3. Verify that the task was successfully created with a 201 status code.
        """
        # Arrange
        new_project_name = Utils.generate_random_string()
        new_project = self.projects.create_a_project(new_project_name)
        new_project_gid = new_project.data['data']['gid']
        new_task_name = Utils.generate_random_string()

        # Act
        new_task = self.tasks.create_a_task(new_task_name, new_project_gid)

        # Assert
        self.assertEqual(new_task.status, 201)

    def test_task_added_to_exact_project(self):
        """
        Tests that a task is correctly added to the specified project.

        Essential steps:
        1. Generate a random project name and create a new project.
        2. Generate a random task name and create a new task within the project.
        3. Retrieve the list of existing tasks for the project.
        4. Verify that the created task is present in the list of existing tasks.
        """
        # Arrange
        new_project_name = Utils.generate_random_string()
        new_project = self.projects.create_a_project(new_project_name)
        new_project_gid = new_project.data['data']['gid']
        new_task_name = Utils.generate_random_string()

        # Act
        self.tasks.create_a_task(new_task_name, new_project_gid)
        existing_tasks = self.tasks.get_multiple_tasks(new_project_gid)

        # Assert
        self.assertEqual(existing_tasks.status, 200)
        self.assertIn(new_task_name, self.tasks.tasks_names(existing_tasks.data),
                      f"{new_task_name} not found in existing tasks.")

    def test_delete_a_task(self):
        """
        Tests deleting a task and verifying it is removed from the list of existing tasks.

        Essential steps:
        1. Create a project and a task with a randomly generated names.
        3. Delete the task.
        4. Retrieve the list of existing tasks for the project.
        5. Verify that the task is not in the list of existing tasks after deletion.
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
        self.assertEqual(deleting_a_task.status, 200)
        self.assertNotIn(new_task_name, self.tasks.tasks_names(existing_tasks.data),
                         f"{new_task_name} not found in existing tasks.")


if __name__ == '__main__':
    unittest.main()
