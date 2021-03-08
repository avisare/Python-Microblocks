import abc


class CommDeviceInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def send(self, message):
        pass

    @abc.abstractmethod
    def receive(self, buffer_size: 'int', timeout: 'float' = None):
        pass
