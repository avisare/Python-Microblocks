import socket
import json

class ConnectionFactory:
    def get_connection(self):
        with open("config.json", "r") as config_file:
            

    def get_TCP_initiator(self):
        self._remote_ip = remote_ip
        self._remote_port = remote_port
        self._tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_connection.connect((self._remote_ip, self._remote_port))