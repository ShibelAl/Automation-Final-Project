class TaskEntity:

    def __init__(self, name, project):
        """
        Initializes a TaskEntity instance with the given name and project.

        :param name: The name of the task.
        :param project: The project to which the task belongs.
        """
        self._name = None
        self._project = None
        self.set_name(name)
        self.set_project(project)

    def set_name(self, name):
        """
        Sets the name of the task.

        :param name: The name of the task.
        """
        self._name = name

    def set_project(self, project):
        """
        Sets the project to which the task belongs.

        :param project: The project to which the task belongs.
        """
        self._project = project

    def get_name(self):
        """
        Gets the name of the task.

        :return: The name of the task.
        """
        return self._name

    def get_project(self):
        """
        Gets the project to which the task belongs.

        :return: The project to which the task belongs.
        """
        return self._project

    def to_dict(self):
        """
        Returns the task entity as a dictionary.

        :return: A dictionary representation of the task entity.
        """
        return {
            "data": {
                "name": self.get_name(),
                "projects": self.get_project()
            }
        }
