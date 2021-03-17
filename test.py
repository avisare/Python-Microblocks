from transportation_protocols.connection_factory import ConnectionFactory
from parse_config import parse_config_files

#config_dictionary = parse_config_files(("config.json",))
#JsonConfigSingleton(config_dictionary)

y = 20

def server():
    tcp_server = ConnectionFactory.get_connection()
    tcp_server.send("dwqd")
    msg = tcp_server.receive()
    print(msg)

def test():
    global y
    y = 100


def client():
    tcp_client = ConnectionFactory.get_connection()
    msg = tcp_client.receive()
    print(msg)
    tcp_client.send("hello")

#client()
