

class JsonKeyNotFound(Exception):
    def __init__(self, key, json_file):
        self._missing_key = key
        self._json_file = json_file
        super().__init__("Json key not found")

    def __str__(self):
        return f'The key {self._missing_key} was not found in {self._json_file}'


class JsonValueWrongConversion(Exception):
    def __init__(self, value, conversion_type):
        self._value = value
        self._conversion_type = conversion_type
        super().__init__("Json wrong conversion")

    def __str__(self):
        return f'The value {self._value} cannot be converted to {self._conversion_type}'
