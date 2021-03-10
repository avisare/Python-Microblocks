from pypsexec.client import Client


def active_remote_agent(remote_username: "str", remote_password: "str", remote_ip: "str"):
    remote_control = Client(remote_ip, username=remote_username, password=remote_password)
    remote_control.connect()
    try:
        remote_control.create_service()
        stdout, stderr, rc = remote_control.run_executable("cmd.exe", arguments="/c cd.. & cd.. & cd test_remote & py start_server.py")
        print(stdout, stderr)
    finally:
        remote_control.remove_service()
        remote_control.disconnect()


