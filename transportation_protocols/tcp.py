import pickle
from datetime import time
from .comm_device import CommDeviceInterface


class TCPConnection(CommDeviceInterface):
    def __init__(self, tcp_connection, timeout: "time", buffer_size: "int"):
        super().__init__(timeout, buffer_size)
        self._tcp_connection = tcp_connection

    def send(self, message):
        self._tcp_connection.sendall(pickle.dumps(message))

    def receive(self, buffer_size_bytes=None, timeout_seconds=None):
        if timeout_seconds is None:
            timeout_seconds = self._timeout_seconds
        if buffer_size_bytes is None:
            buffer_size_bytes = self._buffer_size_bytes
        self._tcp_connection.settimeout(timeout_seconds)
        packet = self._tcp_connection.recv(buffer_size_bytes)
        packet = pickle.loads(packet)
        self._tcp_connection.settimeout(None)
        return packet

    def __del__(self):
        self._tcp_connection.close()


