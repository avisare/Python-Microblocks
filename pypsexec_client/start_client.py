import SharedMemoryWrapper
from shared_memory_factory import getSharedMemory


class Test:
    def __init__(self, client):
        self._client = client
        self._init_memory()
        self._shared_memory_objects = list()

    def _create_topic(self):
        print("Create a new topic to the shared memory called SharedMemoryContent")
        self._client.SMT_CreateTopic("SharedMemoryContent", 40, 3, 10)

    def _create_topic_object(self):
        print("Creating a shared memory object")
        shared_memory_first_object = SharedMemoryWrapper.SharedMemoryContent()
        print("Setting to cstringData of the object to equal to : 'first'")
        shared_memory_first_object.cstringData = SharedMemoryWrapper.charList("first")
        print("Setting to intData of the object to equal to : 1111")
        shared_memory_first_object.intData = 1111
        self._shared_memory_objects.append(shared_memory_first_object)
        print("Creating another shared memory object")
        shared_memory_second_object = SharedMemoryWrapper.SharedMemoryContent()
        print("Setting to cstringData of the object to equal to : 'second'")
        shared_memory_second_object.cstringData = SharedMemoryWrapper.charList("second")
        print("Setting to intData of the object to equal to : 2222")
        shared_memory_second_object.intData = 2222
        self._shared_memory_objects.append(shared_memory_second_object)

    def _publish_objects(self):
        print("Publishing all the objects we created")
        for shared_memory_object in self._shared_memory_objects:
            self._client.send(shared_memory_object)

    def _get_latest(self):
        print("Creating a temporary shared memory object")
        shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
        print("get the latest object enter to the memory, into the temporary object")
        self._client.latestRx(shared_memory_temp_object)
        print("Now the temporary object contain the values:")

        print(f"cstringData: {shared_memory_temp_object.cstringData}, intData: {shared_memory_temp_object.intData}")

    def _get_by_counter(self):
        print("Creating a temporary shared memory object")
        shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
        print("get object by counter equal to 1 ant timeout equal to 30, into the temporary object")
        self._client.receive(shared_memory_temp_object, 1, 30)
        print("Now the temporary object contain the values:")
        print(f"cstringData: {shared_memory_temp_object.cstringData}, intData: {shared_memory_temp_object.intData}")

    def _get_oldest(self):
        print("Creating a data info object")
        data_info = SharedMemoryWrapper.SMT_DataInfo()
        print("Creating a temporary shared memory object")
        shared_memory_temp_object = SharedMemoryWrapper.SharedMemoryContent()
        print("get the oldest object enter into the shared memory, into the temporary object")
        self._client.oldestRx(shared_memory_temp_object, data_info)
        print("Now the temporary object contain the values:")
        print(f"cstringData: {shared_memory_temp_object.cstringData}, intData: {shared_memory_temp_object.intData}")
        print(f"data about the topic: data size: {data_info.m_dataSize}\npublish count: {data_info.m_publishCount}\npublish time:{data_info.m_publishTime}")

    def _init_memory(self):
        print("Init the shared memory")
        self._client.SMT_Init()

    def _show_topic(self):
        print("Start the SMT_Show function on the SharedMemoryContent topic")
        self._client.SMT_Show("SharedMemoryContent")

    def _get_publish_count(self):
        print("printing the number of objects publish with the topic SharedMemoryContent")
        self._client.SMT_GetPublishCount("SharedMemoryContent")

    def _clear_history(self):
        print("Clear the history of the topic SharedMemoryContent")
        self._client.SMT_ClearHistory("SharedMemoryContent")

    def run_test(self):
        self._create_topic()
        self._create_topic_object()
        self._publish_objects()
        self._get_latest()
        self._get_by_counter()
        self._get_oldest()


def main():
    client = getSharedMemory()
    test = Test(client)
    test.run_test()


if __name__ == "__main__":
    main()
