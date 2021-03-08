import json
import SharedMemoryWrapper


def parse_configuration(config_file_path, topics_config_path):
    with open(config_file_path, "r") as config_file:
        config_dict = json.load(config_file)
    for config_name in config_dict:
        if config_name == "tcp_port":
            open_tcp_port(config_dict["tcp_port"])
        elif config_name == "udp_port":
            open_tcp_port(config_dict["udp_port"])
        elif config_name == "topics":
            create_topics(config_dict["topics"], topics_config_path)
        else:
            print(f"Config name {config_name} is not recognize by the parser")


def open_tcp_port(port):
    pass


def open_udp_port(port):
    pass


def create_topics(topics, topics_config_path):
    SharedMemoryWrapper.SMT_Init()
    with open(topics_config_path, "r") as topics_config:
        topics_config_dict = json.load(topics_config)
    for topic_name in topics:
        if topic_name in topics_config_dict.keys():
            SharedMemoryWrapper.SMT_CreateTopic(topic_name, topics_config_dict[topic_name]["maxDataSize"], topics_config_dict[topic_name]["historyDepth"], topics_config_dict[topic_name]["cellsCount"])
        else:
            print(f"Couldn't find apropriate configuration for topic {topic_name}")


parse_configuration("example_config.json", "topics_config_example.json")