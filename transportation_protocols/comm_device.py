from abc import ABCMeta
from datetime import time
from .transportation_protocols_exception import ArgumentMustBeInteger


class CommDeviceInterface(metaclass=ABCMeta):
    """
    The CommDeviceInterface class, is the base class of all communication devices.
    every communication device need to implement the send and receive methods.
    The init function is just initialize the timeout and the buffer size pparameters
    that are common for any connection type.
    """
    SECONDS_IN_HOUR = 3600

    def __init__(self, timeout: "time", buffer_size_bytes: "int"):
        if type(buffer_size_bytes) != int:
            if type(buffer_size_bytes) == str and buffer_size_bytes.isnumeric():
                buffer_size_bytes = int(buffer_size_bytes)
            else:
                raise ArgumentMustBeInteger("buffer size")
        if type(timeout) == time:
            self._timeout_seconds = timeout.hour * self.SECONDS_IN_HOUR + timeout.minute * 60 + timeout.second
        else:
            if type(timeout) != int:
                if type(timeout) == str and timeout.isnumeric():
                    timeout = int(timeout)
                else:
                    raise ArgumentMustBeInteger("timeout seconds")
            self._timeout_seconds = timeout
        self._buffer_size_bytes = buffer_size_bytes

    def send(self, message):
        pass

    def receive(self, timeout_seconds: "int" = None,  buffer_size_bytes: "int" = None):
        pass
