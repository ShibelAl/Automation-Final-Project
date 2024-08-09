import random


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
