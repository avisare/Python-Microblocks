from json_python.json_helper import JsonHelper


def parse_config_files(config_files):
    parsed_config_dictionary = dict()
    override_keys = set()
    for config_file in config_files:
        config_file_dict = JsonHelper.read_file(config_file)
        shared_keys_between_dicts = config_file_dict & parsed_config_dictionary
        if len(shared_keys_between_dicts) > 0:
            override_keys.update(shared_keys_between_dicts)
        parsed_config_dictionary.update(config_file)
    if len(override_keys) > 0:
        print("**WARNING**\nYou are overriding the following keys in your config files:")
        [print(key, end=" ") for key in override_keys]
        print("The key in the latest config file inserted to the parsed config")
    return parsed_config_dictionary
