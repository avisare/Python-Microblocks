from sys import argv
from os import system
from copy import deepcopy
from time import sleep
from threading import Thread
from pypsexec_client.shared_memory_factory import get_shared_memory, initialize_shared_memory
from shared_memory_client_test import TestClient
import parse_config
import SharedMemoryWrapper


def execute_remote_machine(remote_configs):
    system(f'py remote_agent.py {" ".join(remote_configs)}')


def add_if_exist(lst, dictionary, key):
    if key in dictionary.keys():
        lst.append(str(dictionary[key]))


def get_shared_memory_object_base_config(config_file_name):
    """
    function return shared memory object based on the configuration files
    :param config_file_name: list contains names of configuration files
    :return: shared memory object, shared memory client or the actual module
    """
    parse_config.init_configuration(config_file_name)
    if parse_config.config_dictionary["control"] == "local":
        return SharedMemoryWrapper
    remote_configs = [parse_config.config_dictionary["remote_username"],
                      parse_config.config_dictionary["remote_password"],
                      parse_config.config_dictionary["remote_ip"], parse_config.config_dictionary["mode"],
                      parse_config.config_dictionary["connection_type"],
                      str(parse_config.config_dictionary["timeout_seconds"]),
                      str(parse_config.config_dictionary["buffer_size_bytes"])]
    add_if_exist(remote_configs, parse_config.config_dictionary, "responder_port")
    add_if_exist(remote_configs, parse_config.config_dictionary, "responder_ip")
    add_if_exist(remote_configs, parse_config.config_dictionary, "initiator_port")
    local_configs = deepcopy(remote_configs)
    if parse_config.config_dictionary["mode"] == "strict":
        remote_configs[-3] = str(parse_config.config_dictionary["initiator_port"])
        remote_configs[-1] = str(parse_config.config_dictionary["responder_port"])
        remote_configs[-2] = parse_config.config_dictionary["initiator_ip"]
    if parse_config.config_dictionary["mode"] == "client":
        remote_configs[3] = "server"
    remote_thread = Thread(target=execute_remote_machine, args=(remote_configs,), daemon=True)
    remote_thread.start()
    print("waiting for server to up")
    sleep(5)
    return get_shared_memory(*local_configs[3:])


def run_test():
    shared_memory_object = get_shared_memory_object_base_config(["TCP_config.json", ])
    initialize_shared_memory(shared_memory_object)
    test = TestClient()
    test.setObject(shared_memory_object)
    test.run_test()


def main(configuration_files):
    shared_memory_object = get_shared_memory_object_base_config(configuration_files)
    initialize_shared_memory(shared_memory_object)
    # put your test commands you want to run on the remote machine
    # like shared_memory_object.getByCounter()


if __name__ == "__main__":
    run_test()
    """if len(argv) <= 1:
        print("You must pass at least one config file to the script")
    else:
        main(argv[1:])"""
