import abc
from json_python import json_helper
from .transportation_protocols_exception import ArgumentMustBeInteger


class CommDeviceInterface(metaclass=abc.ABCMeta):

    def __init__(self):
        self._timeout = json_helper.JsonHelper.get_value("timeout", "config.json")
        self._buffer_size = json_helper.JsonHelper.get_value("buffer_size", "config.json")
        if type(self._timeout) != int:
            raise ArgumentMustBeInteger("timeout")
        if type(self._buffer_size) != int:
            raise ArgumentMustBeInteger("buffer size")

    @abc.abstractmethod
    def send(self, message):
        pass

    @abc.abstractmethod
    def receive(self):
        pass
