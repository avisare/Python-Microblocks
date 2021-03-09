import pickle
from .comm_device import CommDeviceInterface


class UDPResponderConnection(CommDeviceInterface):
    def __init__(self, udp_connection):
        self._udp_connection = udp_connection
        super().__init__()

    def send(self, message):
        pass

    def receive(self):
        self._udp_connection.settimeout(self._timeout)
        packet, address = self._udp_connection.recvfrom(self._buffer_size)
        self._udp_connection.settimeout(None)
        return pickle.loads(packet)

    def __del__(self):
        self._udp_connection.close()
