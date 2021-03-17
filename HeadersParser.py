import CppHeaderParser
from parserWriter import ParserWriter
from struct import Struct


class Parser:

    def __init__(self, main_header_file):
        self._wrapper_class = list()
        self._structures = list()
        self._include_files = list()
        self._vectors_type = set()
        self._writer = ParserWriter(main_header_file)
        self._main_header_file = main_header_file

    def _create_wrapper_class(self, struct):
        functions_signature = list()
        inner_structs = list()
        vector_names = list()
        vector_sizes = list()
        self._writer.write_class_prefix(struct, functions_signature)
        if self._has_array(struct):
            self._writer.write_update_functions_signatures(functions_signature)
        for variable in struct.variables:
            if variable["name"] != "":
                if variable["array"]:
                    self._vectors_type.add(variable['type'])
                    vector_sizes.append(variable["array_size"])
                    vector_names.append(variable['name'])
                    self._writer.write_vector(variable['type'], variable['name'])
                elif "struct" in variable["raw_type"] and \
                        variable["raw_type"][variable["raw_type"].find("struct") + len("struct") + 1:]\
                        in self._wrapper_class:
                    self._writer.write_inner_struct(functions_signature, inner_structs, variable)
                else:
                    self._writer.write_class_variable(functions_signature, variable)
        self._writer.write_get_class_pointer(struct, functions_signature)
        self._writer.write_class_private(struct)
        self._writer.write_inner_structs_variables(inner_structs)
        self._write_cpp_implementation_file(struct, functions_signature, vector_sizes, vector_names)

    def _write_cpp_implementation_file(self, struct, functions_definition, vector_sizes, vector_names):
        for return_type, function_signature in functions_definition:
            if "get" not in function_signature and "set" not in function_signature and "update" not in function_signature:
                function_name = struct.full_name + "::" + function_signature
            else:
                function_name = function_signature[:function_signature.find(return_type) + len(return_type) + 1] + struct.full_name + "::" + function_signature[function_signature.find(return_type) + len(return_type) + 1:]
            if "update" in function_name:
                self._writer.write_update_function_implementation(struct, function_name, vector_sizes, vector_names)
            else:
                if "set" in function_name:
                    self._writer.write_function_signature(function_name)
                    self._writer.write_set_function(struct, function_name)
                elif "get" in function_name:
                    self._writer.write_function_signature(function_name)
                    self._writer.write_get_function(struct, function_name)
                else:
                    self._writer.write_constructor(struct.name)

    def _has_array(self, struct):
        for variable in struct.variables:
            if variable["array"]:
                return True
        return False

    def _create_pybind_class(self, struct):
        if struct.have_wrapper:
            self._writer.write_wrapper_pybind_class(struct)
        else:
            self._writer.write_pybind_class_without_wrappper(struct)

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
            if struct.name in self._wrapper_class:
                self._create_wrapper_class(struct)
            if struct.need_smt_functions:
                self._writer.write_smt_functions(struct)
        self._writer.write_main_file_prefix(self._vectors_type)
        for struct in self._structures:
            self._writer.write_struct_class_prefix(struct)
            self._create_pybind_class(struct)
        self._writer.write_class_call(self._structures)
        self._writer.write_file_ending()
        self._writer.write_includes(self._include_files)

    def initialize_structures(self, headers_files):
        headers = [CppHeaderParser.CppHeader(header_file) for header_file in headers_files]
        class_keep_changing = True
        while class_keep_changing:
            class_keep_changing = False
            for header in headers:
                for struct_name, struct_content in header.classes.items():
                    struct_variables = struct_content["properties"]["public"]
                    if self._need_wrapper_class(struct_variables) and struct_name not in self._wrapper_class:
                        self._wrapper_class.append(struct_name)
                        class_keep_changing = True
        #  need to be deleted, after the sizes of topics will be received
        structs_size = {"SharedMemoryContent": 36, "testStructOne": 9, "testStructTwo": 42, "testStructThree": 33, "testStructFour": 44}
        index = 1
        for header in headers:
            for struct_name, struct_content in header.classes.items():
                struct_variables = struct_content["properties"]["public"]
                if self._need_wrapper_class(struct_variables):
                    self._structures.append(Struct(struct_content["namespace"], struct_name,
                                                   struct_variables, True, "Wrapper", index == 1, struct_name + "Topic", structs_size[struct_name]))
                else:
                    self._structures.append(Struct(struct_content["namespace"], struct_name, struct_variables,
                                                   False, struct_content["namespace"], index == 1, struct_name + "Topic", structs_size[struct_name]))
            index += 1
        self._writer.set_structures(self._structures)

    def initialize_generic_topic_functions(self):
        generic_functions = ("SMT_Version", "SMT_Init", "SMT_Show", "SMT_CreateTopic",
                             "SMT_GetPublishCount", "SMT_ClearHistory")
        for generic_function in generic_functions:
            self._writer.write_generic_function(generic_function)
