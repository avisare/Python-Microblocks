from .tcp_device import TCPDevice
from datetime import time


class TCPClient(TCPDevice):
    def __init__(self, tcp_connection, timeout: "time", buffer_size_bytes: "int", remote_ip: "str", remote_port: "int"):
        super().__init__(tcp_connection, timeout, buffer_size_bytes)
        self._remote_ip = remote_ip
        self._remote_port = remote_port

    def connect(self):
        self._tcp_connection.connect((self._remote_ip, self._remote_port))