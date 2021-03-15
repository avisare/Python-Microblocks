from json_python.json_helper import JsonHelper


def parse_config_files(config_files):
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
