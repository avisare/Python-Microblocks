from datetime import time


class FunctionObject:
    SECONDS_IN_HOUR = 3600
    SECOND_IN_MINUTE = 60

    def __init__(self, function_ptr: 'function' = None, function_args: 'tuple' = (), timeout: 'time' = None):
        self.function_ptr = function_ptr
        self.function_args = function_args
        if timeout is None:
            self.timeout_seconds = None
        else:
            self.timeout_seconds = timeout.hour*self.SECONDS_IN_HOUR + timeout.minute*self.SECOND_IN_MINUTE + timeout.second
