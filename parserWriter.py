import linecache
from json_python import JsonHelper


class ParserWriter:
    def __init__(self, main_file, topics_index_file):
        self._main_file = main_file
        self._topics_index_file = JsonHelper.read_file(topics_index_file)
        self._structures = list()
        self._pybind_classes_file = open("SharedMemoryWrapper.cpp", "w")
        self._topics_file = open("sharedMemoryTopics.h", "w")
        self._structures_dictionary = dict()

    def set_structures(self, structures):
        self._structures = structures

    def set_structures_dictionary(self, structures_dictionary):
        self._structures_dictionary = structures_dictionary

    def write_includes(self, include_files):
        self._topics_file.close()

        with open("sharedMemoryTopics.h", "r+") as shared_memory_topics_file:
            content = shared_memory_topics_file.read()
            shared_memory_topics_file.seek(0, 0)
            shared_memory_topics_file.write(f'#pragma once\n\n#include "{self._main_file[0]}"\n\n#include "Shared_Memory_Topics_API.h"\n\n#include <pybind11/pybind11.h>\n\n#include <pybind11/stl.h>\n\n#include <pybind11/stl_bind.h>\n\n#include <iostream>\n\n')
            shared_memory_topics_file.write(content)

    def write_generic_function(self, function_name):
        self._pybind_classes_file.write(
            f'\n\tSharedMemoryWrapperModule.def("{function_name}", &{function_name}, py::return_value_policy::copy);\n')

    def write_function(self, function_signature, function_call):
        self._topics_file.write(f'\n\tbool {function_signature}\n\t')
        self._topics_file.write("{\n\t")
        self._topics_file.write(f"\t{function_call}\n\t")
        self._topics_file.write("}\n")

    def write_wrapper_pybind_class(self, struct, vector_types):
        with open(f"{struct.name}Class.h", "a") as class_file:
            class_file.write(f'\n\tpy::class_<{struct.full_name}>(SharedMemoryWrapperModule, "{struct.name}")\n')
            class_file.write(f"\t\t.def(py::init<>())")
            class_variables_names, class_variables = self._write_class_variables(class_file, struct, vector_types)
            class_file.write(f'\n\t.def(py::pickle(\n\t\t[](const {struct.full_name} &obj)')
            class_file.write("{\n\t\t")
            self._write_pack_class_pickle(class_file, class_variables, class_variables_names)
            class_file.write("\t},\n\t\t[](py::tuple t){")
            class_file.write(f"\n\t\t{struct.full_name} obj = {struct.full_name}();")
            self._write_unpack_class_pickle(class_file, struct)
            class_file.write("\n\t\treturn obj;\n\t}\n\t));\n")
            class_file.write("}")

    def _write_class_variables(self, class_file, struct, vector_types, vector_sizes):
        class_variables_names = list()
        class_variables = list()
        for variable in struct.variables:
            if variable != "":
                if variable["array"]:
                    if len(variable['aliases']) > 0 and variable['typedef'] is None and "enum" not in variable.keys():
                        self._write_vector(struct, class_file, variable, vector_types)

                    else:
                        self._write_array(struct, class_file, variable, vector_types)
                        full_declaration = linecache.getline(struct.file_name, variable["line_number"])
                        first_size = full_declaration[full_declaration.find("[") + 1:full_declaration.find("]", full_declaration.find("["), -1)]
                        second_size = full_declaration[full_declaration.rfind("[") + 1:full_declaration.rfind("]")]
                        class_variables.append((variable["name"], f'{variable["name"]}Vector', variable["raw_type"],
                                                first_size, second_size))
                        class_file.write(
                            f'\n\t\t.def_property("{variable["name"]}", []({struct.full_name} &obj)->py::array')
                        class_file.write("{\n\t\t")
                        class_file.write(f'auto dtype = py::dtype(py::format_descriptor<{variable["raw_type"]}>::format());\n\t\t')
                        class_file.write('auto base = py::array(dtype, { '
                                         f'{first_size}, {second_size}'
                                         ' }, { sizeof('
                                         f'{variable["raw_type"]}) * {second_size}, sizeof({variable["raw_type"]})'
                                         ' });')
                        class_file.write("\n\t\treturn py::array(dtype, {"
                                         f"{first_size}, {second_size}"
                                         " }, { sizeof("
                                         f'{variable["raw_type"]}) * {second_size}, sizeof({variable["raw_type"]})'
                                         ' }, '
                                         f'obj.{variable["name"]}, base);')
                        class_file.write("\n\t\t},")
                        class_file.write(f'[]({struct.full_name}& obj, py::list set{variable["name"]})\n\t\t')
                        class_file.write("{\n\t\t\t")
                        class_file.write(f"for (int i = 0; i < {first_size}; i++)\n\t\t\t"
                                         "{\n\t\t\t\t"
                                         f"py::list temp = set{variable['name']}[i].cast<py::list>();\n\t\t\t\t"
                                         f"for (int j =0; j < {second_size}; j++)"
                                         "\n\t\t\t\t{\n\t\t\t\t\t"
                                         f"obj.{variable['name']}[i][j] = temp[j].cast<{variable['raw_type']}>();\n\t\t\t\t"
                                         "}\n\t\t\t}\n\t\t})")
                        class_variables_names.append(f'{variable["name"]}Vector')
                    else:
                        if len(variable['aliases']) > 0 and variable['typedef'] is None and "enum" not in variable.keys():

                        else:
                            class_variables.append((variable["name"], f'{variable["name"]}Vector', variable['raw_type'],
                                                    variable["array_size"]))
                            class_variables_names.append(f'{variable["name"]}Vector')
                            class_file.write(f'\n\t\t.def_property("{variable["name"]}", []({struct.full_name} &obj)->py::array ')
                            class_file.write("{\n\t\t")
                            class_file.write(
                                f"auto dtype = py::dtype(py::format_descriptor<{variable['raw_type']}>::format());\n\t\t"
                                "auto base = py::array(dtype, {"
                                f" {variable['array_size']}"
                                " }, { "
                                f"sizeof({variable['raw_type']}) "
                                "});")
                            class_file.write("\n\t\treturn py::array(dtype, {"
                                             f"{variable['array_size']}"
                                             " }, { sizeof("
                                             f'{variable["raw_type"]})'
                                             ' }, '
                                             f'obj.{variable["name"]}, base);')
                            class_file.write("\n\t\t},")
                            class_file.write(f'[]({struct.full_name}& obj, py::list set{variable["name"]})\n\t\t')
                            class_file.write("{\n\t\t\t")
                            class_file.write(f"for (int i = 0; i < {variable['array_size']}; i++)\n\t\t\t"
                                             "{\n\t\t\t\t"
                                             f'obj.{variable["name"]}[i] = set{variable["name"]}[i].cast<{variable["raw_type"]}>();'
                                             "\n\t\t\t}\n\t\t})")
                else:
                    class_variables_names.append(f'obj.{variable["name"]}')
                    class_file.write(f'\n\t\t.def_readwrite("{variable["name"]}", &{struct.full_name}::{variable["name"]})')
        return class_variables_names, class_variables

    def write_array(self, struct, class_file, variable, vector_types):


    def _write_vector(self, struct, class_file, variable, vector_types):
        full_declaration = linecache.getline(struct.file_name, variable["line_number"])
        sizes = self._get_sizes(full_declaration)
        characters = [chr(ord('i') + i) for i in range(len(sizes))]
        vector_types.append("std::vector<" * len(sizes) + self._structures_dictionary[variable['type']].full_name + '>' * len(sizes))
        self._write_for_loop_get(characters, variable, sizes, 0, class_file)
        class_file.write("\n\n")
        self._write_for_loop_set(characters, variable, sizes, 0, class_file)

    def _write_for_loop_get(self, characters, variable, sizes, call_index, file):
        loop_character = characters[call_index]
        file.write("\n\t\t" + call_index * '\t' + "std::vector<" * (len(sizes) - call_index) + variable['type'] + '>' * (
                    len(sizes) - call_index) + f" temp{call_index};")
        file.write(
            "\n\t\t" + call_index * '\t' + f"for (int {loop_character} = 0; {loop_character} < {sizes[call_index]}; {loop_character}++)")
        file.write("\n\t\t" + call_index * '\t' + "{")
        if call_index == len(sizes) - 1:
            file.write("\n\t\t" + (call_index + 1) * '\t')
            call_stack = ""
            for char in characters:
                call_stack += "[" + char + "]"
            file.write(f"temp{call_index}.push_back(&obj.{variable['name']}{call_stack});")
            file.write("\n\t\t" + call_index * '\t' + "}")
        else:
            self._write_for_loop_get(characters, variable, sizes, call_index + 1, file)
            file.write("\n\t\t" + (call_index + 1) * '\t' + f"temp{call_index}.push_back(temp{call_index + 1});")
            file.write("\n\t\t" + call_index * '\t' + "}")
            if call_index == 0:
                file.write("\n\t\t" + "return temp0;")

    def _write_for_loop_set(self, characters, variable, sizes, call_index, file):
        loop_character = characters[call_index]
        file.write(
            "\n\t\t" + call_index * '\t' + f"for (int {loop_character} = 0; {loop_character} < {sizes[call_index]}; {loop_character}++)")
        file.write("\n\t\t" + call_index * '\t' + "{")
        if call_index == len(sizes) - 1:
            call_stack = ""
            file.write("\n\t\t" + (call_index + 1) * '\t')
            for char in characters:
                call_stack += "[" + char + "]"
            file.write(f"obj.{variable['name']}{call_stack} = *setArr{call_stack};")
            file.write("\n\t\t" + call_index * '\t' + "}")
        else:
            self._write_for_loop_set(characters, variable, sizes, call_index + 1, file)
            file.write("\n\t\t" + call_index * '\t' + "}")

    def _get_sizes(self, full_declaration):
        sizes = list()
        while full_declaration.find("[") != -1:
            sizes.append(full_declaration[full_declaration.find("[") + 1:full_declaration.find("]")])
            full_declaration = full_declaration[full_declaration.find("]") + 1:]
        return sizes

    def write_topics(self):
        self._write_create_topic_name(self._topics_index_file, self._topics_file)
        for topic in self._topics_index_file.keys():
            self._write_smt_class(topic, self._topics_index_file[topic]["Data Size"])
            self.write_overload_smt_functions(topic)

    def _write_create_topic_name(self, topics, topics_file):
        self._topics_file.write("\nstd::map<std::string, std::array<uint32_t, 3>> getTopicsInfo()\n{\n")
        self._topics_file.write("std::map<std::string, std::array<uint32_t, 3>> topicsInfo;")
        for topic_name, topic_info in self._topics_index_file.items():
            self._topics_file.write(f'\n\ttopicsInfo["{topic_name}"] = '
                                    '{ '
                                    f'{topic_info["Data Size"]}, {topic_info["History Depth"]}, {topic_info["Cells Count"]}'
                                    '};')
        self._topics_file.write("\n\treturn topicsInfo;\n")
        self._topics_file.write(
            "struct topicsInfo\n{\n\tstatic std::map<std::string, std::array<uint32_t, 3>> topicsInfoMap;\n};\n")
        self._topics_file.write(
            "std::map<std::string, std::array<uint32_t, 3>> topicsInfo::topicsInfoMap = getTopicsInfo();\n")
        self._topics_file.write("bool SMT_CreateTopic(std::string topicName)\n{\n\t"
                                "if (topicsInfo::topicsInfoMap.find(topicName) == topicsInfo::topicsInfoMap.end())\n\t{"
                                '\n\t\tstd::cerr << "ERROR!! No topic named " + topicName << std::endl;\n\t\t'
                                'return false;\n\t}')
        self._topics_file.write("\n\telse\n\t{\n\t\tauto topic_info = topicsInfo::topicsInfoMap[topicName];\n\t\t"
                                "return SMT_CreateTopic(topicName.c_str(), topic_info[0], topic_info[1], topic_info[2]);\n\t}\n}")

    def _write_pack_class_pickle(self, class_file, class_variables, class_variables_names):
        for class_variable in class_variables:
            if len(class_variable) == 5:
                class_file.write(f"std::vector<std::vector<{class_variable[2]}>> {class_variable[1]};\n\t\t")
                class_file.write(f"for (int i = 0; i < {class_variable[3]}; i++)\n\t\t")
                class_file.write("{\n\t\t\t")
                class_file.write(f"std::vector<{class_variable[2]}> temp;\n\t\t\t")
                class_file.write(f"for (int j = 0; j < {class_variable[4]}; j++)\n\t\t\t")
                class_file.write("{\n\t\t\t\t")
                class_file.write(f"temp.push_back(obj.{class_variable[0]}[i][j]);")
                class_file.write("\n\t\t\t}\n\t\t\t")
                class_file.write(f"{class_variable[1]}.push_back(temp);")
                class_file.write("\n\t\t}")
            else:
                class_file.write(f"\n\t\tstd::vector<{class_variable[2]}> {class_variable[1]};\n\t\t")
                class_file.write(f"for (int i = 0; i < {class_variable[3]}; i++)\n\t\t")
                class_file.write("{\n\t\t\t")
                class_file.write(f"{class_variable[1]}.push_back(obj.{class_variable[0]}[i]);")
                class_file.write("\n\t\t}")
        class_file.write("\n\t\treturn py::make_tuple(")
        class_file.write(f"{','.join(class_variables_names)});\n")

    def _write_unpack_class_pickle(self, class_file, struct):
        tuple_index = 0
        for variable in struct.variables:
            type = variable["type"]
            if "struct " in type:
                type = type[type.find("struct ") + len("struct "):]
                if type in self._structures_dictionary.keys():
                    type = self._structures_dictionary[type].full_name
            if "enum" in variable.keys():
                type = variable["enum"]
            if variable["array"]:
                if "multi_dimensional_array" in variable.keys():
                    full_declaration = linecache.getline(struct.file_name, variable["line_number"])
                    first_size = full_declaration[
                                 full_declaration.find("[") + 1:full_declaration.find("]", full_declaration.find("["),
                                                                                      -1)]
                    second_size = full_declaration[full_declaration.rfind("[") + 1:full_declaration.rfind("]")]
                    class_file.write(
                        f'\n\t\tauto {variable["name"]}Vector = t[{tuple_index}].cast<std::vector<std::vector<{type}>>>();')
                    class_file.write(f"\n\t\tfor (int i = 0; i < {first_size}; i++)\n\t\t")
                    class_file.write("{\n\t\t\t")
                    class_file.write(f"for (int j = 0; j < {second_size}; j++)\n\t\t\t")
                    class_file.write("{\n\t\t\t\t")
                    class_file.write(f"obj.{variable['name']}[i][j] = {variable['name']}Vector[i][j];")
                    class_file.write("\n\t\t\t}\n\t\t}\n\t\t")
                else:
                    class_file.write(
                        f'\n\t\tauto {variable["name"]}Vector = t[{tuple_index}].cast<std::vector<{type}>>();')
                    class_file.write(f"\n\t\tfor (int i = 0; i < {variable['array_size']}; i++)\n\t\t")
                    class_file.write("{\n\t\t\t")
                    class_file.write(f"obj.{variable['name']}[i] = {variable['name']}Vector[i];")
                    class_file.write("\n\t\t}")
            else:
                class_file.write(f'\n\t\tobj.{variable["name"]} = t[{tuple_index}].cast<{type}>();')
            tuple_index += 1

    def write_overload_smt_functions(self, topic_name):
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
        with open("SharedMemoryTopics.h", "w") as shared_memory_topics_file:
            shared_memory_topics_file.write(f'\n\tpy::class_<{topic_name}>(SharedMemoryWrapperModule, "{topic_name}")')
            shared_memory_topics_file.write("\n\t\t.def(py::init<>())")
            [shared_memory_topics_file.write("\n\t\t" + smt_overload_function) for smt_overload_function in smt_overload_functions]
            shared_memory_topics_file.write(";\n}")

    def _write_smt_class(self, topic_name, topic_size):

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
        self._topics_file.write(f"class {topic_name}\n")
        self._topics_file.write("{\nprivate:\n\tstd::string _topicName;\n\tint _topicSize;\npublic:\n\t")
        self._topics_file.write(f'{topic_name}()\n\t')
        self._topics_file.write("{\n\t\t_topicName=")
        self._topics_file.write(f'"{topic_name}";\n\t\t_topicSize={topic_size};\n\t')
        self._topics_file.write("}\n")
        [self.write_function(smt_function_signature, smt_function_call) for smt_function_signature, smt_function_call in smt_functions_signature]
        self._topics_file.write("};\n")

    def write_enums_file(self, enums):
        with open("enums.h", "w") as enums_file:
            enums_file.write(f'#pragma once\n\n#include "{self._main_file[0]}"\n\n#include <pybind11/pybind11.h>\n\n#include <pybind11/stl.h>\n\n#include <pybind11/stl_bind.h>\n\n#include <iostream>\n\n')
            enums_file.write("namespace py = pybind11;\n\n")
            enums_file.write("void enumsRunner(py::module & SharedMemoryWrapperModule)\n\n{")
            for enum in enums:
                enums_file.write(f'\n\tpy::enum_<{enum["namespace"]}{enum["name"]}>(SharedMemoryWrapperModule, "{enum["name"]}")')
                for enum_value in enum["values"]:
                    enums_file.write(f'\n\t\t.value("{enum_value["name"]}", {enum["namespace"]}{enum_value["name"]})')
                enums_file.write(f'\n\t\t.export_values();\n')
            enums_file.write("}")

    def write_main_file_prefix(self, vectors_type, include_files):
        self._pybind_classes_file.close()
        with open("SharedMemoryWrapper.cpp", "r+") as main_file:
            content = main_file.read()
            main_file.seek(0, 0)
            main_file.write('#include "stdafx.h"\n\n')
            [main_file.write(include_path) for include_path in include_files]
            main_file.write('#include "Shared_Memory_Topics_API.h"\n\n'
                            '#include <pybind11\pybind11.h>\n\n#include <pybind11\stl.h>\n\n'
                            '#include <pybind11\stl_bind.h>\n\n#include <iostream>\n\n')
            main_file.write("namespace py = pybind11;\n\nPYBIND11_MODULE(SharedMemoryWrapper, SharedMemoryWrapperModule)\n{\n\t")
            for vector_type in vectors_type:
                main_file.write(f"PYBIND11_MAKE_OPAQUE(std::vector <{vector_type}>);")
                main_file.write("\n")
            generic_functions = ("SMT_Version", "SMT_Init", "SMT_Show", "SMT_CreateTopic",
                                 "SMT_GetPublishCount", "SMT_ClearHistory")
            main_file.write("PYBIND11_MODULE(SharedMemoryWrapper, SharedMemoryWrapperModule)\n{\n")
            for vector_type in vectors_type:
                main_file.write(f'py::bind_vector<std::vector<{vector_type}>>(SharedMemoryWrapperModule, "{vector_type}List");')
            for generic_function in generic_functions:
                self.write_generic_function(generic_function)
            main_file.write(content)

    def write_struct_class_prefix(self, struct):
        with open(f"{struct.name}Class.h", "w") as class_file:
            class_file.write(f'# pragma once\n\n#include "{self._main_file[0]}"\n\n#include "sharedMemoryTopics.h"\n\n'
                             '#include "Shared_Memory_Topics_API.h"\n\n'
                             '#include <pybind11\pybind11.h>\n\n#include <pybind11\stl.h>\n\n'
                             '#include <pybind11\stl_bind.h>\n\n#include <pybind11\\numpy.h>\n\n'
                             '#include <pybind11\pytypes.h>\n\n#include <iostream>\n\n'
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
