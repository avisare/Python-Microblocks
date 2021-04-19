import sys
from pypsexec.client import Client


def active_remote_agent(configurations):
    """
    function activate the remote agent that run the server with an appropriate
    configurations, printing the server output
    :param configurations: the configurations set up the server
    :return: None
    """
    remote_control = Client(configurations[2], username=configurations[0], password=configurations[1])
    remote_control.connect()
    try:
        remote_control.create_service()
        stdout, stderr, rc = remote_control.run_executable("cmd.exe", arguments=f"/c cd.. & cd.. & cd servers & python start_server.py {' '.join(configurations[3:])}")
        print(stdout.decode(), stderr.decode())
    finally:
        remote_control.remove_service()
        remote_control.disconnect()


def initialize_remote_arguments(configurations):
    """
    function initialize the remote base arguments
    :param configurations: the configurations for the remote server
    :return: list contains remote base arguments
    """
    remote_username = configurations[0]
    remote_password = configurations[1]
    remote_ip = configurations[2]
    mode = configurations[3]
    connection_type = configurations[4]
    timeout_seconds = configurations[5]
    buffer_size_bytes = configurations[6]
    return [remote_username, remote_password, remote_ip, mode, connection_type, timeout_seconds, buffer_size_bytes]


def main(configurations):
    remote_arguments = initialize_remote_arguments(configurations)
    if len(configurations) == 7:
        remote_arguments.append(str(None))
        remote_arguments.append(str(None))
        remote_arguments.append(str(None))
    if len(configurations) == 8:
        responder_port = configurations[7]
        remote_arguments.append(responder_port)
        remote_arguments.append(str(None))
        remote_arguments.append(str(None))
    elif len(configurations) == 9:
        responder_port = configurations[7]
        responder_ip = configurations[8]
        remote_arguments.append(responder_port)
        remote_arguments.append(responder_ip)
        remote_arguments.append(str(None))
    else:
        responder_port = configurations[7]
        responder_ip = configurations[8]
        local_port = configurations[9]
        remote_arguments.append(responder_port)
        remote_arguments.append(responder_ip)
        remote_arguments.append(local_port)
    active_remote_agent(tuple(remote_arguments))


if __name__ == "__main__":
    if len(sys.argv[1:]) <= 7 or len(sys.argv[1:]) > 10:
        print("You must pass at least 7 arguments:\n"
              "remote username\n"
              "remote password\n"
              "remote ip\n"
              "mode\n"
              "connection_type\n"
              "timeout_seconds\n"
              "buffer_size_bytes\n"
              "And maximum of 10 arguments:\n"
              "responder port\n"
              "responder ip\n"
              "local port")
    else:
        main(sys.argv[1:])
