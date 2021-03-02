from dataclasses import dataclass


@dataclass
class FunctionObject:
    function_ptr: 'function'
    function_args: 'tuple'
    timeout_seconds: 'float' = None
