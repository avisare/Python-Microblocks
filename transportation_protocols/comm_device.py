from abc import ABCMeta
from datetime import time
from .transportation_protocols_exception import ArgumentMustBeInteger


class CommDeviceInterface(metaclass=ABCMeta):

    SECONDS_IN_HOUR = 3600

    def __init__(self, timeout: "time", buffer_size_bytes: "int"):
        if type(buffer_size_bytes) != int:
            raise ArgumentMustBeInteger("buffer size")
        if type(timeout) == time:
            self._timeout_seconds = timeout.hour * self.SECONDS_IN_HOUR + timeout.minute * 60 + timeout.second
        else:
            self._timeout_seconds = timeout
        self._buffer_size_bytes = buffer_size_bytes

    def send(self, message):
        pass

    def receive(self, timeout_seconds: "int" = None,  buffer_size_bytes: "int" = None):
        pass
