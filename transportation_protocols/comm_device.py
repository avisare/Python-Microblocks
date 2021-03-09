import abc
from datetime import time
from .transportation_protocols_exception import ArgumentMustBeInteger


class CommDeviceInterface(metaclass=abc.ABCMeta):

    SECONDS 
    def __init__(self, timeout: "time", buffer_size: "int"):
        self._timeout = timeout
        self._buffer_size_seconds = buffer_size.hour *

    @abc.abstractmethod
    def send(self, message):
        pass

    @abc.abstractmethod
    def receive(self):
        pass
