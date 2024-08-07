class MembershipEntity:

    def __init__(self, parent, member):
        """
        Initializes a MembershipEntity instance with the given parent and member.

        :param parent: The parent entity (e.g., project) to which the membership belongs.
        :param member: The member entity (e.g., user) being added to the parent entity.
        """
        self._parent = None
        self._member = None
        self.set_parent(parent)
        self.set_member(member)

    def set_parent(self, parent):
        """
        Sets the parent entity.

        :param parent: The parent entity (e.g., project) to which the membership belongs.
        """
        self._parent = parent

    def set_member(self, member):
        """
        Sets the member entity.

        :param member: The member entity (e.g., user) being added to the parent entity.
        """
        self._member = member

    def get_parent(self):
        """
        Gets the parent entity.

        :return: The parent entity.
        """
        return self._parent

    def get_member(self):
        """
        Gets the member entity.

        :return: The member entity.
        """
        return self._member

    def to_dict(self):
        """
        Returns the membership entity as a dictionary.

        :return: A dictionary representation of the membership entity.
        """
        return {
            "data": {
                "parent": self.get_parent(),
                "member": self.get_member()
            }
        }
