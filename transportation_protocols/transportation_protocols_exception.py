

class FunctionNotFound(Exception):
    def __init__(self, mode, connection_type):
        self._mode = mode
        self._connection_type = connection_type

    def __str__(self):
        return f"There is no such function with the mode: {self._mode}\n and the connection type of {self._connection_type} in the connection factory"


class ArgumentMustBeInteger(Exception):
    def __init__(self, argument_name):
        self._argument_name = argument_name

    def __str__(self):
        return f"The argument {self._argument_name} must be integer"


class ControlMethodNotFound(Exception):
    def __init__(self, control_method):
        self._control_method = control_method

    def __str__(self):
        return f"The control method named {self._control_method} was not found"
