import socket
import pickle
from CommDevice import CommDeviceInterface


class UDP_Connection(CommDeviceInterface):

    local_ip = "127.0.0.1"

    def __init__(self, destination_port, is_client, destination_ip=local_ip):
        self._destination_ip = destination_ip
        self._destination_port = destination_port
        self._udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._is_client = is_client
        self._address = None
        if not self._is_client:
            self._udp_connection.bind((self._destination_ip, self._destination_port))

    def send(self, message):
        if self._is_client:
            if isinstance(message, str):
                self._udp_connection.sendto(message.encode('utf-8'), (self._destination_ip, self._destination_port))
            else:
                self._udp_connection.sendto(pickle.dumps(message), (self._destination_ip, self._destination_port))
        else:
            if isinstance(message, str):
                self._udp_connection.sendto(message.encode('utf-8'), self._address)
            else:
                self._udp_connection.sendto(pickle.dumps(message), self._address)

    def receive(self, buffer_size: 'int', timeout: 'float' = None):
        self._udp_connection.settimeout(timeout)
        packet, self._address = self._udp_connection.recvfrom(buffer_size)
        self._udp_connection.settimeout(None)
        try:
            packet = packet.decode('utf-8')
        except UnicodeDecodeError:
            packet = pickle.loads(packet)
        return packet

    def __del__(self):
        self._udp_connection.close()


def is_number_argument(argument):
    return argument.isnumeric()



