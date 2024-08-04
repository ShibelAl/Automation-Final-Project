class ProjectEntity:
    def __init__(self, name, workspace):
        self._name = name
        self._workspace = None
        self.set_name(name)
        self.set_workspace(workspace)

    def set_name(self, name):
        self._name = name

    def set_workspace(self, workspace):
        self._workspace = workspace

    def get_name(self):
        return self._name

    def get_workspace(self):
        return self._workspace

    def to_dict(self):
        return {
            "data": {
                "name": self.get_name(),
                "workspace": self.get_workspace()
            }
        }

