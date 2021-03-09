import pickle
from .comm_device import CommDeviceInterface


class TCPStrictConnection(CommDeviceInterface):
    def __init__(self, tcp_connection, destination_ip, destination_port):
        self._tcp_connection = tcp_connection
        self._destination_ip = destination_ip
        self._destination_port = destination_port
        super().__init__()

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