import pickle
from datetime import time
from .udp_device import UDPDevice


class UDPStrictConnection(UDPDevice):

    def __init__(self, udp_connection, destination_ip, destination_port, timeout: 'time', buffer_size_bytes: 'int'):
        super().__init__(timeout, buffer_size_bytes)
        self._udp_connection = udp_connection
        self._destination_ip = destination_ip
        self._destination_port = destination_port

    def set_connection(self, udp_connection):
        self._udp_connection = udp_connection

    def get_connection(self):
        return self._udp_connection

    def send(self, message):
        self._udp_connection.sendto(pickle.dumps(message), (self._destination_ip, self._destination_port))

    def receive(self, timeout_seconds: "int" = None, buffer_size_bytes: "int" = None):
        if timeout_seconds is None:
            timeout_seconds = self._timeout_seconds
        if buffer_size_bytes is None:
            buffer_size_bytes = self._buffer_size_bytes
        self._udp_connection.settimeout(timeout_seconds)
        packet, address = self._udp_connection.recvfrom(buffer_size_bytes)
        self._udp_connection.settimeout(None)
        return pickle.loads(packet)

    def __del__(self):
        self._udp_connection.close()
