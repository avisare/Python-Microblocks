from pickle import loads, dumps
from tcp_communication import TCP_Connection
from messages import Request, Response
import SharedMemoryWrapper


class SharedMemoryClient:
    BUFFER_SIZE = 1024
    ERROR = 0
    SMT_INIT = 1
    SMT_VERSION = 2
    SMT_CREATE_TOPIC = 3
    SMT_PUBLISH = 4
    SMT_GET_BY_COUNTER = 5
    SMT_GET_LATEST = 6
    SMT_GET_OLDEST = 7
    SMT_GET_PUBLISH_COUNT = 8
    SMT_CLEAR_HISTORY = 9
    EXIT = 999

    def __init__(self, server_port, server_ip="127.0.0.1"):
        self._connection = TCP_Connection(server_port, True, server_ip)

    def SMT_Init(self):
        request = Request(self.SMT_INIT)
        self._connection.send(dumps(request))
        return loads(self._connection.receive(self.BUFFER_SIZE)).response_code

    def SMT_Version(self):
        request = Request(self.SMT_VERSION)
        self._connection.send(dumps(request))
        return loads(self._connection.receive(self.BUFFER_SIZE)).response_object

    def SMT_CreateTopic(self, topic_name, max_data_size, history_depth, cells_count):
        request = Request(self.SMT_CREATE_TOPIC, (topic_name, max_data_size, history_depth, cells_count))
        self._connection.send(dumps(request))
        return loads(self._connection.receive(self.BUFFER_SIZE)).response_code

    def SMT_GetPublishCount(self, topic_name):
        request = Request(self.SMT_GET_PUBLISH_COUNT, topic_name)
        self._connection.send(dumps(request))
        return loads(self._connection.receive(self.BUFFER_SIZE)).response_object

    def SMT_ClearHistory(self, topic_name):
        request = Request(self.SMT_CLEAR_HISTORY, topic_name)
        self._connection.send(dumps(request))
        return loads(self._connection.receive(self.BUFFER_SIZE)).response_code

    def oldestRx(self, smt_object, data_info_object=None):
        if data_info_object is None:
            request = Request(self.SMT_GET_OLDEST, smt_object)
            self._connection.send(dumps(request))
            response = loads(self._connection.receive(self.BUFFER_SIZE))
            temp_obj = response.response_object
            self._copy_shared_memory_object(temp_obj, smt_object)
            return response.response_code
        else:
            request = Request(self.SMT_GET_OLDEST, (smt_object, data_info_object))
            self._connection.send(dumps(request))
            response = loads(self._connection.receive(self.BUFFER_SIZE))
            temp_obj, temp_data = response.response_object
            self._copy_shared_memory_object(temp_obj, smt_object)
            self._copy_shared_memory_object(temp_data, data_info_object)
            return response.response_code

    def getOldest(self, smt_object, data_info_object=None):
        if data_info_object is None:
            request = Request(self.SMT_GET_OLDEST, smt_object)
            self._connection.send(dumps(request))
            response = loads(self._connection.receive(self.BUFFER_SIZE))
            temp = response.response_object
            self._copy_shared_memory_object(temp, smt_object)
            return response.response_code
        else:
            request = Request(self.SMT_GET_OLDEST, (smt_object, data_info_object))
            self._connection.send(dumps(request))
            response = loads(self._connection.receive(self.BUFFER_SIZE))
            temp_obj, temp_data = response.response_object
            self._copy_shared_memory_object(temp_obj, smt_object)
            self._copy_shared_memory_object(temp_data, data_info_object)
            return response.response_code

    def receive(self, smt_object, counter, timeout, data_info_object=None):
        if data_info_object is None:
            request = Request(self.SMT_GET_BY_COUNTER, [smt_object, counter, timeout])
            self._connection.send(dumps(request))
            response = loads(self._connection.receive(self.BUFFER_SIZE))
            temp_object = response.response_object
            self._copy_shared_memory_object(temp_object, smt_object)
            return response.response_code
        else:
            request = Request(self.SMT_GET_BY_COUNTER, [smt_object, counter, timeout, data_info_object])
            self._connection.send(dumps(request))
            response = loads(self._connection.receive(self.BUFFER_SIZE))
            temp_obj, temp_data = response.response_object
            self._copy_shared_memory_object(temp_obj, smt_object)
            self._copy_shared_memory_object(temp_data, data_info_object)
            return response.response_code

    def getByCounter(self, smt_object, counter, timeout, data_info_object=None):
        if data_info_object is None:
            request = Request(self.SMT_GET_BY_COUNTER, (smt_object, counter, timeout))
            self._connection.send(dumps(request))
            response = loads(self._connection.receive(self.BUFFER_SIZE))
            temp_obj = response.response_object
            self._copy_shared_memory_object(temp_obj, smt_object)
            return response.response_code
        else:
            request = Request(self.SMT_GET_BY_COUNTER, (smt_object, counter, timeout, data_info_object))
            self._connection.send(dumps(request))
            response = loads(self._connection.receive(self.BUFFER_SIZE))
            temp_obj, temp_data = response.response_object
            self._copy_shared_memory_object(temp_obj, smt_object)
            self._copy_shared_memory_object(temp_data, data_info_object)
            return response.response_code

    def publish(self, smt_object):
        request = Request(self.SMT_PUBLISH, smt_object)
        self._connection.send(dumps(request))
        response = loads(self._connection.receive(self.BUFFER_SIZE))
        return response.response_code

    def send(self, smt_object):
        request = Request(self.SMT_PUBLISH, smt_object)
        self._connection.send(dumps(request))
        response = loads(self._connection.receive(self.BUFFER_SIZE))
        return response.response_code

    def latestRx(self, smt_object, data_info_object=None):
        if data_info_object is None:
            request = Request(self.SMT_GET_LATEST, smt_object)
            self._connection.send(dumps(request))
            response = loads(self._connection.receive(self.BUFFER_SIZE))
            temp_obj = response.response_object
            self._copy_shared_memory_object(temp_obj, smt_object)
            return response.response_code
        else:
            request = Request(self.SMT_GET_LATEST, (smt_object, data_info_object))
            self._connection.send(dumps(request))
            response = loads(self._connection.receive(self.BUFFER_SIZE))
            temp_obj, temp_data = response.response_object
            self._copy_shared_memory_object(temp_obj, smt_object)
            self._copy_shared_memory_object(temp_data, data_info_object)
            return response.response_code

    def getLatest(self, smt_object, data_info_object=None):
        if data_info_object is None:
            request = Request(self.SMT_GET_LATEST, smt_object)
            self._connection.send(dumps(request))
            response = loads(self._connection.receive(self.BUFFER_SIZE))
            temp_obj = response.response_object
            self._copy_shared_memory_object(temp_obj, smt_object)
            return response.response_code
        else:
            request = Request(self.SMT_GET_LATEST, (smt_object, data_info_object))
            self._connection.send(dumps(request))
            response = loads(self._connection.receive(self.BUFFER_SIZE))
            temp_obj, temp_data = response.response_object
            self._copy_shared_memory_object(temp_obj, smt_object)
            self._copy_shared_memory_object(temp_data, data_info_object)
            return response.response_code

    def _copy_shared_memory_object(self, source_object, dest_object):
        class_variables = [attr for attr in dir(dest_object) if not callable(getattr(dest_object, attr)) and not attr.startswith("__")]
        for variable in class_variables:
            setattr(dest_object, variable, getattr(source_object, variable))

    def __del__(self):
        request = Request(self.EXIT)
        self._connection.send(dumps(request))
