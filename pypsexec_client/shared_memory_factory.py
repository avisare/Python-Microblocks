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