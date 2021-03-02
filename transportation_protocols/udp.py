import socket
import pickle
from CommDevice import CommDeviceInterface


class UDP_Connection(CommDeviceInterface):

    def __init__(self, udp_connection):
        self._udp_connection = udp_connection

    def send(self, message):
        self._udp_connection.sendto(pickle.dumps(message), (self._destination_ip, self._destination_port))

    def receive(self, buffer_size: 'int', timeout: 'float' = None):
        self._udp_connection.settimeout(timeout)
        packet, self._address = self._udp_connection.recvfrom(buffer_size)
        self._udp_connection.settimeout(None)
        packet = pickle.loads(packet)
        return packet

    def __del__(self):
        self._udp_connection.close()


def is_number_argument(argument):
    return argument.isnumeric()



