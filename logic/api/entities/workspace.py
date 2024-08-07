class WorkspaceEntity:
    def __init__(self, name):
        self._workspace_name = None
        self.set_workspace_name(name)

    def set_workspace_name(self, workspace_name):
        self._workspace_name = workspace_name

    def get_workspace_name(self):
        return self._workspace_name

    def to_dict(self):
        return {
            "data": {
                "name": self.get_workspace_name()
            }
        }
