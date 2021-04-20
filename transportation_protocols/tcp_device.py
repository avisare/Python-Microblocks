import pickle
from datetime import time
from .comm_device import CommDeviceInterface


class TCPDevice(CommDeviceInterface):
    """
    This class is representing TCP Device, which is implement basic
    function like send and receive with tcp socket.
    The class make sure that every TCP Device that inherited from her,
    will have receive and send functions.
    """
    def __init__(self, tcp_connection, timeout: "time", buffer_size_bytes: "int"):
        super().__init__(timeout, buffer_size_bytes)
        self._tcp_connection = tcp_connection

    def get_connection(self):
        return self._tcp_connection

    def set_connection(self, tcp_connection):
        self._tcp_connection = tcp_connection

    def send(self, message, tcp_connection=None):
        self._tcp_connection.sendall(pickle.dumps(message))

    def receive(self, buffer_size_bytes=None, timeout_seconds=None, tcp_connection=None):
        if timeout_seconds is None:
            timeout_seconds = self._timeout_seconds
        if buffer_size_bytes is None:
            buffer_size_bytes = self._buffer_size_bytes
        if tcp_connection is None:
            tcp_connection = self._tcp_connection
        tcp_connection.settimeout(timeout_seconds)
        packet = tcp_connection.recv(buffer_size_bytes)
        packet = pickle.loads(packet)
        tcp_connection.settimeout(None)
        return packet

    def __del__(self):
        self._tcp_connection.close()

