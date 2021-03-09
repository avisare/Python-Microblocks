import socket
from json_python.json_helper import JsonHelper
from .tcp_strict import TCPStrictConnection
from .udp_initiator import UDPInitiatorConnection
from .udp_responder import UDPResponderConnection
from .udp_strict import UDPStrictConnection
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
    def _get_TCP_strict_sender():
        remote_ip = JsonHelper.get_string("responder_ip", "config.json")
        remote_port = JsonHelper.get_value("responder_port", "config.json")
        if type(remote_port) != int:
            raise ArgumentMustBeInteger("port address")
        tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_connection.connect((remote_ip, remote_port))
        return TCPStrictConnection(tcp_connection)

    @staticmethod
    def _get_UDP_strict_sender():
        remote_ip = JsonHelper.get_string("responder_ip", "config.json")
        remote_port = JsonHelper.get_value("responder_port", "config.json")
        if type(remote_port) != int:
            raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return UDPStrictConnection(udp_connection, remote_ip, remote_port)

    @staticmethod
    def _get_TCP_strict_listener():
        local_ip = JsonHelper.get_string("responder_ip", "config.json")
        local_port = JsonHelper.get_value("responder_port", "config.json")
        if type(local_port) != int:
            raise ArgumentMustBeInteger("port address")
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((local_ip, local_port))
        tcp_socket.listen()
        tcp_connection, address = tcp_socket.accept()
        return TCPStrictConnection(tcp_connection)

    @staticmethod
    def _get_UDP_strict_listner():
        local_ip = JsonHelper.get_string("responder_ip", "config.json")
        local_port = JsonHelper.get_value("responder_port", "config.json")
        if type(local_port) != int:
            raise ArgumentMustBeInteger("port address")
        destination_ip = JsonHelper.get_string("initiator_ip", "config.json")
        destination_port = JsonHelper.get_value("initiator_port", "config.json")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((local_ip, local_port))
        return UDPStrictConnection(udp_connection, destination_ip, destination_port)

    @staticmethod
    def _get_UDP_responder():
        local_ip = JsonHelper.get_string("responder_ip", "config.json")
        local_port = JsonHelper.get_value("responder_port", "config.json")
        if type(local_port) != int:
            raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((local_ip, local_port))
        return UDPResponderConnection(udp_connection)

    @staticmethod
    def _get_UDP_initiator():
        remote_ip = JsonHelper.get_string("responder_ip", "config.json")
        remote_port = JsonHelper.get_value("responder_port", "config.json")
        if type(remote_port) != int:
            raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((remote_ip, remote_port))
        return UDPInitiatorConnection(udp_connection, remote_ip, remote_port)
