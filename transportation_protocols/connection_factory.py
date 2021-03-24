import socket
from .udp_device import UDPDevice
from .tcp_device import TCPDevice
from .tcp_client import TCPClient
from .tcp_server import TCPServer
from .udp_initiator import UDPInitiatorConnection
from .udp_responder import UDPResponderConnection
from .udp_strict import UDPStrictConnection
from .transportation_protocols_exception import FunctionNotFound, ArgumentMustBeInteger


class ConnectionFactory:
    @staticmethod
    def get_connection(mode: "str", connection_type: "str", timeout_seconds: "int", buffer_size_bytes: "int", responder_port=None, responder_ip=None, local_port=None):
        """
            function return the proper connection according to the parameters
            :param mode: the mode of the connection, server/client/responder/initator/strict
            :param connection_type: the connection type TCP/UDP
            :param timeout_seconds: the timeout until receive function is quit
            :param buffer_size_bytes: the buffer size the receive function get
            :param responder_port: the responder port
            :param responder_ip: the responder ip
            :param local_port: the local port
            :type mode: str
            :type connection_type: str
            :type timeout_seconds: int or time struct
            :type buffer_size_bytes: int
            :type responder_port: int
            :type responder_ip: str
            :type local_port: int
            :return The appropriate connection according to the parameters
            :rtype: CommDevice
        """
        if mode == "":
            function_name = f"_get_{connection_type}"
        else:
            function_name = f"_get_{connection_type}_{mode}"
        if function_name in dir(ConnectionFactory):
            return getattr(ConnectionFactory, function_name)(timeout_seconds, buffer_size_bytes, responder_port, responder_ip, local_port)
        else:
            raise FunctionNotFound(mode, connection_type)

    @staticmethod
    def _get_TCP_server(timeout_seconds, buffer_size_bytes, server_port, responder_ip=None, local_port=None):
        local_ip = "0.0.0.0"
        print(server_port)
        if server_port is None:
            raise TypeError("_get_TCP_server missing one required argument: server_port")
        if type(server_port) != int:
            if not server_port.isnumeric():
                raise ArgumentMustBeInteger("port address")
            else:
                server_port = int(server_port)
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((local_ip, server_port))
        tcp_socket.listen()
        tcp_server = TCPServer(tcp_socket, timeout_seconds, buffer_size_bytes, server_port)
        tcp_server.accept()
        return tcp_server

    @staticmethod
    def _get_TCP_client(timeout_seconds, buffer_size_bytes, server_port, server_ip, local_port=None):
        if server_port is None or server_ip is None:
            raise TypeError("_get_TCP_server missing one or more required arguments: server_port/server_ip")
        if type(server_port) != int:
            if type(server_port) == str and server_port.isnumeric():
                server_port = int(server_port)
            else:
                raise ArgumentMustBeInteger("port address")
        tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client = TCPClient(tcp_connection, timeout_seconds, buffer_size_bytes, server_ip, server_port)
        tcp_client.connect()
        return tcp_client

    @staticmethod
    def _get_TCP(timeout_seconds, buffer_size_bytes, responder_port=None, responder_ip=None, local_port=None):
        tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return TCPDevice(tcp_connection, timeout_seconds, buffer_size_bytes)

    @staticmethod
    def _get_UDP(timeout_seconds, buffer_size_bytes, responder_port=None, responder_ip=None, local_port=None):
        return UDPDevice(timeout_seconds, buffer_size_bytes)

    @staticmethod
    def _get_UDP_strict(timeout_seconds, buffer_size_bytes, destination_port, destination_ip, local_port):
        local_ip = "0.0.0.0"
        if destination_port is None or destination_ip is None or local_port is None:
            raise TypeError("_get_TCP_server missing one or more required arguments: destination_port/destination_ip/local_port")
        if type(destination_port) != int:
            if type(destination_port) == str and destination_port.isnumeric():
                destination_port = int(destination_port)
            else:
                raise ArgumentMustBeInteger("destination port address")
        if type(local_port) != int:
            if type(local_port) == str and local_port.isnumeric():
                local_port = int(local_port)
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((local_ip, local_port))
        return UDPStrictConnection(udp_connection, destination_ip, destination_port, timeout_seconds, buffer_size_bytes)

    @staticmethod
    def _get_UDP_responder(timeout_seconds, buffer_size_bytes, server_port, responder_ip=None, local_port=None):
        local_ip = "0.0.0.0"
        if server_port is None:
            raise TypeError("_get_TCP_server missing one required argument: server_port")
        if type(server_port) != int:
            if type(server_port) == str and server_port.isnumeric():
                server_port = int(server_port)
            else:
                raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((local_ip, server_port))
        return UDPResponderConnection(udp_connection, timeout_seconds, buffer_size_bytes)

    @staticmethod
    def _get_UDP_initiator(timeout_seconds, buffer_size_bytes, server_port, server_ip, local_port=None):
        if server_port is None or server_ip is None:
            raise TypeError("_get_TCP_server missing one or more required arguments: server_port/server_ip")
        if type(server_port) != int:
            if type(server_port) == str and server_port.isnumeric():
                server_port = int(server_port)
            else:
                raise ArgumentMustBeInteger("port address")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((server_ip, server_port))
        return UDPInitiatorConnection(udp_connection, server_ip, server_port, timeout_seconds, buffer_size_bytes)
