import pickle
from datetime import time
from .udp_device import UDPDevice


class UDPInitiatorConnection(UDPDevice):
    """
    This class represent UDP Initiator, which means connection type, who can
    only send packets to destinations, but not receive. Because of that this connection
    implement only the send  function.
    """
    def __init__(self, udp_connection, destination_ip, destination_port, timeout: 'time', buffer_size_bytes: 'int'):
        super().__init__(timeout, buffer_size_bytes)
        self._udp_connection = udp_connection
        self._destination_ip = destination_ip
        self._destination_port = destination_port

    def send(self, message):
        self._udp_connection.sendto(pickle.dumps(message), (self._destination_ip, self._destination_port))

    def receive(self, timeout_seconds: "int" = None, buffer_size_bytes: "int" = None):
        pass

    def __del__(self):
        try:
            self._udp_connection.sendto("exit".encode(), self._destination_ip, self._destination_port)
        except Exception:
            pass
        else:
            self._udp_connection.close()
