from os import path
from HeadersParser import Parser
from sys import argv
import glob


class RecursiveParser:

    def __init__(self, collab_directory):
        self._main_files_path = glob.glob(collab_directory + "*.h")
        self._main_files = [open(main_file_path, "r") for main_file_path in self._main_files]
        self._includes = list()

    def get_includes_recursive(self, file_path):
        with open(file_path, "r") as sub_file:
            for line in sub_file:
                if "#include" in line:
                    include_file = line[line.find('#include "') + len('#include "'):line.rfind('"')]
                    if path.exists(include_file) and include_file not in self._includes:
                        self._includes.append(include_file)
                        self.get_includes_recursive(include_file)

    def parse(self, topics_index_file):
        parser = Parser(self._main_files, topics_index_file)
        parser.initialize_structures(self._main_files_path)
        parser.parse()

    def __del__(self):
        [main_file.close() for main_file in self._main_files]


def main(arguments):
    if len(arguments) != 2:
        raise Exception("Program expected to 2 arguments exactly. directory path of all collabs file and topic_info json file path")
    recursive_parser = RecursiveParser(arguments[0])
    recursive_parser.parse(arguments[1])


if __name__ == "__main__":
    main(argv[1:])
