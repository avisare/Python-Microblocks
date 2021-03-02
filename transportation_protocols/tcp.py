import socket
import pickle
from CommDevice import CommDeviceInterface


class TCP_Connection(CommDeviceInterface):

    local_ip = "127.0.0.1"
    
    def __init__(self, destination_port, is_client, destination_ip=local_ip):

        if is_client:
            self._destination_ip = destination_ip
            self._destination_port = destination_port
            self._tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._tcp_connection.connect((self._destination_ip, self._destination_port))
        else:
            
            connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection_socket.bind((self._destination_ip, self._destination_port))
            connection_socket.listen(1)
            self._tcp_connection, self._client_address = connection_socket.accept()

    def send(self, message):
        if isinstance(message, str):
            self._tcp_connection.sendall(message.encode('utf-8'))
        else:
            self._tcp_connection.sendall(pickle.loads(message))

    def receive(self, buffer_size: 'int', timeout: 'float' = None):
        self._tcp_connection.settimeout(timeout)
        packet = self._tcp_connection.recv(buffer_size)
        try:
            packet = packet.decode('utf-8')
        except UnicodeDecodeError:
            packet = pickle.loads(packet)
        self._tcp_connection.settimeout(None)
        return packet

    def __del__(self):
        self._tcp_connection.close()


def is_number_argument(argument):
    return argument.isnumeric()

