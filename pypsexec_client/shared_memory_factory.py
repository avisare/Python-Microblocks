from shared_memory_client import SharedMemoryClient
from transportation_protocols.transportation_protocols_exception import ControlMethodNotFound
from json_python import JsonHelper
import SharedMemoryWrapper


def getSharedMemory():
    control_method = JsonHelper.get_string("control", "config.json")
    if control_method == "remote":
        return SharedMemoryClient()
    elif control_method == "local":
        return SharedMemoryWrapper
    else:
        raise ControlMethodNotFound(control_method)


def initialize_shared_memory(shared_memory_object):
    shared_memory_object.SMT_Init()
    topics_to_init = JsonHelper.get_value("topics", "config.json")
    for topic in topics_to_init:
        topic_info = JsonHelper.get_value(topic, "config.json")
        shared_memory_object.SMT_CreateTopic(topic, topic_info["max_data_size"], topic_info["history_depth"], topic_info["cells_count"])
