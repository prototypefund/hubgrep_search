import json

import requests

class CachedResponse:
    """
    wrapper class for cached responses

    url -
        url this request was made to
    success -
        True, if status_code was 2XX
    status_code -
        http status code of the response.
        will be `-1` if an exception was thrown, and we didnt get a status code.
    response_json -
        dict from the response json data
    error_msg -
        http error message, if we had a response code,
        otherwise the exception text
    """
    def __init__(self, url, success, status_code, response_json, error_msg):
        self.url = url
        self.success = success
        self.status_code = status_code
        self.response_json = response_json
        self.error_msg = error_msg

    def serialize(self) -> str:
        """
        get serialized version to put in cache
        """
        d = dict(
            url=self.url,
            success=self.success,
            status_code=self.status_code,
            response_json=self.response_json,
            error_msg=self.error_msg,
        )
        return json.dumps(d)

    @staticmethod
    def from_serialized(data: str):
        """
        make CachedResponse object from serialized CachedResponse
        """
        d = json.loads(data)

        url = d["url"]
        success = d["success"]
        status_code = d["status_code"]
        response_json = d["response_json"]
        error_msg = d["error_msg"]
        result = CachedResponse(
            url=url,
            success=success,
            status_code=status_code,
            response_json=response_json,
            error_msg=error_msg,
        )
        return result

    @staticmethod
    def from_response(response: requests.Response):
        url = response.url
        status_code = response.status_code
        response_json = response.json()
        if response.ok:
            success = True
            error_msg = None
        else:
            success = False
            error_msg = response.text

        result = CachedResponse(
            url=url,
            success=success,
            status_code=status_code,
            response_json=response_json,
            error_msg=error_msg,
        )
        return result

    @staticmethod
    def from_exception(url, exception_str):
        return CachedResponse(
            url=url,
            success=False,
            status_code=-1,
            response_json=None,
            error_msg=exception_str,
        )
