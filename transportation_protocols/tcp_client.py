from .tcp_device import TCPDevice
from datetime import time


class TCPClient(TCPDevice):
    """
    This class is representing TCP client, which means the connection who
    start the conversation between the sever and the client.
    The client have the same functions as TCP Device class, and the connect function
    which connect the client to the server
    """
    def __init__(self, tcp_connection, timeout: "time", buffer_size_bytes: "int", remote_ip: "str", remote_port: "int"):
        super().__init__(tcp_connection, timeout, buffer_size_bytes)
        self._remote_ip = remote_ip
        self._remote_port = remote_port

    def connect(self):
        self._tcp_connection.connect((self._remote_ip, self._remote_port))

    def send(self, message, tcp_connection=None):
        super().send(message)

    def receive(self, buffer_size_bytes=None, timeout_seconds=None, tcp_connection=None):
        return super().receive(buffer_size_bytes, timeout_seconds, tcp_connection)
