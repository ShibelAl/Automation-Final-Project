import unittest
from infra.jira_bug_reporter import JiraBugReporter
from infra.utils import Utils
from infra.api.api_wrapper import APIWrapper
from logic.api.projects import Projects
from logic.ui.page_manager import PageManager
from logic.utils.logic_utils import LogicUtils


class TestSidebarProjects(unittest.TestCase):
    """
    This class contains test cases for creating and deleting projects,
    and verifying their presence in the home page sidebar.
    """
    def setUp(self):
        """
        Sets up the test environment before each test.
        """
        self.page_manager = PageManager()
        self.base_page_app = self.page_manager.go_to_base_page_app()
        self.api_request = APIWrapper()
        self.projects = Projects(self.api_request)
        self.project_created = False

    def tearDown(self):
        """
        Deletes the created project - if created one, and then closes the webdriver.
        """
        if self.project_created:
            # wait for projects to be present in the workspace before deletion
            project_gid = LogicUtils.wait_for_project_and_return_gid(self.projects)
            self.projects.delete_a_project(project_gid)

        self.page_manager.close_browser()

    @JiraBugReporter.report_bug(
        description="Creating a new project does not add it to the project list that appears in the sidebar.",
        priority="High",
        labels=["UI", "Project", "Creation"]
    )
    def test_create_a_project(self):
        """
        Tests creating a new project and verifying it is added to the list of existing projects.
        """
        # Arrange
        new_project_name = Utils.generate_random_string()

        # Act
        self.projects.create_a_project(new_project_name)
        self.project_created = True

        # Assert
        self.assertTrue(self.base_page_app.project_is_displayed(new_project_name),
                        f"The project '{new_project_name}' was not found in the project list.")

    @JiraBugReporter.report_bug(
        description="Deleting a project does not remove it from the project list that appears in the sidebar.",
        priority="Medium",
        labels=["UI", "Project", "Deletion"]
    )
    def test_delete_a_project(self):
        """
        Tests creating and deleting a project and verifying it is removed from the list of existing projects.
        """
        # Arrange
        new_project_name = Utils.generate_random_string()
        new_project = self.projects.create_a_project(new_project_name)
        new_project_gid = new_project.data["data"]["gid"]

        # Act
        self.projects.delete_a_project(new_project_gid)

        # Assert
        self.assertTrue(self.base_page_app.project_is_not_displayed(new_project_name),
                        f"The project '{new_project_name}' was found in the project list after deletion.")


if __name__ == '__main__':
    unittest.main()
