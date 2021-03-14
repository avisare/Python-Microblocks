import socket
from json_config_singleton import JsonConfigSingleton
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
        connection_mode = JsonConfigSingleton().json_dictionary["mode"]
        connection_type = JsonConfigSingleton().json_dictionary["connection_type"]
        timeout_seconds = JsonConfigSingleton().json_dictionary["timeout_seconds"]
        buffer_size_bytes = JsonConfigSingleton().json_dictionary["buffer_size_bytes"]
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
        local_ip = "0.0.0.0"
        local_port = JsonConfigSingleton().json_dictionary["responder_port"]
        if type(local_port) != int:
            raise ArgumentMustBeInteger("port address")
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((local_ip, local_port))
        tcp_socket.listen()
        tcp_server = TCPServer(tcp_socket, timeout_seconds, buffer_size_bytes, local_port)
        tcp_connection, address = tcp_socket.accept()
        tcp_server.set_connection(tcp_connection)
        return tcp_server

    @staticmethod
    def _get_TCP_client(timeout_seconds, buffer_size_bytes):
        remote_ip = JsonConfigSingleton().json_dictionary["responder_ip"]
        remote_port = JsonConfigSingleton().json_dictionary["responder_port"]
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
        destination_ip = JsonConfigSingleton().json_dictionary["responder_ip"]
        destination_port = JsonConfigSingleton().json_dictionary["responder_port"]
        local_ip = "0.0.0.0"
        local_port = JsonConfigSingleton().json_dictionary["initiator_port"]
        if type(destination_port) != int or type(local_port) != int:
            raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((local_ip, local_port))
        return UDPStrictConnection(udp_connection, destination_ip, destination_port, timeout_seconds, buffer_size_bytes)

    @staticmethod
    def _get_UDP_responder(timeout_seconds, buffer_size_bytes):
        local_ip = "0.0.0.0"
        local_port = JsonConfigSingleton().json_dictionary["responder_port"]
        if type(local_port) != int:
            raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((local_ip, local_port))
        return UDPResponderConnection(udp_connection, timeout_seconds, buffer_size_bytes)

    @staticmethod
    def _get_UDP_initiator(timeout_seconds, buffer_size_bytes):
        remote_ip = JsonConfigSingleton().json_dictionary["responder_ip"]
        remote_port = JsonConfigSingleton().json_dictionary["responder_port"]
        if type(remote_port) != int:
            raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((remote_ip, remote_port))
        return UDPInitiatorConnection(udp_connection, remote_ip, remote_port, timeout_seconds, buffer_size_bytes)
