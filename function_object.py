

class FunctionObject:

    def __init__(self, function_ptr: 'function' = None, function_args: 'tuple' = ()):
        self.function_ptr = function_ptr
        self.function_args = function_args
