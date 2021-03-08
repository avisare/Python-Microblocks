import socket
from json_python import json_helper
from .tcp import TCPConnection
from .udp import UDPConnection


class ConnectionFactory:
    @staticmethod
    def get_connection():
        connection_mode = json_helper.JsonHelper.get_string("mode", "config.json")
        connection_type = json_helper.JsonHelper.get_string("connection_type", "config.json")
        if connection_mode == "Initiator" and connection_type == "TCP":
            return ConnectionFactory._get_TCP_initiator()
        elif connection_mode == "Initiator" and connection_type == "UDP":
            return ConnectionFactory._get_UDP_initiator()
        elif connection_mode == "Responder" and connection_type == "TCP":
            return ConnectionFactory._get_TCP_responder()
        elif connection_mode == "Responder" and connection_type == "TCP":
            return ConnectionFactory._get_UDP_responder()

    @staticmethod
    def _get_TCP_initiator():
        remote_ip = json_helper.JsonHelper.get_string("responder_ip", "config.json")
        remote_port = json_helper.JsonHelper.get_value("responder_port", "config.json")
        tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_connection.connect((remote_ip, remote_port))
        return TCPConnection(tcp_connection)

    @staticmethod
    def _get_UDP_initiator():
        remote_ip = json_helper.JsonHelper.get_string("responder_ip", "config.json")
        remote_port = json_helper.JsonHelper.get_value("responder_port", "config.json")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return UDPConnection(udp_connection, remote_ip, remote_port)

    @staticmethod
    def _get_TCP_responder():
        local_ip = json_helper.JsonHelper.get_string("responder_ip", "config.json")
        local_port = json_helper.JsonHelper.get_value("responder_port", "config.json")
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((local_ip, local_port))
        tcp_socket.listen()
        tcp_connection, address = tcp_socket.accept()
        return TCPConnection(tcp_connection)

    @staticmethod
    def _get_UDP_responder():
        local_ip = json_helper.JsonHelper.get_string("responder_ip", "config.json")
        local_port = json_helper.JsonHelper.get_value("responder_port", "config.json")
        destination_ip = json_helper.JsonHelper.get_string("initiator_ip", "config.json")
        destination_port = json_helper.JsonHelper.get_value("initiator_port", "config.json")
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.bind((local_ip, local_port))
        return UDPConnection(udp_connection, destination_ip, destination_port)
