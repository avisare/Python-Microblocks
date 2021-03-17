import sys
from threading import Thread
from pypsexec.client import Client


def active_remote_agent(arguments):
    remote_control = Client(arguments[2], username=arguments[0], password=arguments[1])
    remote_control.connect()
    try:
        remote_control.create_service()
        stdout, stderr, rc = remote_control.run_executable("cmd.exe", arguments=f"/c cd.. & cd.. & cd test_remote & py start_server.py {' '.join(arguments[3:])}")
        print(stdout.decode(), stderr.decode())
    finally:
        remote_control.remove_service()
        remote_control.disconnect()


def main(args):
    remote_username = args[0]
    remote_password = args[1]
    remote_ip = args[2]
    mode = args[3]
    connection_type = args[4]
    timeout_seconds = args[5]
    buffer_size_bytes = args[6]
    remote_arguments = [remote_username, remote_password, remote_ip, mode, connection_type, timeout_seconds, buffer_size_bytes]
    if len(args) == 7:
        remote_arguments.append(str(None))
        remote_arguments.append(str(None))
        remote_arguments.append(str(None))
    if len(args) == 8:
        responder_port = args[7]
        remote_arguments.append(responder_port)
        remote_arguments.append(str(None))
        remote_arguments.append(str(None))
    elif len(args) == 9:
        responder_port = args[7]
        responder_ip = args[8]
        remote_arguments.append(responder_port)
        remote_arguments.append(responder_ip)
        remote_arguments.append(str(None))
    else:
        responder_port = args[7]
        responder_ip = args[8]
        local_port = args[9]
        remote_arguments.append(responder_port)
        remote_arguments.append(responder_ip)
        remote_arguments.append(local_port)
    active_remote_agent_thread = Thread(target=active_remote_agent, args=(tuple(remote_arguments), ), daemon=True)
    active_remote_agent_thread.start()
    active_remote_agent_thread.join()


if __name__ == "__main__":
    if len(sys.argv[1:]) <= 7 or len(sys.argv[1:]) > 10:
        print(len(sys.argv[1:]))
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
