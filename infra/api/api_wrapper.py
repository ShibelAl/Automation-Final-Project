import requests


class APIWrapper:
    def __init__(self):
        self._request = None

    @staticmethod
    def get_request(url, header, querystring=None):
        return requests.get(url, headers=header, params=querystring)

    @staticmethod
    def post_request(url, header=None, body=None):
        return requests.post(url, headers=header, json=body)
