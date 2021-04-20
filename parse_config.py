from os import system
from copy import deepcopy
from threading import Thread
from time import sleep
from pypsexec_client.shared_memory_factory import get_shared_memory
from json_python.json_helper import JsonHelper

config_dictionary = None


def parse_config_files(config_files):
    """
    function parse config files into one dictionary, if there are
    multiplies, it overrides, and the later configuration file value is set
    :param config_files: the configuration files
    :return: dictionary contains all configurations
    """
    parsed_config_dictionary = dict()
    override_keys = dict()
    for config_file in config_files:
        config_file_dict = JsonHelper.read_file(config_file)
        shared_keys_between_dicts = config_file_dict.keys() & parsed_config_dictionary.keys()
        if len(shared_keys_between_dicts) > 0:
            for key in shared_keys_between_dicts:
                override_keys[key] = config_file
        parsed_config_dictionary.update(config_file_dict)
    if len(override_keys) > 0:
        print("**WARNING**\nYou are overriding the following keys in your config files:")
        [print(f"key name: {key}, file which key is taken from: {key_file}") for key, key_file in override_keys.items()]
        print("The key in the latest config file inserted to the parsed config")
    return parsed_config_dictionary


def init_configuration(config_files):
    """
    function initialize the global config_dictionary variable
    :param config_files: the configuration files
    :return: None
    """
    global config_dictionary
    config_dictionary = parse_config_files(config_files)


def execute_remote_machine(remote_configs):
    system(f'python remote_agent.py {" ".join(remote_configs)}')


def add_if_exist(lst, dictionary, key):
    if key in dictionary.keys():
        lst.append(str(dictionary[key]))


def execute_preparations():
    """
    function execute the remote server after the config_dictionary initialize
    :return: return the shared memory object created based on the config_dictionary
    """
    if config_dictionary["control"] == "local":
        return None, get_shared_memory("local")
    remote_configs = [config_dictionary["remote_username"],
                      config_dictionary["remote_password"],
                      config_dictionary["remote_ip"], config_dictionary["mode"],
                      config_dictionary["connection_type"],
                      str(config_dictionary["timeout_seconds"]),
                      str(config_dictionary["buffer_size_bytes"])]
    add_if_exist(remote_configs, config_dictionary, "responder_port")
    add_if_exist(remote_configs, config_dictionary, "responder_ip")
    add_if_exist(remote_configs, config_dictionary, "initiator_port")
    local_configs = deepcopy(remote_configs)
    local_configs.insert(3, config_dictionary["control"])
    if config_dictionary["mode"] == "strict":
        remote_configs[-3] = str(config_dictionary["initiator_port"])
        remote_configs[-1] = str(config_dictionary["responder_port"])
        remote_configs[-2] = config_dictionary["initiator_ip"]
    if config_dictionary["mode"] == "client":
        remote_configs[3] = "server"
    remote_thread = Thread(target=execute_remote_machine, args=(remote_configs,), name="execute_remote_machine")
    remote_thread.start()
    print("waiting for server to up")
    sleep(5)
    return remote_thread, get_shared_memory(*local_configs[3:])
