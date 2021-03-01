from os import path
from HeadersParser import Parser


class RecursiveParser:

    def __init__(self, main_file_path):
        self._main_file = open(main_file_path, "r")
        self._includes = [main_file_path]

    def _get_includes_files(self):
        for line in self._main_file:
            if "#include" in line:
                include_file = line[line.find('#include "') + len('#include "'):line.rfind('"')]
                if path.exists(include_file):
                    self._includes.append(include_file)

    def parse(self):
        self._get_includes_files()
        parser = Parser(self._includes[-1])
        parser.initialize_structures(self._includes)
        parser.parse()

    def __del__(self):
        self._main_file.close()


def main():
    recursive_parser = RecursiveParser("SharedMemoryContent.h")
    recursive_parser.parse()


if __name__ == "__main__":
    main()
