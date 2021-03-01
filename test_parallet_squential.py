import sequential_parallel
from time import sleep

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


def main():
    print("Start sequential")
    sequential_parallel.start_sequential([print_first_letters, print_last_letters, print_times_str], [(), (), ("hello", 3)])
    print("start parallel")
    sequential_parallel.start_parallel([print_first_letters, print_last_letters, print_times_str], [(), (), ("hello", 3)])


if __name__ == "__main__":
    main()
