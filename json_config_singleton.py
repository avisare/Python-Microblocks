

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class JsonConfigSingleton(metaclass=Singleton):

    def __init__(self, json_config_dict):
        self.json_dictionary = json_config_dict


