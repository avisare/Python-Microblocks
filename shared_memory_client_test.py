from os import system
from threading import Thread
from time import sleep
import unittest
from copy import deepcopy
from pypsexec_client.shared_memory_factory import get_shared_memory, initialize_shared_memory
import parse_config
from pypsexec_client.shared_memory_client import SharedMemoryClient
import SharedMemoryWrapper


class TestClient(unittest.TestCase):
    shared_memory_object = None
    shared_memory_objects = list()

    def setObject(self, shared_memory_object):
        TestClient.shared_memory_object = shared_memory_object

    def _create_topic(self):
        print("Create a new topic to the shared memory called SharedMemoryContent")
        TestClient.shared_memory_object.SMT_CreateTopic("SharedMemoryContent", 40, 3, 10)

    def _create_topic_object(self):
        try:
            print("Creating a shared memory object")
            shared_memory_first_object = SharedMemoryWrapper.SharedMemoryContent()
            print("Setting to cstringData of the object to equal to : 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'")
            shared_memory_first_object.cstringData = SharedMemoryWrapper.charList("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print("Setting to intData of the object to equal to : 1111")
            shared_memory_first_object.intData = 1111
            TestClient.shared_memory_objects.append(shared_memory_first_object)
            print("Creating another shared memory object")
            shared_memory_second_object = SharedMemoryWrapper.SharedMemoryContent()
            print("Setting to cstringData of the object to equal to : 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'")
            shared_memory_second_object.cstringData = SharedMemoryWrapper.charList("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
            print("Setting to intData of the object to equal to : 2222")
            shared_memory_second_object.intData = 2222
            TestClient.shared_memory_objects.append(shared_memory_second_object)
            print("returning")
            return True

        except Exception:
            return False

    def _publish_objects(self):
        print("Publishing all the objects we created")
        try:
            output = True
            for shared_memory_object in TestClient.shared_memory_objects:
                output = (output and TestClient.shared_memory_object.publish(shared_memory_object))
            return output
        except Exception:
            return False

    def _get_latest(self):
        print("Creating a temporary shared memory object")
        shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
        print("get the latest object enter to the memory, into the temporary object")
        TestClient.shared_memory_object.getLatest(shared_memory_temp_object)
        print("Now the temporary object contain the values:")
        print(f"cstringData: {shared_memory_temp_object.cstringData}, intData: {shared_memory_temp_object.intData}")
        return shared_memory_temp_object.cstringData, shared_memory_temp_object.intData

    def _get_by_counter(self):
        print("Creating a temporary shared memory object")
        shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
        print("get object by counter equal to 1 and timeout equal to 30, into the temporary object")
        TestClient.shared_memory_object.getByCounter(shared_memory_temp_object, 1, 30)
        print("Now the temporary object contain the values:")
        print(f"cstringData: {shared_memory_temp_object.cstringData}, intData: {shared_memory_temp_object.intData}")
        return shared_memory_temp_object.cstringData, shared_memory_temp_object.intData

    def _get_oldest(self):
        print("Creating a data info object")
        data_info = SharedMemoryWrapper.SMT_DataInfo()
        print("Creating a temporary shared memory object")
        shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
        print("get the oldest object enter into the shared memory, into the temporary object")
        TestClient.shared_memory_object.getOldest(shared_memory_temp_object, data_info)
        print("Now the temporary object contain the values:")
        print(f"cstringData: {shared_memory_temp_object.cstringData}, intData: {shared_memory_temp_object.intData}")
        print(f"data about the topic: data size: {data_info.m_dataSize}\npublish count: {data_info.m_publishCount}\npublish time:{data_info.m_publishTime}")
        return shared_memory_temp_object.cstringData, shared_memory_temp_object.intData, data_info.m_dataSize, data_info.m_publishCount

    def _init_memory(self):
        print("Init the shared memory")
        TestClient.shared_memory_object.SMT_Init()

    def _show_topic(self):
        print("Start the SMT_Show function on the SharedMemoryContent topic")
        TestClient.shared_memory_object.SMT_Show("SharedMemoryContent")

    def _get_publish_count(self):
        print("printing the number of objects publish with the topic SharedMemoryContent")
        TestClient.shared_memory_object.SMT_GetPublishCount("SharedMemoryContent")

    def _clear_history(self):
        print("Clear the history of the topic SharedMemoryContent")
        TestClient.shared_memory_object.SMT_ClearHistory("SharedMemoryContent")

    def test_1_create_topic_object(self):
        self.assertTrue(self._create_topic_object())

    def test_2_publish_objects(self):
        self.assertTrue(self._publish_objects())

    def test_3_get_latest(self):
        tuple_result = self._get_latest()
        self.assertEqual(tuple_result, (TestClient.shared_memory_objects[1].cstringData, TestClient.shared_memory_objects[1].intData))

    def test_4_get_by_counter(self):
        tuple_result = self._get_by_counter()
        self.assertEqual(tuple_result, (TestClient.shared_memory_objects[0].cstringData, TestClient.shared_memory_objects[0].intData))

    def test_5_get_oldest(self):
        tuple_result = self._get_oldest()
        self.assertEqual(tuple_result, (TestClient.shared_memory_objects[0].cstringData, TestClient.shared_memory_objects[0].intData, 36, 1))

    def run_test(self):
        unittest.main()

    @classmethod
    def tearDownClass(self):
        if type(self.shared_memory_object) == SharedMemoryClient:
            self.shared_memory_object.__del__()


def execute_remote_machine(remote_configs):
    system(f'py remote_agent.py {" ".join(remote_configs)}')


def add_if_exist(lst, dictionary, key):
    if key in dictionary.keys():
        lst.append(str(dictionary[key]))


def main():
    test_method = input("Enter what do you want to test:\n1. local shared memory\n"
                        "2. remote shared memory with UDP strict\n"
                        "3. remote shared memory with TCP server and client\n")
    local_configs = []
    if test_method == "1":
        local_config_file = ["local_config.json"]
        parse_config.init_configuration(local_config_file)
    else:
        if test_method == "2":
            local_config_file = ["UDP_config.json"]
            parse_config.init_configuration(local_config_file)
        elif test_method == "3":
            local_config_file = ["TCP_config.json"]
            parse_config.init_configuration(local_config_file)
        else:
            raise Exception(f"test method with number {test_method} was not found")
        remote_configs = [parse_config.config_dictionary["remote_username"], parse_config.config_dictionary["remote_password"],
                          parse_config.config_dictionary["remote_ip"], parse_config.config_dictionary["mode"],
                          parse_config.config_dictionary["connection_type"],
                          str(parse_config.config_dictionary["timeout_seconds"]), str(parse_config.config_dictionary["buffer_size_bytes"])]
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
        remote_thread = Thread(target=execute_remote_machine, args=(remote_configs, ), daemon=True)
        remote_thread.start()
        print("waiting for server to up")
        sleep(5)
    shared_memory_object = get_shared_memory(*local_configs[3:])
    initialize_shared_memory(shared_memory_object)
    test = TestClient()
    test.setObject(shared_memory_object)
    test.run_test()


if __name__ == "__main__":
    main()
