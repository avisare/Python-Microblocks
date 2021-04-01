import unittest
from numpy import float32
import parse_config
from pypsexec_client.shared_memory_client import SharedMemoryClient
from pypsexec_client.shared_memory_factory import initialize_shared_memory
import SharedMemoryWrapper


class TestClient(unittest.TestCase):
    shared_memory_object = None
    shared_memory_objects = list()

    def setObject(self, shared_memory_object):
        TestClient.shared_memory_object = shared_memory_object

    def _create_topic(self):
        print("Create a new topic to the shared memory called SharedMemoryContent")
        TestClient.shared_memory_object.SMT_CreateTopic("SharedMemoryContentTopic", 40, 3, 10)

    def _create_topic_object(self):
        try:
            print("Creating a shared memory object")
            shared_memory_first_object = SharedMemoryWrapper.SharedMemoryContent()
            print("Setting to cstringData of the object to equal to : 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'")
            shared_memory_first_object.cstringData = ['a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a',
                                                      'a','a','a','a','a','a','a','a','a','a','a','a','a','a']
            print("Setting to intData of the object to equal to : 1111")
            shared_memory_first_object.intData = 1111
            TestClient.shared_memory_objects.append(shared_memory_first_object)
            print("Creating another shared memory object")
            shared_memory_second_object = SharedMemoryWrapper.SharedMemoryContent()
            print("Setting to cstringData of the object to equal to : 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'")
            shared_memory_second_object.cstringData = ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',
                                                       'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',
                                                       'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']
            print("Setting to intData of the object to equal to : 2222")
            shared_memory_second_object.intData = 2222
            TestClient.shared_memory_objects.append(shared_memory_second_object)
            shared_memory_third_object = SharedMemoryWrapper.testStructOne()
            shared_memory_third_object.intNumber = 20
            shared_memory_third_object.floatNumber = 44.4
            shared_memory_third_object.character = 'z'
            shared_memory_third_object.arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            TestClient.shared_memory_objects.append(shared_memory_third_object)
            shared_memory_fourth_object = SharedMemoryWrapper.testStructOne()
            shared_memory_fourth_object.intNumber = 100
            shared_memory_fourth_object.floatNumber = 105.78
            shared_memory_fourth_object.character = 'f'
            shared_memory_third_object.arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
            TestClient.shared_memory_objects.append(shared_memory_fourth_object)
            shared_memory_fifth_object = SharedMemoryWrapper.testStructThree()
            shared_memory_fifth_object.booleanValue = True
            shared_memory_fifth_object.floatValue = 9.9
            shared_memory_fifth_object.charArray = ['c'] * 32
            TestClient.shared_memory_objects.append(shared_memory_fifth_object)
            shared_memory_sixth_object = SharedMemoryWrapper.testStructThree()
            shared_memory_sixth_object.booleanValue = True
            shared_memory_sixth_object.floatValue = 67.87
            shared_memory_sixth_object.charArray = ['t'] * 32
            TestClient.shared_memory_objects.append(shared_memory_sixth_object)
            shared_memory_seventh_object = SharedMemoryWrapper.testStructTwo()
            shared_memory_seventh_object.longNumber = 123456
            shared_memory_seventh_object.uintNumber = 55
            shared_memory_seventh_object.boolean = True
            shared_memory_seventh_object.structThree = shared_memory_fifth_object
            TestClient.shared_memory_objects.append(shared_memory_seventh_object)
            shared_memory_eighth_object = SharedMemoryWrapper.testStructTwo()
            shared_memory_eighth_object.longNumber = 23456
            shared_memory_eighth_object.uintNumber = 88
            shared_memory_eighth_object.boolean = True
            shared_memory_eighth_object.structThree = shared_memory_sixth_object
            TestClient.shared_memory_objects.append(shared_memory_eighth_object)
            shared_memory_ninth_object = SharedMemoryWrapper.testStructFour()
            shared_memory_ninth_object.singleInteger = 123
            shared_memory_ninth_object.dimensionalArray = [[1, 2, 3], [4, 5, 6]]
            TestClient.shared_memory_objects.append(shared_memory_ninth_object)
            shared_memory_tenth_object = SharedMemoryWrapper.testStructFour()
            shared_memory_tenth_object.singleInteger = 456
            shared_memory_tenth_object.dimensionalArray = [[6, 5, 4], [3, 2, 1]]
            TestClient.shared_memory_objects.append(shared_memory_tenth_object)
            return True

        except Exception as e:
            print("error!!:" + e.__str__())
            return False

    def _publish_objects(self):
        print("Publishing all the objects we created")
        index = 0
        try:
            output = True
            for shared_memory_struct in TestClient.shared_memory_objects:
                if index < 2:
                    output = (output and TestClient.shared_memory_object.SharedMemoryContentTopic().publish(shared_memory_struct))
                elif index < 4:
                    output = (output and TestClient.shared_memory_object.testStructOneTopic().publish(shared_memory_struct))
                elif index < 6:
                    output = (output and TestClient.shared_memory_object.testStructThreeTopic().publish(shared_memory_struct))
                elif index < 8:
                    output = (output and TestClient.shared_memory_object.testStructTwoTopic().publish(shared_memory_struct))
                else:
                    output = (output and TestClient.shared_memory_object.testStructFourTopic().publish(shared_memory_struct))
                index += 1
            return output
        except Exception as e:
            print(f"error at index:{index} {e.__str__()}")
            return False

    def _get_latest(self):
        print("Creating a temporary shared memory object")
        shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
        print("get the latest object enter to the memory, into the temporary object")
        TestClient.shared_memory_object.SharedMemoryContentTopic().getLatest(shared_memory_temp_object)
        print("Now the temporary object contain the values:")
        lst = [chr(char) for char in shared_memory_temp_object.cstringData]
        print(f"cstringData: {lst}, intData: {shared_memory_temp_object.intData}")
        return lst, shared_memory_temp_object.intData

    def _get_latest_data(self):
        shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
        data_info = SharedMemoryWrapper.SMT_DataInfo()
        TestClient.shared_memory_object.SharedMemoryContentTopic().getLatest(shared_memory_temp_object, data_info)
        lst = [chr(char) for char in shared_memory_temp_object.cstringData]
        return lst, shared_memory_temp_object.intData, data_info.m_dataSize, data_info.m_publishCount

    def _get_by_counter(self):
        print("Creating a temporary shared memory object")
        shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
        print("get object by counter equal to 1 and timeout equal to 30, into the temporary object")
        topic = TestClient.shared_memory_object.SharedMemoryContentTopic()
        topic.getByCounter(shared_memory_temp_object, 1, 30)
        print("Now the temporary object contain the values:")
        lst = [chr(char) for char in shared_memory_temp_object.cstringData]
        print(f"cstringData: {lst}, intData: {shared_memory_temp_object.intData}")
        return lst, shared_memory_temp_object.intData

    def _get_by_counter_data(self):
        shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
        data_info = SharedMemoryWrapper.SMT_DataInfo()
        TestClient.shared_memory_object.SharedMemoryContentTopic().getByCounter(shared_memory_temp_object, 1, 30, data_info)
        lst = [chr(char) for char in shared_memory_temp_object.cstringData]
        return lst, shared_memory_temp_object.intData, data_info.m_dataSize, data_info.m_publishCount

    def _get_oldest(self):
        shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
        TestClient.shared_memory_object.SharedMemoryContentTopic().getOldest(shared_memory_temp_object)
        lst = [chr(char) for char in shared_memory_temp_object.cstringData]
        return lst, shared_memory_temp_object.intData

    def _get_oldest_data(self):
        print("Creating a data info object")
        data_info = SharedMemoryWrapper.SMT_DataInfo()
        print("Creating a temporary shared memory object")
        shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
        print("get the oldest object enter into the shared memory, into the temporary object")
        TestClient.shared_memory_object.SharedMemoryContentTopic().getOldest(shared_memory_temp_object, data_info)
        print("Now the temporary object contain the values:")
        lst = [chr(char) for char in shared_memory_temp_object.cstringData]
        print(f"cstringData: {lst}, intData: {shared_memory_temp_object.intData}")
        print(f"data about the topic: data size: {data_info.m_dataSize}\npublish count: {data_info.m_publishCount}\npublish time:{data_info.m_publishTime}")
        return lst, shared_memory_temp_object.intData, data_info.m_dataSize, data_info.m_publishCount

    def _get_oldest_struct_one(self):
        shared_memory_temp_object = SharedMemoryWrapper.testStructOne()
        TestClient.shared_memory_object.testStructOneTopic().getOldest(shared_memory_temp_object)
        return shared_memory_temp_object.intNumber, shared_memory_temp_object.floatNumber, shared_memory_temp_object.character, shared_memory_temp_object.arr

    def _get_latest_struct_one(self):
        shared_memory_temp_object = SharedMemoryWrapper.testStructOne()
        TestClient.shared_memory_object.testStructOneTopic().getLatest(shared_memory_temp_object)
        return shared_memory_temp_object.intNumber, shared_memory_temp_object.floatNumber, shared_memory_temp_object.character, shared_memory_temp_object.arr

    def _get_latest_struct_two(self):
        shared_memory_temp_object = SharedMemoryWrapper.testStructTwo()
        TestClient.shared_memory_object.testStructTwoTopic().getLatest(shared_memory_temp_object)
        return shared_memory_temp_object.longNumber, shared_memory_temp_object.uintNumber, shared_memory_temp_object.boolean, shared_memory_temp_object.structThree

    def _get_latest_struct_three(self):
        shared_memory_temp_object = SharedMemoryWrapper.testStructThree()
        TestClient.shared_memory_object.testStructThreeTopic().getLatest(shared_memory_temp_object)
        return shared_memory_temp_object.booleanValue, float32(shared_memory_temp_object.floatValue), shared_memory_temp_object.charArray

    def _get_latest_struct_four(self):
        shared_memory_temp_object = SharedMemoryWrapper.testStructFour()
        TestClient.shared_memory_object.testStructFourTopic().getLatest(shared_memory_temp_object)
        return shared_memory_temp_object.singleInteger, shared_memory_temp_object.dimensionalArray

    def _get_oldest_struct_two(self):
        shared_memory_temp_object = SharedMemoryWrapper.testStructTwo()
        TestClient.shared_memory_object.testStructTwoTopic().getOldest(shared_memory_temp_object)
        return shared_memory_temp_object.longNumber, shared_memory_temp_object.uintNumber, shared_memory_temp_object.boolean, shared_memory_temp_object.structThree

    def _get_oldest_struct_three(self):
        shared_memory_temp_object = SharedMemoryWrapper.testStructThree()
        TestClient.shared_memory_object.testStructThreeTopic().getOldest(shared_memory_temp_object)
        return shared_memory_temp_object.booleanValue, float32(shared_memory_temp_object.floatValue), shared_memory_temp_object.charArray

    def _get_oldest_struct_four(self):
        shared_memory_temp_object = SharedMemoryWrapper.testStructFour()
        TestClient.shared_memory_object.testStructFourTopic().getOldest(shared_memory_temp_object)
        return shared_memory_temp_object.singleInteger, shared_memory_temp_object.dimensionalArray

    def _get_by_counter_struct_one(self):
        shared_memory_temp_object = SharedMemoryWrapper.testStructOne()
        TestClient.shared_memory_object.testStructOneTopic().getByCounter(shared_memory_temp_object, 1, 30)
        return shared_memory_temp_object.intNumber, shared_memory_temp_object.floatNumber, shared_memory_temp_object.character, shared_memory_temp_object.arr

    def _get_by_counter_struct_two(self):
        shared_memory_temp_object = SharedMemoryWrapper.testStructTwo()
        TestClient.shared_memory_object.testStructTwoTopic().getByCounter(shared_memory_temp_object, 1, 30)
        return shared_memory_temp_object.longNumber, shared_memory_temp_object.uintNumber, shared_memory_temp_object.boolean, shared_memory_temp_object.structThree

    def _get_by_counter_struct_three(self):
        shared_memory_temp_object = SharedMemoryWrapper.testStructThree()
        TestClient.shared_memory_object.testStructThreeTopic().getByCounter(shared_memory_temp_object, 1, 30)
        return shared_memory_temp_object.booleanValue, float32(shared_memory_temp_object.floatValue), shared_memory_temp_object.charArray

    def _get_by_counter_struct_four(self):
        shared_memory_temp_object = SharedMemoryWrapper.testStructFour()
        TestClient.shared_memory_object.testStructFourTopic().getByCounter(shared_memory_temp_object, 1, 30)
        return shared_memory_temp_object.singleInteger, shared_memory_temp_object.dimensionalArray

    def _init_memory(self):
        print("Init the shared memory")
        TestClient.shared_memory_object.SMT_Init()

    def _show_topic(self):
        print("Start the SMT_Show function on the SharedMemoryContentTopic")
        TestClient.shared_memory_object.SMT_Show("SharedMemoryContentTopic")

    def _get_publish_count(self):
        print("printing the number of objects publish with the topic SharedMemoryContentTopic")
        TestClient.shared_memory_object.SMT_GetPublishCount("SharedMemoryContentTopic")

    def _clear_history(self):
        print("Clear the history of the topic SharedMemoryContentTopic")
        TestClient.shared_memory_object.SMT_ClearHistory("SharedMemoryContentTopic")

    def test_1_create_topic_object(self):
        self.assertTrue(self._create_topic_object())

    def test_2_publish_objects(self):
        self.assertTrue(self._publish_objects())

    def test_3_get_latest_content(self):
        tuple_result = self._get_latest()
        self.assertEqual(tuple_result, (['b']*32, TestClient.shared_memory_objects[1].intData))

    def test_4_get_by_counter(self):
        tuple_result = self._get_by_counter()
        self.assertEqual(tuple_result, (['a'] * 32, TestClient.shared_memory_objects[0].intData))

    def test_5_get_oldest_data_content(self):
        tuple_result = self._get_oldest_data()
        self.assertEqual(tuple_result, (['a'] * 32, TestClient.shared_memory_objects[0].intData, 36, 1))

    def test_6_get_latest_data_content(self):
        tuple_result = self._get_latest_data()
        self.assertEqual(tuple_result, (['b'] * 32, TestClient.shared_memory_objects[1].intData, 36, 2))

    def test_7_get_by_counter_data_content(self):
        tuple_result = self._get_by_counter_data()
        self.assertEqual(tuple_result, (['a'] * 32, TestClient.shared_memory_objects[0].intData, 36, 1))

    def test_8_get_oldest_content(self):
        tuple_result = self._get_oldest()
        self.assertEqual(tuple_result, (['a'] * 32, TestClient.shared_memory_objects[0].intData))

    def test_9_get_latest_struct_one(self):
        tuple_result = self._get_latest_struct_one()
        self.assertEqual(tuple_result[:-1], (TestClient.shared_memory_objects[3].intNumber, float32(TestClient.shared_memory_objects[3].floatNumber), TestClient.shared_memory_objects[3].character))
        self.assertTrue(self._compare_lists(tuple_result[-1].tolist(), TestClient.shared_memory_objects[3].arr.tolist()))

    def test_A_get_by_counter_struct_one(self):
        tuple_result = self._get_by_counter_struct_one()
        self.assertEqual(tuple_result[:-1], (TestClient.shared_memory_objects[2].intNumber, float32(TestClient.shared_memory_objects[2].floatNumber), TestClient.shared_memory_objects[2].character))
        self.assertTrue(self._compare_lists(tuple_result[-1].tolist(), TestClient.shared_memory_objects[2].arr.tolist()))

    def test_B_get_oldest_struct_one(self):
        tuple_result = self._get_oldest_struct_one()
        self.assertEqual(tuple_result[:-1], (TestClient.shared_memory_objects[2].intNumber, float32(TestClient.shared_memory_objects[2].floatNumber), TestClient.shared_memory_objects[2].character))
        self.assertTrue(self._compare_lists(tuple_result[-1].tolist(), TestClient.shared_memory_objects[2].arr.tolist()))

    def test_C_get_latest_struct_two(self):
        tuple_result = self._get_latest_struct_two()
        self.assertEqual(tuple_result[:-1], (TestClient.shared_memory_objects[7].longNumber, TestClient.shared_memory_objects[7].uintNumber, TestClient.shared_memory_objects[7].boolean))
        self.assertTrue(self._compare_struct_three(TestClient.shared_memory_objects[7].structThree, tuple_result[-1]))

    def test_D_get_by_counter_struct_two(self):
        tuple_result = self._get_by_counter_struct_two()
        self.assertEqual(tuple_result[:-1], (TestClient.shared_memory_objects[6].longNumber, TestClient.shared_memory_objects[6].uintNumber, TestClient.shared_memory_objects[6].boolean))
        self.assertTrue(self._compare_struct_three(TestClient.shared_memory_objects[6].structThree, tuple_result[-1]))

    def test_E_get_oldest_struct_two(self):
        tuple_result = self._get_oldest_struct_two()
        self.assertEqual(tuple_result[:-1], (TestClient.shared_memory_objects[6].longNumber, TestClient.shared_memory_objects[6].uintNumber, TestClient.shared_memory_objects[6].boolean))
        self.assertTrue(self._compare_struct_three(TestClient.shared_memory_objects[6].structThree, tuple_result[-1]))

    def test_F_get_latest_struct_three(self):
        tuple_result = self._get_latest_struct_three()
        tuple_result = (tuple_result[0], tuple_result[1], [chr(char) for char in tuple_result[-1]])
        self.assertEqual(tuple_result, (TestClient.shared_memory_objects[5].booleanValue, float32(TestClient.shared_memory_objects[5].floatValue), ['t'] * 32))

    def test_G_get_by_counter_struct_three(self):
        tuple_result = self._get_by_counter_struct_three()
        tuple_result = (tuple_result[0], tuple_result[1], [chr(char) for char in tuple_result[-1]])
        self.assertEqual(tuple_result, (TestClient.shared_memory_objects[4].booleanValue, float32(TestClient.shared_memory_objects[4].floatValue), ['c'] * 32))

    def test_H_get_oldest_struct_three(self):
        tuple_result = self._get_oldest_struct_three()
        tuple_result = (tuple_result[0], tuple_result[1], [chr(char) for char in tuple_result[-1]])
        self.assertEqual(tuple_result, (TestClient.shared_memory_objects[4].booleanValue, float32(TestClient.shared_memory_objects[4].floatValue), ['c'] * 32))

    def test_I_get_latest_struct_four(self):
        tuple_result = self._get_latest_struct_four()
        self.assertEqual(tuple_result[:-1], (TestClient.shared_memory_objects[9].singleInteger, ))
        self.assertTrue(self._compare_lists(tuple_result[-1].tolist(), TestClient.shared_memory_objects[9].dimensionalArray.tolist()))

    def test_J_get_by_counter_struct_four(self):
        tuple_result = self._get_by_counter_struct_four()
        self.assertEqual(tuple_result[:-1], (TestClient.shared_memory_objects[8].singleInteger,))
        self.assertTrue(self._compare_lists(tuple_result[-1].tolist(), TestClient.shared_memory_objects[8].dimensionalArray.tolist()))

    def test_K_get_oldest_struct_four(self):
        tuple_result = self._get_oldest_struct_four()
        self.assertEqual(tuple_result[:-1], (TestClient.shared_memory_objects[8].singleInteger,))
        self.assertTrue(self._compare_lists(tuple_result[-1].tolist(), TestClient.shared_memory_objects[8].dimensionalArray.tolist()))

    def _compare_struct_three(self, first_struct, second_struct):
        lst = [chr(char) for char in first_struct.charArray]
        lst1 = [chr(char) for char in second_struct.charArray]
        return first_struct.booleanValue == second_struct.booleanValue and \
               float32(first_struct.floatValue) == float32(second_struct.floatValue) and lst == lst1

    def _compare_lists(self, lst1, lst2):
        lst1 = lst1.sort()
        lst2 = lst2.sort()
        return lst1 == lst2

    def run_test(self):
        unittest.main()

    @classmethod
    def tearDownClass(self):
        if type(self.shared_memory_object) == SharedMemoryClient:
            self.shared_memory_object.__del__()


def main():
    test_method = input("Enter what do you want to test:\n1. local shared memory\n"
                        "2. remote shared memory with UDP strict\n"
                        "3. remote shared memory with TCP server and client\n")
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
    shared_memory_object = parse_config.execute_preparations()
    initialize_shared_memory(shared_memory_object)
    test = TestClient()
    test.setObject(shared_memory_object)
    test.run_test()


if __name__ == "__main__":
    main()
