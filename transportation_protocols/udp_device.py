from .comm_device import CommDeviceInterface
from datetime import time


class UDPDevice(CommDeviceInterface):
    """
    This class represent generic UDP connection.
    This is an abstract class, that make sure every child of here need to implement the send
    and receive functions
    """

    def __init__(self, timeout: 'time', buffer_size_bytes: 'int'):
        super().__init__(timeout, buffer_size_bytes)

    def send(self, message):
        pass

    def receive(self, timeout_seconds: "int" = None, buffer_size_bytes: "int" = None):
        pass
