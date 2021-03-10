import sequential_parallel
from time import sleep
from datetime import time
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


def sleep_five_seconds():
    print("hello")
    sleep(5)


def sleep_thirty_seconds():
    print("start sleep")
    sleep(30)
    print("finish sleep")


def main():
    print("Start sequential")
    first_letters_printer = FunctionObject(print_first_letters, ())
    last_letter_printer = FunctionObject(print_last_letters, ())
    times_str_printer = FunctionObject(print_times_str, ("hello", 3))
    sleep_thirty = FunctionObject(sleep_thirty_seconds, ())
    sleep_five = FunctionObject(sleep_five_seconds, ())
    sequential_parallel.start_sequential(first_letters_printer, last_letter_printer,
                                         times_str_printer, sleep_five, sleep_five, sleep_five, sleep_five, time(second=12))
    print("start parallel")
    sequential_parallel.start_parallel(first_letters_printer, last_letter_printer,
                                       times_str_printer, sleep_thirty, time(second=3))


if __name__ == "__main__":
    main()
