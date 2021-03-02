import pickle
from CommDevice import CommDeviceInterface


class TCP_Connection(CommDeviceInterface):
    def __init__(self, tcp_connection):
        self._tcp_connection = tcp_connection

    def send(self, message):
        self._tcp_connection.sendall(pickle.loads(message))

    def receive(self, buffer_size: 'int', timeout: 'float' = None):
        self._tcp_connection.settimeout(timeout)
        packet = self._tcp_connection.recv(buffer_size)
        packet = pickle.loads(packet)
        self._tcp_connection.settimeout(None)
        return packet

    def __del__(self):
        self._tcp_connection.close()


def is_number_argument(argument):
    return argument.isnumeric()

