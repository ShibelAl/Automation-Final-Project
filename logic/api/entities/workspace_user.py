class WorkspaceUserEntity:
    def __init__(self, name):
        self._name = None
        self.set_name(name)

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def to_dict(self):
        return {
            "data": {
                "user": self.get_name()
            }
        }
