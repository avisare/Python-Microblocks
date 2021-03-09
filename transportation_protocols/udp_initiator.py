import pickle
from .comm_device import CommDeviceInterface


class UDPInitiatorConnection(CommDeviceInterface):

    def __init__(self, udp_connection, destination_ip, destination_port):
        self._udp_connection = udp_connection
        self._destination_ip = destination_ip
        self._destination_port = destination_port
        super().__init__()

    def send(self, message):
        self._udp_connection.sendto(pickle.dumps(message), (self._destination_ip, self._destination_port))

    def receive(self):
        pass

    def __del__(self):
        self._udp_connection.close()
