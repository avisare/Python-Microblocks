import pickle
from .comm_device import CommDeviceInterface


class TCPStrictConnection(CommDeviceInterface):
    def __init__(self, tcp_connection):
        super().__init__()
        self._tcp_connection = tcp_connection

    def send(self, message):
        self._tcp_connection.sendall(pickle.dumps(message))

    def receive(self):
        self._tcp_connection.settimeout(self._timeout)
        packet = self._tcp_connection.recv(self._buffer_size)
        packet = pickle.loads(packet)
        self._tcp_connection.settimeout(None)
        return packet

    def __del__(self):
        self._tcp_connection.close()


