import sys
from shared_memory_server import SharedMemoryServer


def convert_suitable_type(lst, index):
    if lst[index].isnumeric():
        lst[index] = int(lst[index])
    elif lst[index] == 'None':
        lst[index] = None


def main(configurations):
    server = SharedMemoryServer()
    for i in range(len(configurations)):
        convert_suitable_type(configurations, i)
    server.start_server(configurations)


if __name__ == "__main__":
    main(sys.argv[1:])
