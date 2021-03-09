import pickle
from .comm_device import CommDeviceInterface


class UDPConnection(CommDeviceInterface):

    def __init__(self, udp_connection):
        self._udp_connection = udp_connection
        self._address = tuple()
        super().__init__()

    def send(self, message):
        self._udp_connection.sendto(pickle.dumps(message), self._address)

    def receive(self):
        self._udp_connection.settimeout(self._timeout)
        packet, self._address = self._udp_connection.recvfrom(self._buffer_size)
        self._udp_connection.settimeout(None)
        return pickle.loads(packet)

    def __del__(self):
        self._udp_connection.close()
