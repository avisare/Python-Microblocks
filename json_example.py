from json_python import JsonHelper, JsonKeyNotFound
import test

class Example:

    def create_file(self):
        initial_content = {"intKey": 1, "strKey": "str", "array": [1, 2, 3, 4]}
        JsonHelper.write_into_file("example.json", initial_content)

    def set_existing_item(self):
        new_array = JsonHelper.get_value("array", "example.json")
        new_array.append(-13)
        JsonHelper.write_string("array", new_array, "example.json")


def main():
    example = Example()
    example.create_file()
    print(JsonHelper.get_string("intKey", "example.json"))
    print(JsonHelper.get_value("array", "example.json"))
    JsonHelper.write_string("newStr", 34.76, "example.json")
    example.set_existing_item()
    print(JsonHelper.get_value_if_exist("notExist", "example.json"))
    JsonHelper.delete_key("newStr", "example.json")
    JsonHelper.delete_key_if_exist("newStr", "example.json")
    try:
        JsonHelper.delete_key("newStr", "example.json")  # In this time, because we already delete the key,
        # we to get key not found error
    except JsonKeyNotFound as e:
        print(e.__str__())


if __name__ == "__main__":
    #main()
    test.test()
    print(test.y)
