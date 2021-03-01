from threading import Thread


def start_parallel(functions, arguments):

    threads_array = [Thread(target=function, args=argument) for function, argument in zip(functions, arguments)]

    [thread_function.start() for thread_function in threads_array]

    [thread_function.join() for thread_function in threads_array]


def start_sequential(functions, arguments):
    for function, argument in zip(functions, arguments):
        function(*argument)
