import sys
from pypsexec_client.shared_memory_factory import get_shared_memory, initialize_shared_memory
from json_config_singleton import JsonConfigSingleton
from parse_config import parse_config_files
from shared_memory_client_test import TestClient


def init_configuration(config_files):
    config_dictionary = parse_config_files(config_files)
    JsonConfigSingleton(config_dictionary)


def main(config_files):
    init_configuration(config_files)
    shared_memory_object = get_shared_memory()
    initialize_shared_memory(shared_memory_object)
    # put your test commands you want to run on the remote machine
    # like client.getByCounter()
    test = TestClient()
    test.setObject(shared_memory_object)
    test.run_test()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("You must pass at least one config file to the script")
    else:
        main(sys.argv[1:])
