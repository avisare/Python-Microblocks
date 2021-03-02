from threading import Thread
from function_object import FunctionObject


def start_parallel(*functions: 'FunctionObject'):

    threads_array = [Thread(target=function.function_ptr, args=function.function_args) for function in functions]
    timeout_array = [function.timeout_seconds for function in functions]
    [thread_function.start() for thread_function in threads_array]
    [thread_function.join(timeout=timeout) for thread_function, timeout in zip(threads_array, timeout_array)]


def start_sequential(*functions: 'FunctionObject'):
    for function in functions:
        function_thread = Thread(target=function.function_ptr, args=function.function_args)
        function_thread.start()
        function_thread.join(timeout=function.timeout_seconds)
