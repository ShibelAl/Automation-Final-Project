class UserEntity:
    def __init__(self, workspace):
        self._workspace = None
        self.set_workspace(workspace)

    def set_workspace(self, workspace):
        self._workspace = workspace

    def get_workspace(self):
        return self._workspace

    def to_dict(self):
        return {
            "data": {
                "workspace": self.get_workspace()
            }
        }
