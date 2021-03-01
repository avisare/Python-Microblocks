import socket


class UDP_Connection:

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
            self._udp_connection.sendto(message.encode('utf-8'), (self._destination_ip, self._destination_port))
        else:
            self._udp_connection.sendto(message.encode('utf-8'), self._address)

    def receive(self, buffer_size, timeout=None):
        self._udp_connection.settimeout(timeout)
        print(f"Wating for message from port {self._destination_port}")
        packet, self._address = self._udp_connection.recvfrom(buffer_size)
        self._udp_connection.settimeout(None)
        packet = packet.decode('utf-8')
        return packet

    def __del__(self):
        self._udp_connection.close()


def is_number_argument(argument):
    return argument.isnumeric()



