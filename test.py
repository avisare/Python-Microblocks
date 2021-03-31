from copy import deepcopy
from time import sleep
from os import system
from threading import Thread
from pypsexec_client.shared_memory_factory import get_shared_memory, initialize_shared_memory
import parse_config
import SharedMemoryWrapper


def add_if_exist(lst, dictionary, key):
    if key in dictionary.keys():
        lst.append(str(dictionary[key]))


def execute_remote_machine(remote_configs):
    system(f'py remote_agent.py {" ".join(remote_configs)}')


def main():
    local_config_file = ["TCP_config.json"]
    parse_config.init_configuration(local_config_file)
    remote_configs = [parse_config.config_dictionary["remote_username"], parse_config.config_dictionary["remote_password"],
                      parse_config.config_dictionary["remote_ip"], parse_config.config_dictionary["mode"],
                      parse_config.config_dictionary["connection_type"],
                      str(parse_config.config_dictionary["timeout_seconds"]),
                      str(parse_config.config_dictionary["buffer_size_bytes"])]
    add_if_exist(remote_configs, parse_config.config_dictionary, "responder_port")
    add_if_exist(remote_configs, parse_config.config_dictionary, "responder_ip")
    add_if_exist(remote_configs, parse_config.config_dictionary, "initiator_port")
    local_configs = deepcopy(remote_configs)
    local_configs.insert(3, parse_config.config_dictionary["control"])
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
    shared_memory_object = get_shared_memory(*local_configs[3:])
    initialize_shared_memory(shared_memory_object)
    shared_memory_first_object = SharedMemoryWrapper.SharedMemoryContent()
    print("Setting to cstringData of the object to equal to : 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'")
    shared_memory_first_object.cstringData = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a',
                                              'a', 'a', 'a',
                                              'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
    print("Setting to intData of the object to equal to : 1111")
    shared_memory_first_object.intData = 1111
    shared_memory_object.SharedMemoryContentTopic().publish(shared_memory_first_object)
    print("Creating a temporary empty shared memory object")
    shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
    shared_memory_object.SharedMemoryContentTopic().getLatest(shared_memory_temp_object)
    print("Now the shared memory object contain:")
    newArr = [chr(char) for char in shared_memory_temp_object.cstringData]
    print(newArr)
    print(shared_memory_temp_object.intData)


if __name__ == "__main__":
    main()
