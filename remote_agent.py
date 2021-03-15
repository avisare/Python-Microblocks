import sys
from threading import Thread
from pypsexec.client import Client
from json_config_singleton import JsonConfigSingleton
from parse_config import parse_config_files


def active_remote_agent(remote_username: "str", remote_password: "str", remote_ip: "str", config_files: "list"):
    remote_control = Client(remote_ip, username=remote_username, password=remote_password)
    remote_control.connect()
    try:
        remote_control.create_service()
        stdout, stderr, rc = remote_control.run_executable("cmd.exe", arguments=f"/c cd.. & cd.. & cd test_remote & py start_server.py {' '.join(config_files)}")
        print(stdout.decode(), stderr.decode())
    finally:
        remote_control.remove_service()
        remote_control.disconnect()


def main(config_files):
    config_dictionary = parse_config_files(config_files)
    timeout = None
    if "timeout_remote_seconds" in config_dictionary.keys():
        timeout = config_dictionary["timeout_remote_seconds"]
    JsonConfigSingleton(config_dictionary)
    active_remote_agent_thread = Thread(target=active_remote_agent, args=(config_dictionary["remote_username"], config_dictionary["remote_password"], config_dictionary["remote_ip"], config_files), daemon=True)
    active_remote_agent_thread.start()
    active_remote_agent_thread.join(timeout=timeout)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("You must pass at least one config file to the script")
    else:
        main(sys.argv[1:])
