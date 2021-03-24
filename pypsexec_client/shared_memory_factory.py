from .shared_memory_client import SharedMemoryClient
from transportation_protocols.transportation_protocols_exception import ControlMethodNotFound
from transportation_protocols.connection_factory import ConnectionFactory
from parse_config import config_dictionary
import SharedMemoryWrapper


def get_shared_memory():
    control_method = config_dictionary["control"]
    if control_method == "remote":
        return SharedMemoryClient(ConnectionFactory.get_connection())
    elif control_method == "local":
        return SharedMemoryWrapper
    else:
        raise ControlMethodNotFound(control_method)


def initialize_shared_memory(shared_memory_object):
    shared_memory_object.SMT_Init()
    topics_to_init = config_dictionary["topics"]
    for topic in topics_to_init:
        topic_info = config_dictionary[topic]
        shared_memory_object.SMT_CreateTopic(topic, topic_info["max_data_size"], topic_info["history_depth"], topic_info["cells_count"])
