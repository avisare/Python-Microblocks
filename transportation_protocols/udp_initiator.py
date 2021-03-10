import pickle
from datetime import time
from .comm_device import CommDeviceInterface


class UDPInitiatorConnection(CommDeviceInterface):

    def __init__(self, udp_connection, destination_ip, destination_port, timeout: 'time', buffer_size_bytes: 'int'):
        super().__init__(timeout, buffer_size_bytes)
        self._udp_connection = udp_connection
        self._destination_ip = destination_ip
        self._destination_port = destination_port

    def send(self, message):
        self._udp_connection.sendto(pickle.dumps(message), (self._destination_ip, self._destination_port))

    def receive(self, timeout_seconds: "int" = None, buffer_size_bytes: "int" = None):
        pass

    def __del__(self):
        self._udp_connection.close()
