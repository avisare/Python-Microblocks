from .tcp_device import TCPDevice
from datetime import time


class TCPServer(TCPDevice):
    def __init__(self, tcp_connection, timeout: "time", buffer_size_bytes: "int", local_port: "int"):
        super().__init__(tcp_connection, timeout, buffer_size_bytes)

    def accept(self):
        connection, address = self._tcp_connection.accept()
        self.set_connection(connection)
        return connection

    def send_to_client(self, message, tcp_connection):
        self.send(message, tcp_connection)

    def receive_from_client(self, tcp_connection, buffer_size_bytes=None, timeout_seconds=None):
        return self.receive(buffer_size_bytes, timeout_seconds, tcp_connection)
