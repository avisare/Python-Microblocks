import socket
from json_python.json_helper import JsonHelper
from .tcp_device import TCPDevice
from .tcp_client import TCPClient
from .tcp_server import TCPServer
from .udp_initiator import UDPInitiatorConnection
from .udp_responder import UDPResponderConnection
from .udp_strict import UDPStrictConnection
from .transportation_protocols_exception import FunctionNotFound, ArgumentMustBeInteger


class ConnectionFactory:
    @staticmethod
    def get_connection():
        connection_mode = JsonHelper.get_string("mode", "config.json")
        connection_type = JsonHelper.get_string("connection_type", "config.json")
        timeout_seconds = JsonHelper.get_value("timeout_seconds", "config.json")
        buffer_size_bytes = JsonHelper.get_value("buffer_size_bytes", "config.json")
        if connection_mode == "":
            function_name = f"_get_{connection_type}"
        else:
            function_name = f"_get_{connection_type}_{connection_mode}"
        if function_name in dir(ConnectionFactory):
            return getattr(ConnectionFactory, function_name)(timeout_seconds, buffer_size_bytes)
        else:
            raise FunctionNotFound(connection_mode, connection_type)

    @staticmethod
    def _get_TCP_server(timeout_seconds, buffer_size_bytes):
        local_ip = JsonHelper.get_string("responder_ip", "config.json")
        local_port = JsonHelper.get_value("responder_port", "config.json")
        if type(local_port) != int:
            raise ArgumentMustBeInteger("port address")
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((local_ip, local_port))
        tcp_socket.listen()
        tcp_server = TCPServer(tcp_socket, timeout_seconds, buffer_size_bytes)
        tcp_server.accept()
        return tcp_server

    @staticmethod
    def _get_TCP_client(timeout_seconds, buffer_size_bytes):
        remote_ip = JsonHelper.get_string("responder_ip", "config.json")
        remote_port = JsonHelper.get_value("responder_port", "config.json")
        if type(remote_port) != int:
            raise ArgumentMustBeInteger("port address")
        tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client = TCPClient(tcp_connection, timeout_seconds, buffer_size_bytes, remote_ip, remote_port)
        tcp_client.connect()
        return tcp_client

    @staticmethod
    def _get_TCP(timeout_seconds, buffer_size_bytes):
        tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return TCPDevice(tcp_connection, timeout_seconds, buffer_size_bytes)

    @staticmethod
    def _get_UDP_strict(timeout_seconds, buffer_size_bytes):
        destination_ip = JsonHelper.get_string("responder_ip", "config.json")
        destination_port = JsonHelper.get_value("responder_port", "config.json")
        if type(destination_port) != int:
            raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return UDPStrictConnection(udp_connection, destination_ip, destination_port, timeout_seconds, buffer_size_bytes)

    @staticmethod
    def _get_UDP_server(timeout_seconds, buffer_size_bytes):
        remote_ip = JsonHelper.get_string("responder_ip", "config.json")
        remote_port = JsonHelper.get_value("responder_port", "config.json")
        if type(remote_port) != int:
            raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind(("127.0.0.1", remote_port))
        return UDPStrictConnection(udp_connection, remote_ip, remote_port, timeout_seconds, buffer_size_bytes)

    @staticmethod
    def _get_UDP_responder(timeout_seconds, buffer_size_bytes):
        local_ip = JsonHelper.get_string("responder_ip", "config.json")
        local_port = JsonHelper.get_value("responder_port", "config.json")
        if type(local_port) != int:
            raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((local_ip, local_port))
        return UDPResponderConnection(udp_connection, timeout_seconds, buffer_size_bytes)

    @staticmethod
    def _get_UDP_initiator(timeout_seconds, buffer_size_bytes):
        remote_ip = JsonHelper.get_string("responder_ip", "config.json")
        remote_port = JsonHelper.get_value("responder_port", "config.json")
        if type(remote_port) != int:
            raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((remote_ip, remote_port))
        return UDPInitiatorConnection(udp_connection, remote_ip, remote_port, timeout_seconds, buffer_size_bytes)
