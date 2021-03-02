import socket
from udp import UDP_Connection
from tcp import TCP_Connection


class TCPResponder(TCP_Connection):
    def __init__(self, host_ip, host_port):
        self._host_ip = host_ip
        self._host_port = host_port
        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_socket.bind((self._host_ip, self._host_port))
        connection_socket.listen(1)
        self._tcp_connection, self._client_address = connection_socket.accept()
        super().__init__(self._tcp_connection)


class UDPResponder(UDP_Connection):
    def __init__(self, host_ip, host_port):
        self._host_ip = host_ip
        self._host_port = host_port
        self._udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._udp_connection.bind((self._host_ip, self._host_ip))
        super().__init__(self._udp_connection)