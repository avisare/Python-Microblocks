from threading import Thread
from function_object import FunctionObject


def execute_function(function_object: 'FunctionObject'):
    function_thread = Thread(target=function_object.function_ptr, args=function_object.function_args)
    function_thread.daemon = True
    function_thread.start()
    function_thread.join(timeout=function_object.timeout_seconds)


def start_parallel(*functions: 'FunctionObject'):
    threads_array = [Thread(target=execute_function, args=(function, )) for function in functions]
    [thread_function.start() for thread_function in threads_array]
    [thread_function.join() for thread_function in threads_array]


def start_sequential(*functions: 'FunctionObject'):
    for function in functions:
        execute_function(function)
