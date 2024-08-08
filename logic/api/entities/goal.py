class GoalEntity:

    def __init__(self, name, workspace, time_period=None):
        """
        Initializes the GoalEntity with a name, workspace, and an optional time period.

        :param name: The name of the goal.
        :param workspace: The workspace to which the goal belongs.
        :param time_period: The time period associated with the goal (optional).
        """
        self._name = None
        self._workspace = None
        self._time_period = None
        self.set_name(name)
        self.set_workspace(workspace)
        self.set_time_period(time_period)

    def set_name(self, name):
        """
        Sets the name of the goal.

        :param name: The name of the goal.
        """
        self._name = name

    def set_workspace(self, workspace):
        """
        Sets the workspace for the goal.

        :param workspace: The workspace to which the goal belongs.
        """
        self._workspace = workspace

    def set_time_period(self, time_period):
        """
        Sets the time period for the goal.

        :param time_period: The time period associated with the goal.
        """
        self._time_period = time_period

    def get_name(self):
        """
        Gets the name of the goal.

        :return: The name of the goal.
        """
        return self._name

    def get_workspace(self):
        """
        Gets the workspace associated with the goal.

        :return: The workspace of the goal.
        """
        return self._workspace

    def get_time_period(self):
        """
        Gets the time period associated with the goal.

        :return: The time period of the goal.
        """
        return self._time_period

    def to_dict(self):
        """
        Converts the goal entity to a dictionary representation.

        :return: A dictionary containing the goal's name, workspace, and optionally the time period.
        """
        if self._time_period is None:
            return {
                "data": {
                    "name": self.get_name(),
                    "workspace": self.get_workspace()
                }
            }

        return {
            "data": {
                "name": self.get_name(),
                "workspace": self.get_workspace(),
                "time_period": self.get_time_period()
            }
        }
