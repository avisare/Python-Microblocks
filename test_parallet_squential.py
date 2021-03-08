import sequential_parallel
from time import sleep
from function_object import FunctionObject


def print_first_letters():
    letter = 'a'
    for i in range(10):
        print(chr(ord(letter) + i))
        sleep(0.1)


def print_last_letters():
    letter = 'z'
    for i in range(10):
        print(chr(ord(letter) - i))


def print_times_str(str_to_print, times):
    for i in range(times):
        print(str_to_print)


def sleep_thirty_seconds():
    print("start sleep")
    sleep(30)
    print("finish sleep")


def main():
    print("Start sequential")
    first_letters_printer = FunctionObject(print_first_letters, ())
    last_letter_printer = FunctionObject(print_last_letters, ())
    times_str_printer = FunctionObject(print_times_str, ("hello", 3))
    sleep_without_timeout = FunctionObject(sleep_thirty_seconds, ())
    sleep_with_timeout = FunctionObject(sleep_thirty_seconds, (), 3)
    sequential_parallel.start_sequential(first_letters_printer, last_letter_printer,
                                         times_str_printer, sleep_without_timeout)
    print("start parallel")
    sequential_parallel.start_parallel(first_letters_printer, last_letter_printer,
                                       times_str_printer, sleep_with_timeout)


if __name__ == "__main__":
    main()
