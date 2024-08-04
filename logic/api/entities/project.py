class ProjectEntity:
    """
    Represents a project entity with a name and a workspace.
    """

    def __init__(self, name, workspace):
        """
        Initializes the project entity with a name and workspace.
        """
        self._name = None
        self._workspace = None
        self.set_name(name)
        self.set_workspace(workspace)

    def set_name(self, name):
        """
        Sets the name of the project.
        """
        self._name = name

    def set_workspace(self, workspace):
        """
        Sets the workspace of the project.
        """
        self._workspace = workspace

    def get_name(self):
        """
        Returns the name of the project.
        """
        return self._name

    def get_workspace(self):
        """
        Returns the workspace of the project.
        """
        return self._workspace

    def to_dict(self):
        """
        Returns the project entity as a dictionary.
        """
        return {
            "data": {
                "name": self.get_name(),
                "workspace": self.get_workspace()
            }
        }
