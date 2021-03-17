from os import path
from HeadersParser import Parser


class RecursiveParser:

    def __init__(self, main_file_path):
        self._main_file_path = main_file_path
        self._main_file = open(main_file_path, "r")
        self._includes = list()

    def get_includes_recursive(self, includes, file_path):
        with open(file_path, "r") as sub_file:
            for line in sub_file:
                if "#include" in line:
                    include_file = line[line.find('#include "') + len('#include "'):line.rfind('"')]
                    if path.exists(include_file) and include_file not in includes:
                        self._includes.append(include_file)
                        self.get_includes_recursive(includes, include_file)

    def parse(self):
        temp_include_files = list()
        self.get_includes_recursive(temp_include_files, self._main_file_path)
        if self._main_file_path in temp_include_files:
            temp_include_files.remove(self._main_file_path)
        temp_include_files.append(self._main_file_path)
        self._includes = temp_include_files
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
