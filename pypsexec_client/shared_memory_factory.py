from .shared_memory_client import SharedMemoryClient
from transportation_protocols.transportation_protocols_exception import ControlMethodNotFound
from transportation_protocols.connection_factory import ConnectionFactory
import parse_config
import SharedMemoryWrapper


def get_shared_memory(mode=None, connection_type=None, timeout_seconds=None, buffer_size_bytes=None, responder_port=None, responder_ip=None, local_port=None):
    control_method = parse_config.config_dictionary["control"]
    if control_method == "remote":
        return SharedMemoryClient(ConnectionFactory.get_connection(mode, connection_type, timeout_seconds, buffer_size_bytes, responder_port, responder_ip, local_port))
    elif control_method == "local":
        return SharedMemoryWrapper
    else:
        raise ControlMethodNotFound(control_method)


def initialize_shared_memory(shared_memory_object):
    shared_memory_object.SMT_Init()
    topics_to_init = parse_config.config_dictionary["topics"]
    for topic in topics_to_init:
        topic_info = parse_config.config_dictionary[topic]
        shared_memory_object.SMT_CreateTopic(topic, topic_info["max_data_size"], topic_info["history_depth"], topic_info["cells_count"])
