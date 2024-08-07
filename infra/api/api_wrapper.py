import requests

from infra.api.response_wrapper import ResponseWrapper


class APIWrapper:
    def __init__(self):
        self._request = None

    @staticmethod
    def get_request(url, headers=None, json=None):
        try:
            response = requests.get(
                url,
                headers=headers,
                json=json
            )
            response.raise_for_status()
            return ResponseWrapper(ok=response.ok, status=response.status_code, data=response.json())
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error occurred: {e}')
        except Exception as e:
            print(f'Other error occurred: {e}')
        return None

    @staticmethod
    def post_request(url, headers=None, json=None):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=json
            )
            response.raise_for_status()
            return ResponseWrapper(ok=response.ok, status=response.status_code, data=response.json())
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error occurred: {e}')
        except Exception as e:
            print(f'Other error occurred: {e}')
        return None

    @staticmethod
    def delete_request(url, headers=None):
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return ResponseWrapper(ok=response.ok, status=response.status_code, data=response.json())
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error occurred: {e}')
        except Exception as e:
            print(f'Other error occurred: {e}')
        return None

    @staticmethod
    def put_request(url, headers=None, json=None):
        try:
            response = requests.put(
                url,
                headers=headers,
                json=json
            )
            response.raise_for_status()
            return ResponseWrapper(ok=response.ok, status=response.status_code, data=response.json())
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error occurred: {e}')
        except Exception as e:
            print(f'Other error occurred: {e}')
        return None

