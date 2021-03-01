import json
from json_python.json_exceptions import JsonKeyNotFound, JsonValueWrongConversion


class JsonHelper:

    @staticmethod
    def write_into_file(json_file_path, json_content):
        with open(json_file_path, "w") as json_file:
            json.dump(json_content, json_file)

    @staticmethod
    def read_file(json_file_path):
        with open(json_file_path, "r") as json_file:
            json_data = json.load(json_file)
        return json_data

    @staticmethod
    def get_string(key, json_file_path):
        json_data = JsonHelper.read_file(json_file_path)
        if key not in json_data.keys():
            raise JsonKeyNotFound(key, json_file_path)
        try:
            value = json_data[key]
            string_value = str(value)
        except (SyntaxError, ValueError):
            raise JsonValueWrongConversion(value, "string")
        return string_value

    @staticmethod
    def get_value(key, json_file_path):
        json_data = JsonHelper.read_file(json_file_path)
        if key not in json_data.keys():
            raise JsonKeyNotFound(key, json_file_path)
        return json_data[key]

    @staticmethod
    def write_value(key, value, json_file_path):
        with open(json_file_path, "r") as json_file:
            json_data = json.load(json_file)
        json_data[key] = value
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file)

    @staticmethod
    def write_string(key, value, json_file_path):
        with open(json_file_path, "r") as json_file:
            json_data = json.load(json_file)
        try:
            string_value = str(value)
        except (SyntaxError, ValueError):
            raise JsonValueWrongConversion(value, "string")
        json_data[key] = string_value
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file)

    @staticmethod
    def delete_key(key, json_file_path):
        with open(json_file_path, "r") as json_file:
            json_data = json.load(json_file)
        if key not in json_data.keys():
            raise JsonKeyNotFound(key, json_file_path)
        del json_data[key]
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file)

    @staticmethod
    def is_key_exist(key, json_file_path):
        with open(json_file_path, "r") as json_file:
            json_data = json.load(json_file)
        return key in json_data.keys()

    @staticmethod
    def delete_key_if_exist(key, json_file_path):
        if JsonHelper.is_key_exist(key, json_file_path):
            JsonHelper.delete_key(key, json_file_path)

    @staticmethod
    def get_value_if_exist(key, json_file_path):
        if JsonHelper.is_key_exist(key, json_file_path):
            return JsonHelper.get_value(key, json_file_path)
        return None
