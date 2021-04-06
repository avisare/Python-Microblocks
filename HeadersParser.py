import CppHeaderParser
import linecache
from parserWriter import ParserWriter
from struct import Struct


class Parser:

    def __init__(self, main_headers_file, topics_index_file):
        self._enums = list()
        self._wrapper_class = list()
        self._structures = list()
        self._include_files = list()
        self._writer = ParserWriter(main_headers_file, topics_index_file)
        self._main_headers_file = main_headers_file

    def _create_wrapper_class(self, struct):
        vector_names = list()
        vector_sizes = list()
        for variable in struct.variables:
            if variable["name"] != "":
                if variable["array"]:
                    if "multi_dimensional_array" in variable.keys():
                        full_declaration = linecache.getline(struct.file_name, variable["line_number"])
                        first_size = full_declaration[full_declaration.find("[") + 1:full_declaration.find("]", full_declaration.find("["), -1)]
                        second_size = full_declaration[full_declaration.rfind("[")+1:full_declaration.rfind("]")]
                        vector_sizes.append(f"{first_size},{second_size}")
                    else:
                        vector_sizes.append(variable["array_size"])
                    vector_names.append(variable['name'])

    def parse(self):
        for struct in self._structures:
            self._include_files.append(f'#include "{struct.name}Class.h"\n\n')
        vectors_type = list()
        for struct in self._structures:
            self._writer.write_struct_class_prefix(struct)
            self._writer.write_wrapper_pybind_class(struct, vectors_type)
            self._writer.write_topics()
        self._writer.write_class_call(self._structures, len(self._enums) > 0)
        self._writer.write_file_ending()
        if len(self._enums) > 0:
            self._include_files.append('#include "enums.h"\n\n')
        self._writer.write_includes(self._include_files)
        self._writer.write_main_file_prefix(vectors_type, self._include_files)

    def initialize_structures(self, main_files_path):
        headers = [CppHeaderParser.CppHeader(header_file) for header_file in self._main_headers_file]
        structures_dictionary = dict()
        for header in headers:
            self._enums += header.enums
        if len(self._enums) > 0:
            self._writer.write_enums_file(self._enums)
        index = 0
        for header in headers:
            file = main_files_path[index]
            for struct_name, struct_content in header.classes.items():
                struct_variables = struct_content["properties"]["public"]
                struct = Struct(struct_content["namespace"], struct_name,
                                               struct_variables, file)
                self._structures.append(struct)
                structures_dictionary[struct_name] = struct
            index += 1
            self._get_missing_structs(structures_dictionary, header, file)
        self._writer.set_structures(self._structures)
        self._writer.set_structures_dictionary(structures_dictionary)

    def _get_missing_structs(self, structures_dictionary, header, file):
        for struct_name, struct_content in header.classes.items():
            for var in struct_content["properties"]["public"]:
                if len(var['aliases']) > 0:
                    if var['typedef'] is None and "enum" not in var.keys():
                        if var not in structures_dictionary.keys():
                            includes = list()
                            self._get_includes(file, includes)
                            for include_file in includes:
                                missing_struct = self._search_for_struct(include_file, var['name'])
                                if missing_struct is not None:
                                    self._structures.append(missing_struct)
                                    structures_dictionary[missing_struct.struct_name] = missing_struct

    def _get_includes(self, file, includes):
        with open(file, "r") as header_file:
            for line in header_file:
                if "#include" in line and (line.count('"') == 2 or line.count("'") == 2):
                    if "'" in line:
                        include_path = line[line.find("'") + 1:line.rfind("'")]
                        if include_path not in includes:
                            includes.append(include_path)
                            self._get_includes(include_path, includes)
                    else:
                        include_path = line[line.find('"') + 1:line.rfind('"')]
                        if include_path not in includes:
                            includes.append(include_path)
                            self._get_includes(include_path, includes)

    def _search_for_struct(self, include_file_path, missing_struct_name):
        header = CppHeaderParser.CppHeader(include_file_path)
        for struct_name, struct_content in header.classes.items():
            if struct_name == missing_struct_name:
                struct_variables = struct_content["properties"]["public"]
                return Struct(struct_content["namespace"], struct_name, struct_variables, include_file_path)
        return None

    def initialize_generic_topic_functions(self):
        generic_functions = ("SMT_Version", "SMT_Init", "SMT_Show", "SMT_CreateTopic",
                             "SMT_GetPublishCount", "SMT_ClearHistory")
        for generic_function in generic_functions:
            self._writer.write_generic_function(generic_function)
