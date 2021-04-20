from types import FunctionType
from numpy import ndarray
from .messages import Request


class SharedMemoryClient:
    """
    The SharedMemoryClient class, is responsible for sending messages
    to the remote server, in order to control his shared memory.
    The client and the server are talking in unique protocol, which contains
    Request and Response structures. Every request has its request code.
    """
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

    def __init__(self, connection):
        self._connection = connection

    def SMT_Init(self):
        request = Request(self.SMT_INIT)
        self._connection.send(request)
        return self._connection.receive().response_code

    def SMT_Version(self):
        request = Request(self.SMT_VERSION)
        self._connection.send(request)
        return self._connection.receive().response_object

    def SMT_CreateTopic(self, topic_name, max_data_size, history_depth, cells_count):
        request = Request(self.SMT_CREATE_TOPIC, (topic_name, max_data_size, history_depth, cells_count))
        self._connection.send(request)
        f_code = compile(f'def get_topic(self): return(GenericTopic(self, "{topic_name}")) ', "<GenericTopic>", "exec")
        f_func = FunctionType(f_code.co_consts[0], globals(), "get_topic")
        setattr(SharedMemoryClient, topic_name, f_func)
        return self._connection.receive().response_code

    def SMT_CreateTopic(self, topic_name):
        request = Request(self.SMT_CREATE_TOPIC, (topic_name, ))
        self._connection.send(request)
        f_code = compile(f'def get_topic(self): return(GenericTopic(self, "{topic_name}")) ', "<GenericTopic>", "exec")
        f_func = FunctionType(f_code.co_consts[0], globals(), "get_topic")
        setattr(SharedMemoryClient, topic_name, f_func)
        return self._connection.receive().response_code

    def SMT_GetPublishCount(self, topic_name):
        request = Request(self.SMT_GET_PUBLISH_COUNT, topic_name)
        self._connection.send(request)
        return self._connection.receive().response_object

    def SMT_ClearHistory(self, topic_name):
        request = Request(self.SMT_CLEAR_HISTORY, topic_name)
        self._connection.send(request)
        return self._connection.receive().response_code

    def getOldest(self, smt_object, topic_name, data_info_object=None):
        if data_info_object is None:
            request = Request(self.SMT_GET_OLDEST, (smt_object, topic_name))
        else:
            request = Request(self.SMT_GET_OLDEST, (smt_object, data_info_object, topic_name))
        self._connection.send(request)
        response = self._connection.receive()
        if data_info_object is not None:
            temp_obj, temp_data = response.response_object
        else:
            temp_obj = response.response_object
        self._copy_shared_memory_object(temp_obj, smt_object)
        if data_info_object is not None:
            self._copy_shared_memory_object(temp_data, data_info_object)
        return response.response_code

    def getByCounter(self, smt_object, counter, timeout, topic_name, data_info_object=None):
        if data_info_object is None:
            request = Request(self.SMT_GET_BY_COUNTER, (smt_object, counter, timeout, topic_name))
        else:
            request = Request(self.SMT_GET_BY_COUNTER, (smt_object, counter, timeout, data_info_object, topic_name))
        self._connection.send(request)
        response = self._connection.receive()
        if data_info_object is not None:
            temp_obj, temp_data = response.response_object
        else:
            temp_obj = response.response_object
        self._copy_shared_memory_object(temp_obj, smt_object)
        if data_info_object is not None:
            self._copy_shared_memory_object(temp_data, data_info_object)
        return response.response_code

    def publish(self, smt_object, topic_name):
        request = Request(self.SMT_PUBLISH, (smt_object, topic_name))
        self._connection.send(request)
        response = self._connection.receive()
        return response.response_code

    def getLatest(self, smt_object, topic_name, data_info_object=None):
        if data_info_object is None:
            request = Request(self.SMT_GET_LATEST, (smt_object, topic_name))
        else:
            request = Request(self.SMT_GET_LATEST, (smt_object, data_info_object, topic_name))
        self._connection.send(request)
        response = self._connection.receive()
        if data_info_object is not None:
            temp_obj, temp_data = response.response_object
        else:
            temp_obj = response.response_object
        self._copy_shared_memory_object(temp_obj, smt_object)
        if data_info_object is not None:
            self._copy_shared_memory_object(temp_data, data_info_object)
        return response.response_code

    def _copy_shared_memory_object(self, source_object, dest_object):
        class_variables = [attr for attr in dir(dest_object) if
                           not callable(getattr(dest_object, attr)) and not attr.startswith("__")]
        for variable in class_variables:
            attribute = getattr(source_object, variable)
            if type(attribute) == ndarray and attribute.dtype == 'int8':
                attribute = attribute.tolist()
                self._convert_to_char_list(attribute)
            elif type(attribute) == ndarray:
                attribute = attribute.tolist()
            setattr(dest_object, variable, attribute)

    def _convert_to_char_list(self, lst):
        if type(lst[0]) == list:
            for i in range(len(lst)):
                for j in range(len(lst[i])):
                    lst[i][j] = chr(lst[i][j])
        else:
            for i in range(len(lst)):
                lst[i] = chr(lst[i])

    def __del__(self):
        request = Request(self.EXIT)
        self._connection.send(request)
        self._connection.__del__()


class GenericTopic:
    def __init__(self, shared_memory_client, topic_name):
        self._topic_name = topic_name
        self._shared_memory_client = shared_memory_client

    def __call__(self):
        return self

    def getOldest(self, smt_object, data_info_object=None):
        return self._shared_memory_client.getOldest(smt_object, self._topic_name, data_info_object)

    def getByCounter(self, smt_object, counter, timeout, data_info_object=None):
        return self._shared_memory_client.getByCounter(smt_object, counter, timeout, self._topic_name, data_info_object)

    def publish(self, smt_object):
        return self._shared_memory_client.publish(smt_object, self._topic_name)

    def getLatest(self, smt_object, data_info_object=None):
        return self._shared_memory_client.getLatest(smt_object, self._topic_name, data_info_object)
