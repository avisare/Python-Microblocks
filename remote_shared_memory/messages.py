
class Response:
    def __init__(self, response_code, response_object=None):
        self.response_code = response_code
        self.response_object = response_object


class Request:
    def __init__(self, request_code, arguments=None):
        self.request_code = request_code
        self.arguments = arguments
