import socket


class TCP_Connection:

    local_ip = "127.0.0.1"
    
    def __init__(self, destination_port, is_client, destination_ip=local_ip):
        self._destination_ip = destination_ip
        self._destination_port = destination_port
        if is_client:
            self._tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._tcp_connection.connect((self._destination_ip, self._destination_port))
        else:
            connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection_socket.bind((self._destination_ip, self._destination_port))
            print(f"Waiting for a client to connect to ip {self._destination_ip} and port {self._destination_port}")
            connection_socket.listen(1)
            self._tcp_connection, self._client_address = connection_socket.accept()
        print("Connected")

    def send(self, message):
        self._tcp_connection.sendall(message.encode('utf-8'))

    def receive(self, buffer_size, timeout=None):
        self._tcp_connection.settimeout(timeout)
        print(f"Wating for message from ip {self._destination_ip} and port {self._destination_port}")
        packet = self._tcp_connection.recv(buffer_size).decode('utf-8')
        self._tcp_connection.settimeout(None)
        return packet

    def __del__(self):
        self._tcp_connection.close()


def is_number_argument(argument):
    return argument.isnumeric()

