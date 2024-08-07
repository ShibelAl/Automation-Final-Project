class ResponseWrapper:
    def __init__(self, ok, status, data):
        """
        Initializes a ResponseWrapper instance with the given parameters.

        :param ok: Indicates whether the response was successful.
        :param status: The HTTP status code of the response.
        :param data: The response data in JSON format.
        """
        self.ok = ok
        self.status = status
        self.data = data

    @property
    def ok(self):
        """
        Gets the success indicator of the response.

        :return: The success indicator of the response.
        """
        return self._ok

    @ok.setter
    def ok(self, value):
        """
        Sets the success indicator of the response.

        :param value: The new success indicator of the response.
        """
        self._ok = value

    @property
    def status(self):
        """
        Gets the HTTP status code of the response.

        :return: The HTTP status code of the response.
        """
        return self._status

    @status.setter
    def status(self, value):
        """
        Sets the HTTP status code of the response.

        :param value: The new HTTP status code of the response.
        """
        self._status = value

    @property
    def data(self):
        """
        Gets the response data in JSON format.

        :return: The response data in JSON format.
        """
        return self._data

    @data.setter
    def data(self, value):
        """
        Sets the response data in JSON format.

        :param value: The new response data in JSON format.
        """
        self._data = value

    def __str__(self):
        """
        Returns a string representation of the ResponseWrapper instance.

        :return: A string representation of the ResponseWrapper instance.
        """
        return f"ResponseWrapper(ok={self.ok}, status={self.status}, data={self.data})"
