import socket
from json_python.json_helper import JsonHelper
from .tcp import TCPConnection
from .udp import UDPConnection
from .transportation_protocols_exception import FunctionNotFound, ArgumentMustBeInteger


class ConnectionFactory:
    @staticmethod
    def get_connection():
        connection_mode = JsonHelper.get_string("mode", "config.json")
        connection_type = JsonHelper.get_string("connection_type", "config.json")
        function_name = f"_get_{connection_type}_{connection_mode}"
        if function_name in dir(ConnectionFactory):
            return getattr(ConnectionFactory, function_name)()
        else:
            raise FunctionNotFound(connection_mode, connection_type)

    @staticmethod
    def _get_TCP_initiator():
        remote_ip = JsonHelper.get_string("responder_ip", "config.json")
        remote_port = JsonHelper.get_value("responder_port", "config.json")
        if type(remote_port) != int:
            raise ArgumentMustBeInteger("port address")
        tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_connection.connect((remote_ip, remote_port))
        return TCPConnection(tcp_connection)

    @staticmethod
    def _get_UDP_initiator():
        remote_ip = JsonHelper.get_string("responder_ip", "config.json")
        remote_port = JsonHelper.get_value("responder_port", "config.json")
        if type(remote_port) != int:
            raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return UDPConnection(udp_connection, remote_ip, remote_port)

    @staticmethod
    def _get_TCP_responder():
        local_ip = JsonHelper.get_string("responder_ip", "config.json")
        local_port = JsonHelper.get_value("responder_port", "config.json")
        if type(local_port) != int:
            raise ArgumentMustBeInteger("port address")
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((local_ip, local_port))
        tcp_socket.listen()
        # how should the application know, what to send for every connection
        tcp_connection, address = tcp_socket.accept()
        return TCPConnection(tcp_connection)

    @staticmethod
    def _get_UDP_responder():
        local_ip = JsonHelper.get_string("responder_ip", "config.json")
        local_port = JsonHelper.get_value("responder_port", "config.json")
        if type(local_port) != int:
            raise ArgumentMustBeInteger("port address")
        destination_ip = JsonHelper.get_string("initiator_ip", "config.json")
        destination_port = JsonHelper.get_value("initiator_port", "config.json")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((local_ip, local_port))
        return UDPConnection(udp_connection, destination_ip, destination_port)

    @staticmethod
    def _get_TCP_strict():
        pass

    @staticmethod
    def get_UDP_strict():
        pass