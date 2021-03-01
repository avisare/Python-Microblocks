from transportation_protocols import TCP_Connection, UDP_Connection


def run_server():
    close_connection = False
    server_port = input("Enter the port you want to listen on\n")
    if not server_port.isnumeric():
        raise Exception(f"Invalid port argument: {server_port}")

    print("Which transportation protocol do you want for your server?")
    transportation_protocol = input("Enter TCP for tcp and UDP for udp\n")
    if transportation_protocol == "UDP":
        server = UDP_Connection(int(server_port), False)
    elif transportation_protocol == "TCP":
        server = TCP_Connection(int(server_port), False)
    else:
        raise Exception(f"No such transportation protocol {transportation_protocol}")

    while not close_connection:
        buffer_size = input("Enter the buffer size of the message, close if you want to end the session\n")
        if buffer_size == "close":
            close_connection = True
        else:
            if not buffer_size.isnumeric():
                raise Exception(f"Invalid buffer size argument: {buffer_size}")
            packet = server.receive(int(buffer_size))
            print(f"Receive from the client: {packet}")
            message = input("Enter the message you want to send\n")
            server.send(message)


def run_client():
    close_connection = False
    client_port = input("Enter the port you want to connect to\n")
    if not client_port.isnumeric():
        raise Exception(f"Invalid port argument: {client_port}")

    print("Which transportation protocol do you want for your server?")
    transportation_protocol = input("Enter TCP for tcp and UDP for udp\n")
    if transportation_protocol == "UDP":
        client = UDP_Connection(int(client_port), True)
    elif transportation_protocol == "TCP":
        client = TCP_Connection(int(client_port), True)
    else:
        raise Exception(f"No such transportation protocol {transportation_protocol}")

    while not close_connection:
        message = input("Enter the message you want to send, close if you want to end the session\n")
        if message == "close":
            close_connection = True
        else:
            client.send(message)
            buffer_size = input("Enter the buffer size of the message\n")
            if not buffer_size.isnumeric():
                raise Exception(f"Invalid buffer size argument: {buffer_size}")
            packet = client.receive(int(buffer_size))
            print(f"Receive from the server: {packet}")


def main():
    print("Enter which side you want to be:")
    side = input("client for the client side and server for the server side\n")
    if side == "client":
        run_client()
    elif side == "server":
        run_server()


if __name__ == "__main__":
    main()
