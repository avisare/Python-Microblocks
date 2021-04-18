from .tcp_device import TCPDevice
from datetime import time


class TCPServer(TCPDevice):
    """
    This class represent TCP Server, which means the side who listen
    to transportation on specific port and ip address.
    This class have the same functions  as the TCP Device class and the accept
    function which accept client.
    """
    def __init__(self, tcp_connection, timeout: "time", buffer_size_bytes: "int", local_port: "int"):
        super().__init__(tcp_connection, timeout, buffer_size_bytes)

    def accept(self):
        connection, address = self._tcp_connection.accept()
        self.set_connection(connection)
        return connection

    def send(self, message, tcp_connection=None):
        super().send(message, self._tcp_connection)

    def receive(self, tcp_connection=None, buffer_size_bytes=None, timeout_seconds=None):
        return super().receive(buffer_size_bytes, timeout_seconds, tcp_connection)
