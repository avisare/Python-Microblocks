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
    responder_port = args[3]
    remote_arguments = [remote_username, remote_password, remote_ip, responder_port]
    if len(args) == 5:
        responder_ip = args[4]
        remote_arguments.append(responder_ip)
    elif len(args) == 6:
        local_port = args[5]
        remote_arguments.append(local_port)
    active_remote_agent_thread = Thread(target=active_remote_agent, args=tuple(remote_arguments), daemon=True)
    active_remote_agent_thread.start()
    active_remote_agent_thread.join()


if __name__ == "__main__":
    if len(sys.argv) <= 4 or len(sys.argv) > 7:
        print("You must pass at least 4 arguments:\n"
              "remote username\n"
              "remote password\n"
              "remote ip\n"
              "responder port\n"
              "And maximum of 7 arguments:\n"
              "responder ip\n"
              "local port")
    else:
        main(sys.argv[1:])
