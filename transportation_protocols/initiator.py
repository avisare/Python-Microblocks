import socket
from tcp import TCP_Connection
from udp import UDP_Connection


class TCPInitiator(TCP_Connection):
    local_ip = "127.0.0.1"

    def __init__(self, remote_ip, remote_port):
        self._remote_ip = remote_ip
        self._remote_port = remote_port
        self._tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_connection.connect((self._remote_ip, self._remote_port))
        super().__init__(self._tcp_connection)


class UDPInitiator(UDP_Connection):
    def __init__(self, remote_ip, remote_port):
        self._remote_ip = remote_ip
        self._remote_port = remote_port
        self._udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        super().__init__(self._udp_connection)