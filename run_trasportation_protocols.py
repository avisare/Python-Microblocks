from transportation_protocols import connection_factory


def run_server():
    connection = connection_factory.ConnectionFactory.get_connection()

    while True:
        packet = connection.receive()
        print(f"Receive from the client: {packet}")
        message = input("Enter the message you want to send\n")
        connection.send(message)


def run_client():
    connection = connection_factory.ConnectionFactory.get_connection()

    while True:
        message = input("Enter the message you want to send, close if you want to end the session\n")
        connection.send(message)
        packet = connection.receive()
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
