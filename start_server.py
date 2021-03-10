import sys
import SharedMemoryWrapper
from shared_memory_server import SharedMemoryServer
from json_config_singleton import JsonConfigSingleton
from parse_config import parse_config_files


def main(config_files):
    config_dictionary = parse_config_files(config_files)
    JsonConfigSingleton(config_dictionary)

    server = SharedMemoryServer()
    server.start_server()


if __name__ == "__main__":
    main(sys.argv[1:])
