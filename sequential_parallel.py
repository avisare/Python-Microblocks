from threading import Thread
from function_object import FunctionObject
import datetime
from time import time


SECONDS_IN_HOUR = 3600
SECOND_IN_MINUTE = 60


def get_timeout(timeout):
    if type(timeout) == datetime.time:
        timeout_seconds = timeout.hour * SECONDS_IN_HOUR + timeout.minute * SECOND_IN_MINUTE + timeout.second
    else:
        timeout_seconds = None
    return timeout_seconds


def start_parallel(*functions: 'FunctionObject'):
    timeout_seconds = get_timeout(functions[-1])  # the last argument is the timeout)
    if timeout_seconds is not None:
        functions = functions[:-1]
    threads_array = [Thread(target=function.function_ptr, args=function.function_args) for function in functions]
    for function_thread in threads_array:
        function_thread.daemon = True
    [thread_function.start() for thread_function in threads_array]
    [thread_function.join(timeout=timeout_seconds) for thread_function in threads_array]


def start_sequential(*functions: 'FunctionObject'):
    timeout_seconds = get_timeout(functions[-1])  # the last argument is the timeout)
    print(timeout_seconds)
    if timeout_seconds is not None:
        functions = functions[:-1]
    threads_array = [Thread(target=function.function_ptr, args=function.function_args) for function in functions]
    if timeout_seconds is None:
        execute_sequential_no_timeout(threads_array)
    else:
        execute_sequential_with_timeout(threads_array, timeout_seconds)


def execute_sequential_no_timeout(function_threads: 'list'):
    for function_thread in function_threads:
        function_thread.daemon = True
        function_thread.start()
        function_thread.join()


def execute_sequential_with_timeout(function_threads: 'list', timeout_seconds: 'int'):
    total_time_passed = 0
    for function_thread in function_threads:
        function_start = time()
        function_thread.daemon = True
        function_thread.start()
        function_thread.join(timeout_seconds-total_time_passed)
        total_time_passed += time() - function_start
        if timeout_seconds-total_time_passed < 0:
            return
