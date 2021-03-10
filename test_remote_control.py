from threading import Thread
from time import sleep
from remote_agent import active_remote_agent
from pypsexec_client.test_client import test_client
from json_config_singleton import JsonConfigSingleton
from parse_config import parse_config_files


def start_test(*config_files):
    config_dictionary = parse_config_files(config_files)
    JsonConfigSingleton(config_dictionary)
    active_remote_agent_thread = Thread(target=active_remote_agent, args=("Administrator", "1234", "127.0.0.1"))
    active_remote_agent_thread.daemon = True
    active_remote_agent_thread.start()
    sleep(5)
    test_client()
    active_remote_agent_thread.join(timeout=15)
