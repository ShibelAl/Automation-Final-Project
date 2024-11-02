import random
import time


class LogicUtils:
    """
    Utility class for logic and test functions.
    """
    @staticmethod
    def generate_random_binary():
        """
        Generates a random number that is either 0 or 1.

        :return: 0 or 1 (randomly chosen).
        """
        return random.randint(0, 1)

    @staticmethod
    def wait_for_goals_to_exist(saved_goals, workspace_gid, timeout=5, interval=1):
        """
        Waits for at least one goal to exist in the specified workspace.

        :param saved_goals: An instance or object responsible for fetching goals, expected to have a `get_goals` method.
        :param workspace_gid: The unique identifier (GID) of the workspace.
        :param timeout: Maximum time to wait in seconds.
        :param interval: Time to wait between checks in seconds.
        :return: True if goals exist within the timeout, False otherwise.
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            # fetch goals from the workspace
            response = saved_goals.get_goals(workspace_gid)
            goals = response.data['data']

            if goals:
                return True

            # wait for the interval before trying again
            time.sleep(interval)

        return False
