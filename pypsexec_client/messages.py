
"""
The codes are:
ERROR = 0
SMT_INIT = 1
SMT_VERSION = 2
SMT_CREATE_TOPIC = 3
SMT_PUBLISH = 4
SMT_GET_BY_COUNTER = 5
SMT_GET_LATEST = 6
SMT_GET_OLDEST = 7
SMT_GET_PUBLISH_COUNT = 8
SMT_CLEAR_HISTORY = 9
EXIT = 999
"""


class Response:
    def __init__(self, response_code, response_object=None):
        self.response_code = response_code
        self.response_object = response_object


class Request:
    def __init__(self, request_code, arguments=None):
        self.request_code = request_code
        self.arguments = arguments
