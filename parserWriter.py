import linecache
import functools
from json_python import JsonHelper


class ParserWriter:
    def __init__(self, main_files, topics_index_file):
        self._main_files = main_files
        self._topics_dictionary = JsonHelper.read_file(topics_index_file)
        self._structures = list()
        main_files = [f'#include "{main_file}"' for main_file in main_files]
        self._includes = "\n\n".join(main_files)
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
            includes = "".join(include_files)
            shared_memory_topics_file.write(f'#pragma once\n\n#pragma warning( disable:4267 )\n\n{includes}#include "Shared_Memory_Topics_API.h"\n\n#include <iostream>\n\n')
            shared_memory_topics_file.write(content)

    def write_generic_function(self, function_name, file):
        if function_name == "SMT_CreateTopic":
            file.write(
                f'\n\tSharedMemoryWrapperModule.def("{function_name}", py::overload_cast<std::string>(&{function_name}), py::return_value_policy::copy);\n')
            file.write(
                f'\n\tSharedMemoryWrapperModule.def("{function_name}", py::overload_cast<const char*, const uint32_t, const uint32_t, const uint32_t>(&{function_name}), py::return_value_policy::copy);\n')
        else:
            file.write(
                f'\n\tSharedMemoryWrapperModule.def("{function_name}", &{function_name}, py::return_value_policy::copy);\n')

    def write_topics_shared_memory(self):
        with open("smt.h", "w") as smt_file:
            self._write_smt_includes(smt_file)
            smt_file.write("namespace py = pybind11;\nvoid smtRunner(py::module & SharedMemoryWrapperModule)\n{\n")
            for topic in self._topics_dictionary.keys():
                if topic == "SMT_DataInfo":
                    continue
                self.write_overload_smt_functions(topic, smt_file)
                smt_file.write("\n\n")
            smt_file.write("\n}")

    def _write_smt_includes(self, smt_file):
        smt_file.write(
            f'#pragma once\n\n#include "sharedMemoryTopics.h"\n\n#include "Shared_Memory_Topics_API.h"\n\n#include <pybind11\pybind11.h>\n\n#include <iostream>\n\n')

    def write_function(self, function_signature, function_call):
        self._topics_file.write(f'\n\tbool {function_signature}\n\t')
        self._topics_file.write("{\n\t")
        self._topics_file.write(f"\t{function_call}\n\t")
        self._topics_file.write("}\n")

    def write_wrapper_pybind_class(self, struct, vector_types):
        with open(f"{struct.name}Class.h", "a") as class_file:
            class_file.write(f'\n\tpy::class_<{struct.full_name}>(SharedMemoryWrapperModule, "{struct.name}")\n')
            class_file.write(f"\t\t.def(py::init<>())\n")
            class_variables_names, class_variables = self._write_class_variables(class_file, struct, vector_types)
            class_file.write(f'\n\t.def(py::pickle(\n\t\t[](const {struct.full_name} &obj)')
            class_file.write("{\n\t\t")
            self._write_pack_class_pickle(class_file, class_variables, class_variables_names)
            class_file.write("\t},\n\t\t[](py::tuple t){")
            class_file.write(f"\n\t\t{struct.full_name} obj = {struct.full_name}();")
            self._write_unpack_class_pickle(class_file, struct)
            class_file.write("\n\t\treturn obj;\n\t}\n\t));\n")
            class_file.write("}")

    def _write_class_variables(self, class_file, struct, vector_types):
        class_variables_names = list()
        class_variables = list()
        for variable in struct.variables:
            if variable != "":
                if variable["array"]:
                    if len(variable['aliases']) > 0 and variable['typedef'] is None and "enum" not in variable.keys():
                        self._write_vector(struct, class_file, variable, vector_types)
                        full_declaration = linecache.getline(struct.file_name, variable["line_number"])
                        sizes = self._get_sizes(full_declaration)
                        class_variables_names.append(f'{variable["name"]}Vector')
                        class_variables.append((struct.full_name, sizes, self._structures_dictionary[variable['raw_type']].full_name, variable['name']))
                    else:
                        full_declaration = linecache.getline(struct.file_name, variable["line_number"])
                        sizes = self._get_sizes(full_declaration)
                        self._write_array(variable['name'], struct.full_name, variable['raw_type'], sizes, class_file)
                        class_variables_names.append(f'{variable["name"]}Vector')
                        class_variables.append((struct.full_name, sizes, variable['raw_type'], variable['name']))
                else:
                    class_variables_names.append(f'obj.{variable["name"]}')
                    class_file.write(f'\n\t\t.def_readwrite("{variable["name"]}", &{struct.full_name}::{variable["name"]})')
        return class_variables_names, class_variables

    def _get_multiply(self, array_sizes, array_type):
        multiply_lst = list()
        index = 1
        for size in array_sizes:
            if size == array_sizes[-1]:
                multiply_lst.append(1)
            else:
                multiply_lst.append(functools.reduce(lambda a, b: int(a) * int(b), array_sizes[index:]))
            index += 1
        final_multiply = "{ "
        for multiply in multiply_lst:
            final_multiply += f"sizeof({array_type}) * {multiply}, "
        final_multiply += "}"
        final_multiply = final_multiply.replace(", }", " }")
        return final_multiply

    def _write_array(self, name, full_name, array_type, array_sizes, file):
        sizes = "{ " + ",".join(array_sizes) + " }"
        multipliers = self._get_multiply(array_sizes, array_type)
        file.write(f'\n\t\t.def_property("{name}", []({full_name} & obj)->py::array')
        file.write("{\n\t\tauto dtype = "
                   f"py::dtype(py::format_descriptor<{array_type}>::format());\n\t")
        file.write(f"\tauto base = py::array(dtype, {sizes}, {multipliers});"
                   "\n\t\treturn py::array(dtype, "
                   f"{sizes}, {multipliers}, obj.{name}, base);\n")
        characters = [chr(ord('i') + i) for i in range(len(array_sizes))]
        file.write("\n\t}, []("
                   f"{full_name}& obj, py::list setArr)\n\t"
                   "{\n")
        self._write_set_array(characters, array_type, name, array_sizes, 0, file)
        file.write("\n\t})")

    def _write_pickle(self, array_sizes, array_type, name, file):
        characters = [chr(ord('i') + i) for i in range(len(array_sizes))]
        temp_type = array_type
        if "::" in array_type:
            temp_type = array_type[array_type.find("::") + 2:]
        if temp_type in self._structures_dictionary.keys():
            self._write_pickle_pack_structs_list(characters, name, array_sizes, 0, file)
        else:
            self._write_for_loop_get(characters, array_type, name, array_sizes, 0, file, True)

    def _write_vector(self, struct, class_file, variable, vector_types):
        full_declaration = linecache.getline(struct.file_name, variable["line_number"])
        sizes = self._get_sizes(full_declaration)
        characters = [chr(ord('i') + i) for i in range(len(sizes))]
        vector_types.add("std::vector<" * (len(sizes)-1) + self._structures_dictionary[variable['type']].full_name + '>'*(len(sizes) - 1))
        class_file.write(f'\n\t\t.def_property("{variable["name"]}", []({struct.full_name} &obj)->'
                         f'{"std::vector<" * len(sizes)}{self._structures_dictionary[variable["raw_type"]].full_name + "*"}{">" * len(sizes)}'
                         ' {')
        self._write_for_loop_get(characters, self._structures_dictionary[variable["raw_type"]].full_name + "*", variable['name'], sizes, 0, class_file, False)
        class_file.write("\n\n")
        class_file.write('\t}, '
                         f'[]({struct.full_name}& obj, {"std::vector<" * len(sizes)}{self._structures_dictionary[variable["raw_type"]].full_name + "*"}{">" * len(sizes)} setArr)'
                         '\n\t{')
        self._write_for_loop_set(characters, variable['name'], sizes, 0, class_file, False)
        class_file.write("\n\t})")

    def _write_for_loop_get(self, characters, array_type, variable_name, sizes, call_index, file, is_pickle):
        loop_character = characters[call_index]
        if call_index == 0 and is_pickle:
            file.write("\n\t\t" + call_index * '\t' + "std::vector<" * (len(sizes) - call_index) + array_type + '>' * (
                        len(sizes) - call_index) + f" {variable_name}Vector;")
        else:
            file.write("\n\t\t" + call_index * '\t' + "std::vector<" * (len(sizes) - call_index) + array_type + '>' * (
                        len(sizes) - call_index) + f" temp{call_index};")
        file.write(
            "\n\t\t" + call_index * '\t' + f"for (int {loop_character} = 0; {loop_character} < {sizes[call_index]}; {loop_character}++)")
        file.write("\n\t\t" + call_index * '\t' + "{")
        if call_index == len(sizes) - 1:
            file.write("\n\t\t" + (call_index + 1) * '\t')
            call_stack = ""
            for char in characters:
                call_stack += "[" + char + "]"
            if is_pickle:
                if call_index == 0:
                    file.write(f"{variable_name}Vector.push_back(obj.{variable_name}{call_stack});")
                else:
                    file.write(f"temp{call_index}.push_back(obj.{variable_name}{call_stack});")
            else:
                if call_index == 0:
                    file.write(f"{variable_name}Vector.push_back(&obj.{variable_name}{call_stack});")
                else:
                    file.write(f"temp{call_index}.push_back(&obj.{variable_name}{call_stack});")
            file.write("\n\t\t" + call_index * '\t' + "}")
        else:
            self._write_for_loop_get(characters, array_type, variable_name, sizes, call_index + 1, file, is_pickle)
            if call_index == 0 and is_pickle:
                file.write("\n\t\t" + (call_index + 1) * '\t' + f"{variable_name}Vector.push_back(temp{call_index + 1});")
            else:
                file.write("\n\t\t" + (call_index + 1) * '\t' + f"temp{call_index}.push_back(temp{call_index + 1});")
            file.write("\n\t\t" + call_index * '\t' + "}")
            if call_index == 0 and not is_pickle:
                file.write("\n\t\t" + "return temp0;")

    def _write_for_loop_set(self, characters, variable_name, sizes, call_index, file, is_pickle):
        loop_character = characters[call_index]
        file.write(
            "\n\t\t" + call_index * '\t' + f"for (int {loop_character} = 0; {loop_character} < {sizes[call_index]}; {loop_character}++)")
        file.write("\n\t\t" + call_index * '\t' + "{")
        if call_index == len(sizes) - 1:
            call_stack = ""
            file.write("\n\t\t" + (call_index + 1) * '\t')
            for char in characters:
                call_stack += "[" + char + "]"
            if is_pickle:
                file.write(f"obj.{variable_name}{call_stack} = {variable_name}Vector{call_stack};")
            else:
                file.write(f"obj.{variable_name}{call_stack} = *setArr{call_stack};")
            file.write("\n\t\t" + call_index * '\t' + "}")
        else:
            self._write_for_loop_set(characters, variable_name, sizes, call_index + 1, file, is_pickle)
            file.write("\n\t\t" + call_index * '\t' + "}")

    def _write_set_array(self, characters, array_type, variable_name, sizes, call_index, file):
        loop_character = characters[call_index]
        file.write(
            "\n\t\t" + call_index * '\t' + f"for (int {loop_character} = 0; {loop_character} < {sizes[call_index]}; {loop_character}++)")
        file.write("\n\t\t" + call_index * '\t' + "{")
        if call_index == len(sizes) - 1:
            call_stack = ""
            for char in characters:
                call_stack += "[" + char + "]"
            file.write("\n\t\t" + (call_index + 1) * '\t')
            if call_index == 0:
                file.write(f"obj.{variable_name}{call_stack} = setArr[{loop_character}].cast<{array_type}>();")
            else:
                file.write(f"obj.{variable_name}{call_stack} = temp{call_index-1}[{loop_character}].cast<{array_type}>();")
            file.write("\n\t\t" + call_index * '\t' + "}")
        elif call_index == 0:
            file.write("\n\t\t" + (call_index + 1) * '\t')
            file.write(f"py::list temp{call_index} = setArr[{loop_character}].cast<py::list>();")
            self._write_set_array(characters, array_type, variable_name, sizes, call_index + 1, file)
            file.write("\n\t\t" + call_index * '\t' + "}")
        else:
            file.write("\n\t\t" + (call_index + 1) * '\t')
            file.write(f"py::list temp{call_index} = temp{call_index - 1}[{loop_character}].cast<py::list>();")
            self._write_set_array(characters, array_type, variable_name, sizes, call_index + 1, file)
            file.write("\n\t\t" + call_index * '\t' + "}")

    def _get_sizes(self, full_declaration):
        sizes = list()
        while full_declaration.find("[") != -1:
            sizes.append(full_declaration[full_declaration.find("[") + 1:full_declaration.find("]")])
            full_declaration = full_declaration[full_declaration.find("]") + 1:]
        return sizes

    def write_topics(self):
        self._write_create_topic_name()
        for topic in self._topics_dictionary.keys():
            self._write_smt_class(topic, self._topics_dictionary[topic]["Data Size"])

    def _write_create_topic_name(self):
        self._topics_file.write("\nstd::map<std::string, std::array<uint32_t, 3>> getTopicsInfo()\n{\n")
        self._topics_file.write("\tstd::map<std::string, std::array<uint32_t, 3>> topicsInfo;")
        for topic_name, topic_info in self._topics_dictionary.items():
            self._topics_file.write(f'\n\ttopicsInfo["{topic_name}"] = '
                                    '{ '
                                    f'{topic_info["Data Size"]}, {topic_info["History Depth"]}, {topic_info["Cells Count"]}'
                                    '};')
        self._topics_file.write("\n\treturn topicsInfo;\n}\n")
        self._topics_file.write(
            "struct topicsInfo\n{\n\tstatic std::map<std::string, std::array<uint32_t, 3>> topicsInfoMap;\n};\n")
        self._topics_file.write(
            "std::map<std::string, std::array<uint32_t, 3>> topicsInfo::topicsInfoMap = getTopicsInfo();\n")
        self._topics_file.write("bool SMT_CreateTopic(std::string topicName)\n{\n\t"
                                "if (topicsInfo::topicsInfoMap.find(topicName) == topicsInfo::topicsInfoMap.end())\n\t{"
                                '\n\t\tstd::cerr << "ERROR!! No topic named " + topicName << std::endl;\n\t\t'
                                'return false;\n\t}')
        self._topics_file.write("\n\telse\n\t{\n\t\tauto topic_info = topicsInfo::topicsInfoMap[topicName];\n\t\t"
                                "return SMT_CreateTopic(topicName.c_str(), topic_info[0], topic_info[1], topic_info[2]);\n\t}\n}\n")

    def _write_pack_class_pickle(self, class_file, class_variables, class_variables_names):
        for class_variable in class_variables:
            self._write_pickle(class_variable[1], class_variable[2],
                               class_variable[3], class_file)
        class_file.write("\n\t\treturn py::make_tuple(")
        class_file.write(f"{','.join(class_variables_names)});\n")

    def _write_unpack_class_pickle(self, class_file, struct):
        tuple_index = 0
        for variable in struct.variables:
            unpacked = False
            is_basic_type_array = True
            type = variable["type"]
            if (len(variable['aliases']) > 0 and variable['typedef'] is None and "enum" not in variable.keys()) or "struct" in type:
                is_basic_type_array = False
                if "struct" in type:
                    type = type[type.find("struct ") + len("struct "):]
                if type in self._structures_dictionary.keys():
                    type = self._structures_dictionary[type].full_name
                if variable["array"]:
                    full_declaration = linecache.getline(struct.file_name, variable["line_number"])
                    sizes = self._get_sizes(full_declaration)
                    class_file.write(f"\n\t\tauto {variable['name']}lst0 = t[{tuple_index}].cast<py::list>();")
                    characters = [chr(ord('i') + i) for i in range(len(sizes))]
                    self._write_pickle_unpack_structs_list(characters, variable['name'], type, sizes, 0, class_file)
                    unpacked = True
            if "enum" in variable.keys():
                type = variable["enum"]
            if variable["array"] and is_basic_type_array:
                full_declaration = linecache.getline(struct.file_name, variable["line_number"])
                sizes = self._get_sizes(full_declaration)
                if variable['raw_type'] in self._structures_dictionary.keys():
                    class_file.write(
                        f'\n\t\tauto {variable["name"]}Vector = t[{tuple_index}].cast<{"std::vector<" * len(sizes) + self._structures_dictionary[variable["raw_type"]].full_name + ">" * len(sizes)}>();')
                else:
                    class_file.write(
                        f'\n\t\tauto {variable["name"]}Vector = t[{tuple_index}].cast<{"std::vector<" * len(sizes) + variable["raw_type"] + ">" * len(sizes)}>();')
                characters = [chr(ord('i') + i) for i in range(len(sizes))]
                self._write_for_loop_set(characters, variable['name'], sizes, 0, class_file, True)
            else:
                if not unpacked:
                    class_file.write(f'\n\t\tobj.{variable["name"]} = t[{tuple_index}].cast<{type}>();')
            tuple_index += 1

    def _write_pickle_pack_structs_list(self, characters, array_name, array_sizes, call_index, file):
        if call_index == len(array_sizes):
            call_stack = ""
            for char in characters:
                call_stack += "[" + char + "]"
            if call_index == 1:
                file.write("\n\t\t" + '\t'*call_index + f"{array_name}Vector.append(obj.{array_name}{call_stack});")
            else:
                file.write("\n\t\t" + '\t'*call_index + f"lst{call_index-1}.append(obj.{array_name}{call_stack});")
            file.write("\n\t\t" + '\t'*(call_index-1) + "}")
        else:
            if call_index == 0:
                file.write(f"\n\t\t" + '\t'*call_index + f"py::list {array_name}Vector;")
                file.write(f"\n\t\t" + '\t' * call_index + f"for(int {characters[call_index]} = 0; {characters[call_index]} < {array_sizes[call_index]}; {characters[call_index]}++)")
                file.write(f"\n\t\t" + '\t' * call_index + "{")
                self._write_pickle_pack_structs_list(characters, array_name, array_sizes, call_index + 1, file)
                file.write("\n\t\t" + '\t'*(call_index+1) + f"{array_name}Vector.append(lst{call_index + 1});")
                file.write("\n\t\t" + '\t' * call_index + "}")
            else:
                file.write(f"\n\t\t" + '\t'*call_index + f"py::list lst{call_index};")
                file.write(f"\n\t\t" + '\t'*call_index + f"for(int {characters[call_index]} = 0; {characters[call_index]} < {array_sizes[call_index]}; {characters[call_index]}++)")
                file.write(f"\n\t\t" + '\t' * call_index + "{")
                self._write_pickle_pack_structs_list(characters, array_name, array_sizes, call_index+1, file)
                if call_index != 1:
                    file.write("\n\t\t" + '\t'*call_index + f"lst{call_index}.append(lst{call_index+1})")
                    file.write("\n\t\t" + '\t' * call_index + "}")

    def _write_pickle_unpack_structs_list(self, characters, array_name, array_type, array_sizes, call_index, file):
        if call_index + 1 == len(array_sizes):
            call_stack = ""
            for char in characters:
                call_stack += "[" + char + "]"
            file.write("\n\t\t" + '\t' * call_index + f"for (int {characters[call_index]} = 0; {characters[call_index]} < {array_sizes[call_index]}; {characters[call_index]}++)")
            file.write("\n\t\t" + '\t' * call_index + "{")
            file.write("\n\t\t" + '\t'*(call_index + 1) + f"obj.{array_name}{call_stack} = {array_name}lst{call_index}[{characters[call_index]}].cast<{array_type}>();")
            file.write("\n\t\t" + '\t' * call_index + "}")
        else:
            file.write("\n\t\t" + '\t' * call_index + f"for (int {characters[call_index]} = 0; {characters[call_index]} < {array_sizes[call_index]}; {characters[call_index]}++)")
            file.write("\n\t\t" + '\t' * call_index + "{")
            file.write("\n\t\t" + '\t'*(call_index + 1) + f"auto {array_name}lst{call_index+1} = {array_name}lst{call_index}[{characters[call_index]}].cast<py::list>();")
            self._write_pickle_unpack_structs_list(characters, array_name, array_type, array_sizes, call_index+1, file)
            file.write("\n\t\t" + '\t' * call_index + "}")

    def write_overload_smt_functions(self, topic_name, shared_memory_topics_file):
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
        shared_memory_topics_file.write(f'\n\tpy::class_<{topic_name}>(SharedMemoryWrapperModule, "{topic_name}")')
        shared_memory_topics_file.write("\n\t\t.def(py::init<>())")
        [shared_memory_topics_file.write("\n\t\t" + smt_overload_function) for smt_overload_function in smt_overload_functions]
        shared_memory_topics_file.write(";")

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
            enums_file.write(f'#pragma once\n\n{self._includes}\n\n#include <pybind11/pybind11.h>\n\n#include <pybind11/stl.h>\n\n#include <pybind11/stl_bind.h>\n\n#include <iostream>\n\n')
            enums_file.write("namespace py = pybind11;\n\n")
            enums_file.write("void enumsRunner(py::module & SharedMemoryWrapperModule)\n\n{")
            for enum in enums:
                enums_file.write(f'\n\tpy::enum_<{enum["namespace"]}{enum["name"]}>(SharedMemoryWrapperModule, "{enum["name"]}")')
                for enum_value in enum["values"]:
                    enums_file.write(f'\n\t\t.value("{enum_value["name"]}", {enum["namespace"]}{enum_value["name"]})')
                enums_file.write(f'\n\t\t.export_values();\n')
            enums_file.write("}")

    def write_smt_data_class(self):
        with open("SMT_DataInfoClass.h", "w") as data_info_file:
            content = r"""# pragma once

includes_files

#include "sharedMemoryTopics.h"

#include "Shared_Memory_Topics_API.h"

#include <pybind11\pybind11.h>

#include <pybind11\stl.h>

#include <pybind11\stl_bind.h>

#include <pybind11\numpy.h>

#include <pybind11\pytypes.h>

#include <iostream>

namespace py = pybind11;
void SMT_DataInfoRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<SMT_DataInfo>(SharedMemoryWrapperModule, "SMT_DataInfo")
		.def(py::init<>())
		.def_readwrite("m_dataSize", &SMT_DataInfo::m_dataSize)
		.def_readwrite("m_publishCount", &SMT_DataInfo::m_publishCount)
		.def_readwrite("m_publishTime", &SMT_DataInfo::m_publishTime)
		.def(py::pickle(
			[](const ::SMT_DataInfo &obj) {

		return py::make_tuple(obj.m_dataSize, obj.m_publishCount, obj.m_publishTime);
	},
			[](py::tuple t) {
		SMT_DataInfo obj = SMT_DataInfo();
		obj.m_dataSize = t[0].cast<unsigned int>();
		obj.m_publishCount = t[1].cast<unsigned int>();
		obj.m_publishTime = t[2].cast<uint64_t>();
		return obj;
	}
	));
}"""
            content = content.replace("includes_files", self._includes)
            data_info_file.write(content)

    def write_main_file_prefix(self, vectors_type, include_files):
        self._pybind_classes_file.close()
        with open("SharedMemoryWrapper.cpp", "r+") as main_file:
            content = main_file.read()
            main_file.seek(0, 0)
            main_file.write('#include "stdafx.h"\n\n#include "smt.h"\n\n#include "SMT_DataInfoClass.h"\n\n')
            [main_file.write(include_path) for include_path in include_files]
            main_file.write('#include "SharedMemoryTopics.h"\n\n#include "Shared_Memory_Topics_API.h"\n\n'
                            '#include <pybind11\pybind11.h>\n\n#include <pybind11\stl.h>\n\n'
                            '#include <pybind11\stl_bind.h>\n\n#include <iostream>\n\n')
            main_file.write("namespace py = pybind11;\n\n")
            all_vector_types = []
            for vector_type in vectors_type:
                main_file.write("\n")
                main_file.write(f"PYBIND11_MAKE_OPAQUE(std::vector<{vector_type}>);\n")
                vector_inner_types = self._get_inner_types_vector("std::vector<" + vector_type + ">")
                for inner_type in vector_inner_types:
                    main_file.write(f"PYBIND11_MAKE_OPAQUE({inner_type});\n")
                    all_vector_types.append("std::vector<" + inner_type + ">")
                all_vector_types.append(vector_type)
            main_file.write("PYBIND11_MODULE(SharedMemoryWrapper, SharedMemoryWrapperModule)\n{\n")
            for vector_type in all_vector_types:
                if "<" in inner_type:
                    inner_type = vector_type[vector_type.rfind("<") + 1:vector_type.find(">")]
                if "::" in inner_type:
                    inner_type = inner_type[inner_type.find("::") + 2:]
                dimensions = vector_type.count("std::vector")
                main_file.write(f'\n\tpy::bind_vector<{vector_type}>(SharedMemoryWrapperModule, "{inner_type}{dimensions}");')
            generic_functions = ("SMT_Version", "SMT_Init", "SMT_Show", "SMT_CreateTopic",
                                 "SMT_GetPublishCount", "SMT_ClearHistory")
            for generic_function in generic_functions:
                self.write_generic_function(generic_function, main_file)
            main_file.write(content)

    def _get_inner_types_vector(self, vector_type):
        inner_types = []
        while vector_type.count("std::vector") > 1:
            inner_types.append(vector_type[vector_type.find("std::vector") + len("std::vector") + 1:-1])
            vector_type = vector_type[vector_type.find("std::vector") + len("std::vector") + 1:-1]
        return inner_types

    def write_struct_class_prefix(self, struct):
        with open(f"{struct.name}Class.h", "w") as class_file:
            class_file.write(f'# pragma once\n\n{self._includes}\n\n#include "sharedMemoryTopics.h"\n\n'
                             '#include "Shared_Memory_Topics_API.h"\n\n'
                             '#include <pybind11\pybind11.h>\n\n#include <pybind11\stl.h>\n\n'
                             '#include <pybind11\stl_bind.h>\n\n#include <pybind11\\numpy.h>\n\n'
                             '#include <pybind11\pytypes.h>\n\n#include <iostream>\n\n'
                             f'namespace py = pybind11;\nvoid {struct.name}ClassRunner(py::module & SharedMemoryWrapperModule)\n'
                             '{\n')

    def write_class_call(self, structs, enums):
        self._pybind_classes_file.write("\n\n\tsmtRunner(SharedMemoryWrapperModule);")
        self._pybind_classes_file.write("\n\n\tSMT_DataInfoRunner(SharedMemoryWrapperModule);")
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
