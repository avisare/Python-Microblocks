import CppHeaderParser
import linecache
from parserWriter import ParserWriter
from struct import Struct


class Parser:

    def __init__(self, main_header_file):
        self._enums = list()
        self._wrapper_class = list()
        self._structures = list()
        self._include_files = list()
        self._vectors_type = set()
        self._writer = ParserWriter([main_header_file,])
        self._main_header_file = main_header_file

    def _create_wrapper_class(self, struct):
        functions_signature = list()
        vector_names = list()
        vector_sizes = list()
        for variable in struct.variables:
            if variable["name"] != "":
                if variable["array"]:
                    if "multi_dimensional_array" in variable.keys():
                        type = variable["raw_type"]
                        full_declaration = linecache.getline(struct.file_name, variable["line_number"])
                        first_size = full_declaration[full_declaration.find("[") + 1:full_declaration.find("]", full_declaration.find("["), -1)]
                        second_size = full_declaration[full_declaration.rfind("[")+1:full_declaration.rfind("]")]
                        vector_sizes.append(f"{first_size},{second_size}")
                    else:
                        type = variable['raw_type']
                        vector_sizes.append(variable["array_size"])
                    self._vectors_type.add(type)
                    vector_names.append(variable['name'])

    def _has_array(self, struct):
        for variable in struct.variables:
            if variable["array"]:
                return True
        return False

    def _need_wrapper_class(self, struct_variables):
        for struct_variable in struct_variables:
            if struct_variable["array"] or\
                    ("struct" in struct_variable["raw_type"]
                     and struct_variable["raw_type"][struct_variable["raw_type"].find("struct") + len("struct") + 1:]
                     in self._wrapper_class):
                return True
        return False

    def parse(self):
        for struct in self._structures:
            self._include_files.append(f'#include "{struct.name}Class.h"\n\n')
            if struct.need_smt_functions:
                self._writer.write_smt_functions(struct)
        self._writer.write_main_file_prefix(self._vectors_type)
        for struct in self._structures:
            self._writer.write_struct_class_prefix(struct)
            self._writer.write_wrapper_pybind_class(struct)
        self._writer.write_class_call(self._structures, len(self._enums) > 0)
        self._writer.write_file_ending()
        if len(self._enums) > 0:
            self._include_files.append('#include "enums.h"\n')
        self._writer.write_includes(self._include_files)

    def initialize_structures(self, headers_files):
        headers = [CppHeaderParser.CppHeader(header_file) for header_file in headers_files]
        for header in headers:
            self._enums += header.enums
        if len(self._enums) > 0:
            self._writer.write_enums_file(self._enums)
        #  need to be deleted, after the sizes of topics will be received
        structs_size = {"SharedMemoryContent": 36, "testStructOne": 25, "testStructTwo": 42, "testStructThree": 33, "testStructFour": 44, "NavCov_Record": 8, "test": 440}
        index = 1
        for header in headers:
            file = headers_files[index-1]
            for struct_name, struct_content in header.classes.items():
                struct_variables = struct_content["properties"]["public"]
                self._structures.append(Struct(struct_content["namespace"], struct_name,
                                               struct_variables, index == 1, struct_name + "Topic", structs_size[struct_name], file))
            index += 1
        self._writer.set_structures(self._structures)

    def initialize_generic_topic_functions(self):
        generic_functions = ("SMT_Version", "SMT_Init", "SMT_Show", "SMT_CreateTopic",
                             "SMT_GetPublishCount", "SMT_ClearHistory")
        for generic_function in generic_functions:
            self._writer.write_generic_function(generic_function)
