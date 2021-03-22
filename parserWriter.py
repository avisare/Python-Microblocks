

class ParserWriter:
    def __init__(self, main_files):
        self._main_files = main_files
        self._structures = list()
        self._pybind_classes_file = open("SharedMemoryWrapper.cpp", "w")
        self._topics_file = open("sharedMemoryTopics.h", "w")

    def set_structures(self, structures):
        self._structures = structures

    def write_includes(self, include_files):
        self._topics_file.close()
        outer_include_files = [f'#include "{include_file_path}"\n' for include_file_path in self._main_files]
        with open("SharedMemoryWrapper.cpp", "r+") as main_file:
            content = main_file.read()
            main_file.seek(0, 0)
            main_file.write('#include "stdafx.h"\n')
            [main_file.write(include_path) for include_path in include_files]
            main_file.write('#include "Shared_Memory_Topics_API.h"\n\n'
                            '#include <pybind11\pybind11.h>\n\n#include <pybind11\stl.h>\n\n'
                            '#include <pybind11\stl_bind.h>\n\n#include <iostream>\n\n')
            main_file.write(content)

        with open("sharedMemoryTopics.h", "r+") as shared_memory_topics_file:
            content = shared_memory_topics_file.read()
            shared_memory_topics_file.seek(0, 0)
            shared_memory_topics_file.write(f'#pragma once\n#include "Shared_Memory_Topics_API.h"\n#include "GenericWrapperHandler.h"\n#include <pybind11/pybind11.h>\n#include <pybind11/stl.h>\n#include <pybind11/stl_bind.h>\n#include <iostream>\n')
            shared_memory_topics_file.write(content)

    def write_generic_function(self, function_name):
        self._pybind_classes_file.write(
            f'\n\tSharedMemoryWrapperModule.def("{function_name}", &{function_name}, py::return_value_policy::copy);\n')

    def write_function(self, function_signature, function_call):
        self._topics_file.write(f'\n\tbool {function_signature}\n\t')
        self._topics_file.write("{\n\t")
        self._topics_file.write(f"\t{function_call}\n\t")
        self._topics_file.write("}\n")

    def write_wrapper_pybind_class(self, struct):
        class_variables = list()
        with open(f"{struct.name}Class.h", "a") as class_file:
            class_file.write(f'\n\tpy::class_<{struct.full_name}>(SharedMemoryWrapperModule, "{struct.name}")\n')
            class_file.write(f"\t\t.def(py::init<>())")
            for variable in struct.variables:
                if variable != "":
                    if variable["array"]:
                        if "multi_dimensional_array" in variable.keys():
                            full_declaration = linecache.getline(struct.file_name, variable["line_number"])
                            first_size = full_declaration[full_declaration.find("[") + 1:full_declaration.find("]",full_declaration.find("["),-1)]
                            second_size = full_declaration[full_declaration.rfind("[") + 1:full_declaration.rfind("]")]
                            class_variables.append(({variable["name"]}, "dimensionalVector", variable["raw_type"], first_size, second_size))
                            class_file.write(f'\n\t\t.def_readwrite("{variable["name"]}", &{struct.full_name}::{variable["name"]})')
                        else:
                            class_variables.append((f'{variable["name"]}, {variable["name"]}Vector', variable['raw_type'], variable["size"]))
                            class_file.write(f'\n\t\t.def_readwrite("{variable["name"]}", &{struct.full_name}::{variable["name"]})')
                    else:
                        class_variables.append(f'obj.{variable["name"]}')
                        class_file.write(f'\n\t\t.def_readwrite("{variable["name"]}", &{struct.full_name}::{variable["name"]}, py::return_value_policy::copy)')

            class_file.write(f'\n\t\t.def(py::pickle(\n\t\t\t[](const {struct.full_name} &obj)')
            class_file.write("{\n\t\t\t")
            for class_variable in class_variables:
                if len(class_variable) == 5:
                    class_file.write(f"std::vector<std::vector<{class_variable[2]}>> {class_variable[1]};\n\t\t\t")
                    class_file.write(f"for (int i = 0; i < {class_variable[3]}; i++)\n\t\t\t")
                    class_file.write("{\n\t\t\t\t")
                    class_file.write(f"std::vector<{class_variable[2]}> temp;\n\t\t\t\t")
                    class_file.write(f"for (int j = 0; j < {class_variable[4]}; j++)")
                    class_file.write("{\n\t\t\t\t\t")
                    class_file.write(f"temp.push_back(obj.{class_variable[0]}[i][j]);")
                    class_file.write("\n\t\t\t\t\t}\n\t\t\t\t")
                    class_file.write(f"{class_variable[1]}.push_back(temp);")
                    class_file.write("\n\t\t\t\t}")
                elif len(class_variable) == 4:
                    class_file.write(f"std::vector<{class_variable[2]}> {class_variable[1]};\n\t\t\t")
                    class_file.write(f"for (int i = 0; i < {class_variable[3]}; i++)\n\t\t\t")
                    class_file.write("{\n\t\t\t\t")
                    class_file.write(f"{class_variable[1]}.push_back(obj.{class_variable[0]}[i]);")
                    class_file.write("\n\t\t\t\t}")
            class_file.write("return py::make_tuple(")
            class_file.write(f"{','.join(variable_functions)});\n")
            class_file.write("\t\t},\n\t\t\t[](py::tuple t){")
            class_file.write(f"\n\t\t\t{struct.full_name} obj = {struct.full_name}();")
            tuple_index = 0
            for variable in struct.variables:
                type = variable["raw_type"]
                if "enum" in variable.keys():
                    type = variable["enum"]
                if variable["array"]:
                    class_file.write(f'\n\t\t\tobj.{variable["name"]} = t[{tuple_index}].cast<std::vector<{type}>>();')
                    class_file.write(f"for (int i = 0; i < ; i++)\n\t\t\t")
                    class_file.write("{\n\t\t\t\t")
                    class_file.write("")
                elif "struct" in type:
                    inner_struct = self._find_struct(type[type.find("struct") + len("struct") + 1:])
                    if inner_struct is not None and inner_struct.have_wrapper:
                        class_file.write(f'\n\t\t\tobj.set{variable["name"]}(t[{tuple_index}].cast<{type[variable["type"].find("struct") + len("struct") + 1:]}Wrapper>());')
                    elif inner_struct is not None:
                        class_file.write(f'\n\t\t\tobj.set{variable["name"]}(t[{tuple_index}].cast<{type[variable["type"].find("struct") + len("struct") + 1:]}>());')
                    else:
                        print(f"Error occured, struct name {variable['raw_type']} wasn't found")
                else:
                    class_file.write(f'\n\t\t\tobj.set{variable["name"]}(t[{tuple_index}].cast<{type}>());')
                tuple_index += 1
            class_file.write("\n\t\t\treturn obj;\n\t\t}\n\t\t));\n")
            if not struct.need_smt_functions:
                class_file.write("}")
            else:
                self.write_overload_smt_functions(class_file, struct.topic_name)


    def write_overload_smt_functions(self, class_file, topic_name):
        smt_overload_functions = [f'.def("getOldest",'
                                  f' py::overload_cast<void*, SMT_DataInfo&>(&{topic_name}::GetOldest),'
                                  f'py::return_value_policy::copy)',
                                  f'.def("getOldest",'
                                  f' py::overload_cast<void*>(&{topic_name}::GetOldest),'
                                  f'py::return_value_policy::copy)',
                                  f'.def("getByCounter",'
                                  f' py::overload_cast<void*, '
                                  f'uint32_t, uint64_t, SMT_DataInfo&>(&{topic_name}::GetByCounter), py::return_value_policy::copy)',
                                  f'.def("getByCounter",'
                                  f' py::overload_cast<void*, '
                                  f'uint32_t, uint64_t>(&{topic_name}::GetByCounter), py::return_value_policy::copy)',
                                  f'.def("publish", '
                                  f'py::overload_cast<void*>(&{topic_name}::Publish), '
                                  f'py::return_value_policy::copy)',
                                  f'.def("publish", '
                                  f'py::overload_cast<void*, size_t>(&{topic_name}::Publish), '
                                  f'py::return_value_policy::copy)',
                                  f'.def("getLatest",'
                                  f' py::overload_cast<void*, SMT_DataInfo&>(&{topic_name}::GetLatest),'
                                  f' py::return_value_policy::copy)',
                                  f'.def("getLatest",'
                                  f' py::overload_cast<void*>(&{topic_name}::GetLatest),'
                                  f' py::return_value_policy::copy)']
        class_file.write(f'\n\tpy::class_<{topic_name}>(SharedMemoryWrapperModule, "{topic_name}")')
        class_file.write("\n\t\t.def(py::init<>())")
        [class_file.write("\n\t\t" + smt_overload_function) for smt_overload_function in smt_overload_functions]
        class_file.write(";\n}")

    def write_smt_functions(self, struct):
        smt_functions_signature = [
            (f"GetByCounter(void* structObject, uint32_t counter, uint64_t timeout_us, "
             "SMT_DataInfo& data_info)",
             f'return SMT_GetByCounter(_topicName.c_str(), structObject, counter, timeout_us, &data_info);'),
            (f"GetByCounter(void* structObject, uint32_t counter, uint64_t timeout_us)",
             'SMT_DataInfo data_info = SMT_DataInfo{0,0,0};\n\t\t'
             f'return SMT_GetByCounter(_topicName.c_str(), structObject, counter, timeout_us, &data_info);'),
            (f"GetLatest(void* structObject, SMT_DataInfo& data_info)",
             f'return SMT_GetLatest(_topicName.c_str(), structObject, &data_info);'),
            (f"GetLatest(void* structObject)",
             'SMT_DataInfo data_info = SMT_DataInfo{0,0,0};\n\t\t'
             f'return SMT_GetLatest(_topicName.c_str(), structObject, &data_info);'),
            (f"Publish(void* structObject)",
             f'return SMT_Publish(_topicName.c_str(), structObject, _topicSize);'),
            (f"Publish(void* structObject, size_t size)",
             f'return SMT_Publish(_topicName.c_str(), structObject, size);'),
            (f"GetOldest(void* structObject, SMT_DataInfo& data_info)",
             f'return SMT_GetOldest(_topicName.c_str(), structObject, &data_info);'),
            (f"GetOldest(void* structObject)",
             'SMT_DataInfo data_info = SMT_DataInfo{0,0,0};\n\t\t'
             f'return SMT_GetOldest(_topicName.c_str(), structObject, &data_info);')]
        self._topics_file.write(f"class {struct.topic_name}\n")
        self._topics_file.write("{\nprivate:\n\tstd::string _topicName;\n\tint _topicSize;\npublic:\n\t")
        self._topics_file.write(f'{struct.topic_name}()\n\t')
        self._topics_file.write("{\n\t\t_topicName=")
        self._topics_file.write(f'"{struct.topic_name}";\n\t\t_topicSize={struct.struct_size};\n\t')
        self._topics_file.write("}\n")
        [self.write_function(smt_function_signature, smt_function_call) for smt_function_signature, smt_function_call in smt_functions_signature]
        self._topics_file.write("};\n")

    def write_enums_file(self, enums):
        with open("enums.h", "w") as enums_file:
            includes = "\n".join(self._main_files)
            enums_file.write(f'#pragma once\n#include "{includes}"\n#include <pybind11/pybind11.h>\n#include <pybind11/stl.h>\n#include <pybind11/stl_bind.h>\n#include <iostream>\n')
            enums_file.write("namespace py = pybind11;\n")
            enums_file.write("void enumsRunner(py::module & SharedMemoryWrapperModule)\n{")
            for enum in enums:
                enums_file.write(f'\n\tpy::enum_<{enum["namespace"]}{enum["name"]}>(SharedMemoryWrapperModule, "{enum["name"]}")')
                for enum_value in enum["values"]:
                    enums_file.write(f'\n\t\t.value("{enum_value["name"]}", {enum["namespace"]}{enum_value["name"]})')
                enums_file.write(f'\n\t\t.export_values();')
            enums_file.write("}")

    def write_main_file_prefix(self, vector_types):
        for vector_type in vector_types:
            self._pybind_classes_file.write(f"PYBIND11_MAKE_OPAQUE(std::vector<{vector_type}>);\n")
        self._pybind_classes_file.write("namespace py = pybind11;\n\nPYBIND11_MODULE(SharedMemoryWrapper, SharedMemoryWrapperModule)\n{\n\t")
        for vector_type in vector_types:
                self._pybind_classes_file.write(f'py::bind_vector<std::vector<{vector_type}>> (SharedMemoryWrapperModule, "{vector_type}List");\n\t')
        self._pybind_classes_file.write("\n")
        generic_functions = ("SMT_Version", "SMT_Init", "SMT_Show", "SMT_CreateTopic",
                             "SMT_GetPublishCount", "SMT_ClearHistory")
        for generic_function in generic_functions:
            self.write_generic_function(generic_function)

    def write_struct_class_prefix(self, struct):
        with open(f"{struct.name}Class.h", "w") as class_file:
            class_file.write('# pragma once\n#include "sharedMemoryTopics.h"\n'
                             '#include "Shared_Memory_Topics_API.h"\n#include "GenericWrapperHandler.h"\n'
                             '#include <pybind11\pybind11.h>\n#include <pybind11\stl.h>\n'
                             '#include <pybind11\stl_bind.h>\n#include <iostream>\n'
                             f'namespace py = pybind11;\nvoid {struct.name}ClassRunner(py::module & SharedMemoryWrapperModule)\n'
                             '{\n')

    def write_class_call(self, structs, enums):
        [self._pybind_classes_file.write(f"\n\n\t{struct.name}ClassRunner(SharedMemoryWrapperModule);") for struct in structs]
        if enums:
            self._pybind_classes_file.write("\n\n\tenumsRunner(SharedMemoryWrapperModule);")

    def _find_struct(self, struct_name):
        for struct in self._structures:
            if struct.name == struct_name:
                return struct
        return None

    def write_file_ending(self):
        self._pybind_classes_file.write("\n}")

    def __del__(self):
        self._pybind_classes_file.close()
        self._topics_file.close()
