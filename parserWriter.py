

class ParserWriter:
    def __init__(self, main_files):
        self._main_files = main_files
        self._structures = list()
        self._pybind_classes_file = open("SharedMemoryWrapper.cpp", "w")
        self._class_definition_file = open("GenericWrapperHandler.h", "w")
        self._class_implementation_file = open("GenericWrapperHandler.cpp", "w")
        self._topics_file = open("sharedMemoryTopics.h", "w")

    def set_structures(self, structures):
        self._structures = structures

    def write_includes(self, include_files):
        self._pybind_classes_file.close()
        self._class_definition_file.close()
        self._class_implementation_file.close()
        self._topics_file.close()
        outer_include_files = [f'#include "{include_file_path}"\n' for include_file_path in self._main_files]
        with open("SharedMemoryWrapper.cpp", "r+") as main_file:
            content = main_file.read()
            main_file.seek(0, 0)
            main_file.write('#include "stdafx.h"\n')
            [main_file.write(include_path) for include_path in include_files]
            main_file.write('#include "WrapperFunctions.h"\n\n'
                            '#include "Shared_Memory_Topics_API.h"\n\n#include "GenericWrapperHandler.h"\n\n'
                            '#include <pybind11\pybind11.h>\n\n#include <pybind11\stl.h>\n\n'
                            '#include <pybind11\stl_bind.h>\n\n#include <iostream>\n\n')
            main_file.write(content)
        with open("GenericWrapperHandler.cpp", "r+") as wrapper_class_implementation:
            content = wrapper_class_implementation.read()
            wrapper_class_implementation.seek(0, 0)
            wrapper_class_implementation.write('#include "stdafx.h"\n#include "GenericWrapperHandler.h"\n#include <iostream>\n')
            wrapper_class_implementation.write(content)

        with open("GenericWrapperHandler.h", "r+") as wrapper_functions_definition_file:
            content = wrapper_functions_definition_file.read()
            wrapper_functions_definition_file.seek(0, 0)
            wrapper_functions_definition_file.write(f'#pragma once\n{"".join(outer_include_files)}\n#include <pybind11/pybind11.h>\n#include <pybind11/stl.h>\n')
            wrapper_functions_definition_file.write(content)

        with open("sharedMemoryTopics.h", "r+") as shared_memory_topics_file:
            content = shared_memory_topics_file.read()
            shared_memory_topics_file.seek(0, 0)
            shared_memory_topics_file.write(f'#pragma once\n#include "Shared_Memory_Topics_API.h"\n#include <pybind11/pybind11.h>\n#include <pybind11/stl.h>\n#include <pybind11/stl_bind.h>\n#include <iostream>\n')
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
        with open(f"{struct.name}Class.h", "a") as class_file:
            class_file.write(f'\n\tpy::class_<{struct.full_name}>(SharedMemoryWrapperModule, "{struct.name}")\n')
            class_file.write(f"\t\t.def(py::init<>())")
            variable_functions = []
            for variable in struct.variables:
                if variable != "":
                    if "struct" in variable["type"]:
                        variable_functions.append(f'obj.get{variable["name"]}Const()')
                        class_file.write(
                            f'\n\t\t.def_property("{variable["name"]}", &{struct.full_name}::get{variable["name"]},'
                            f' &{struct.full_name}::set{variable["name"]}, py::return_value_policy::reference)')
                    elif variable["array"]:
                        variable_functions.append(f'obj.{variable["name"]}')
                        class_file.write(
                            f'\n\t\t.def_readwrite("{variable["name"]}", &{struct.full_name}::{variable["name"]})'
                        )
                    else:
                        variable_functions.append(f'obj.get{variable["name"]}()')
                        class_file.write(
                            f'\n\t\t.def_property("{variable["name"]}", &{struct.full_name}::get{variable["name"]},'
                            f' &{struct.full_name}::set{variable["name"]}, py::return_value_policy::copy)')

            class_file.write(f'\n\t\t.def(py::pickle(\n\t\t\t[](const {struct.full_name} &obj)')
            class_file.write("{\n\t\t\treturn py::make_tuple(")
            class_file.write(f"{','.join(variable_functions)});\n")
            class_file.write("\t\t},\n\t\t\t[](py::tuple t){")
            class_file.write(f"\n\t\t\t{struct.full_name} obj = {struct.full_name}();")
            tuple_index = 0
            for variable in struct.variables:
                if variable["array"]:
                    class_file.write(f'\n\t\t\tobj.{variable["name"]} = t[{tuple_index}].cast<std::vector<{variable["type"]}>>();')
                elif "struct" in variable["type"]:
                    inner_struct = self._find_struct(variable["type"][variable["type"].find("struct") + len("struct") + 1:])
                    if inner_struct is not None and inner_struct.have_wrapper:
                        class_file.write(f'\n\t\t\tobj.set{variable["name"]}(t[{tuple_index}].cast<{variable["type"][variable["type"].find("struct") + len("struct") + 1:]}Wrapper>());')
                    elif inner_struct is not None:
                        class_file.write(f'\n\t\t\tobj.set{variable["name"]}(t[{tuple_index}].cast<{variable["type"][variable["type"].find("struct") + len("struct") + 1:]}>());')
                    else:
                        print(f"Error occured, struct name {variable['type']} wasn't found")
                else:
                    class_file.write(f'\n\t\t\tobj.set{variable["name"]}(t[{tuple_index}].cast<{variable["type"]}>());')
                tuple_index += 1
            class_file.write("\n\t\t\treturn obj;\n\t\t}\n\t\t));\n")
            if not struct.need_smt_functions:
                class_file.write("}")
            else:
                self.write_overload_smt_functions(class_file, struct.topic_name)

    def write_pybind_class_without_wrappper(self, struct):
        with open(f"{struct.name}Class.h", "a") as class_file:
            class_file.write(f'\n\tpy::class_<{struct.full_name}>(SharedMemoryWrapperModule, "{struct.name}")\n')
            class_file.write(f"\t\t.def(py::init<>())")
            for variable in struct.variables:
                if variable != "":
                    class_file.write(
                        f'\n\t\t.def_readwrite("{variable["name"]}", &{struct.full_name}::{variable["name"]},'
                        f' py::return_value_policy::copy)')
            class_file.write(f'\n\t\t.def(py::pickle(\n\t\t\t[](const {struct.full_name} &obj)')
            class_file.write("{\n\t\t\treturn py::make_tuple(")
            class_file.write(f'{",".join(["obj." + variable["name"] for variable in struct.variables])});\n')
            class_file.write("\t\t},\n\t\t\t[](py::tuple t){")
            class_file.write(f"\n\t\t\t{struct.full_name} obj = {struct.full_name}();")
            tuple_index = 0
            for variable in struct.variables:
                class_file.write(f'\n\t\t\tobj.{variable["name"]} = t[{tuple_index}].cast<{variable["type"]}>();')
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
                                  f' py::overload_cast<void*&, '
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
             f'return SMT_GetByCounter("{struct.topic_name}", structObject, counter, timeout_us, &data_info);'),
            (f"GetByCounter(void* structObject, uint32_t counter, uint64_t timeout_us)",
             'SMT_DataInfo data_info = SMT_DataInfo{0,0,0};\n\t\t'
             f'return SMT_GetByCounter("{struct.topic_name}", structObject, counter, timeout_us, &data_info);'),
            (f"GetLatest(void* structObject, SMT_DataInfo& data_info)",
             f'return SMT_GetLatest("{struct.topic_name}", structObject, &data_info);'),
            (f"GetLatest(void* structObject)",
             'SMT_DataInfo data_info = SMT_DataInfo{0,0,0};\n\t\t'
             f'return SMT_GetLatest("{struct.topic_name}", structObject, &data_info);'),
            (f"Publish(void* structObject)",
             f'return SMT_Publish("{struct.topic_name}", structObject, {struct.struct_size});'),
            (f"Publish(void* structObject, size_t size)",
             f'return SMT_Publish("{struct.topic_name}", structObject, size);'),
            (f"GetOldest({struct.full_name}& structObject, SMT_DataInfo& data_info)",
             f'return SMT_GetOldest("{struct.topic_name}", structObject, &data_info);'),
            (f"GetOldest(void* structObject)",
             'SMT_DataInfo data_info = SMT_DataInfo{0,0,0};\n\t\t'
             f'return SMT_GetOldest("{struct.topic_name}", structObject, &data_info);')]
        self._topics_file.write(f"class {struct.topic_name}\n")
        self._topics_file.write("{\nprivate:\n\tstd::string _topicName\n\tint _topicSize;\npublic:\n\t")
        self._topics_file.write(f'{struct.topic_name}()\n\t')
        self._topics_file.write("{\n\t\t_topicName=")
        self._topics_file.write(f"{struct.topic_name}\n\t\t_topicSize={struct.struct_size}\n\t")
        self._topics_file.write("}\n")
        [self.write_function(smt_function_signature, smt_function_call) for smt_function_signature, smt_function_call in smt_functions_signature]
        self._topics_file.write("};\n")

    def write_update_functions_signatures(self, functions_signature):
        functions_signature.append(("void", "void updatePublish()"))
        self._class_definition_file.write(f"\t{functions_signature[-1][1]};\n")
        functions_signature.append(("void", "void updateGet()"))
        self._class_definition_file.write(f"\t{functions_signature[-1][1]};")

    def write_class_prefix(self, struct, functions_signature):
        class_name = struct.name + "Wrapper"
        self._class_definition_file.write(f"\nclass {class_name}\n")
        self._class_definition_file.write("{\npublic:\n\t")
        functions_signature.append(("", f"{class_name}()"))
        self._class_definition_file.write(f"{functions_signature[-1][1]};\n")

    def write_vector(self, vector_type, vector_name):
        self._class_definition_file.write(f"\n\tstd::vector<{vector_type}> {vector_name};")

    def write_inner_struct(self, functions_signature, inner_structs, variable):
        struct_wrapper_class = variable["type"][variable["type"].find("struct") + len("struct") + 1:] + "Wrapper"
        functions_signature.append((f"{struct_wrapper_class}&", f"{struct_wrapper_class}& get{variable['name']}()"))
        self._class_definition_file.write(f"\n\t{functions_signature[-1][1]};")
        functions_signature.append((f"{struct_wrapper_class}", f"{struct_wrapper_class} get{variable['name']}Const() const"))
        self._class_definition_file.write(f"\n\t{functions_signature[-1][1]};")
        functions_signature.append(("void", f"void set{variable['name']}({struct_wrapper_class} set{variable['name']})"))
        self._class_definition_file.write(f"\n\t{functions_signature[-1][1]};")
        inner_structs.append((struct_wrapper_class, variable['name']))

    def write_class_variable(self, functions_signature, variable):
        functions_signature.append((f"{variable['type']}",f"{variable['type']} get{variable['name']}() const"))
        self._class_definition_file.write(f"\n\t{functions_signature[-1][1]};")
        functions_signature.append(("void", f"void set{variable['name']}({variable['type']} setVar{variable['name']})"))
        self._class_definition_file.write(f"\n\t{functions_signature[-1][1]};")

    def write_get_class_pointer(self, struct, functions_signature):
        functions_signature.append((f'{struct.namespace}::{struct.name}*', f"{struct.namespace}::{struct.name}* get{struct.name}Ptr()"))
        self._class_definition_file.write(f"\n\t{functions_signature[-1][1]};")

    def write_class_private(self, struct):
        self._class_definition_file.write(f"\nprivate:\n\t{struct.namespace}::{struct.name} _{struct.name};\n")

    def write_inner_structs_variables(self, inner_structs):
        if len(inner_structs) > 0:
            [self._class_definition_file.write(f"\t{inner_struct[0]} _{inner_struct[1]};\n") for inner_struct in inner_structs]
        self._class_definition_file.write("};\n")

    def write_update_function_implementation(self, struct, function_name, vector_sizes, vector_names):
        self._class_implementation_file.write(f"{function_name}\n")
        self._class_implementation_file.write("{")
        if "Get" in function_name:
            for vector_name, vector_size in zip(vector_names, vector_sizes):
                self._class_implementation_file.write(f"\n\t{vector_name}.clear();")
                self._class_implementation_file.write(f"\n\tfor (int i = 0; i < {vector_size}; i++)\n\t")
                self._class_implementation_file.write("{\n\t\t")
                self._class_implementation_file.write(f"{vector_name}.push_back(_{struct.name}.{vector_name}[i]);\n\t")
                self._class_implementation_file.write("}")
            self._class_implementation_file.write("\n}\n")
        else:
            for vector_name, vector_size in zip(vector_names, vector_sizes):
                self._class_implementation_file.write(f"\n\tint max_index = ({vector_name}.size() >= {vector_size}) ? {vector_size} : {vector_name}.size();")
                self._class_implementation_file.write(f"\n\tfor (int i = 0; i < max_index; i++)\n\t")
                self._class_implementation_file.write("{\n\t\t")
                self._class_implementation_file.write(f"_{struct.name}.{vector_name}[i] = {vector_name}[i];\n\t")
                self._class_implementation_file.write("}")
            self._class_implementation_file.write("\n}\n")

    def write_function_signature(self, function_name):
        self._class_implementation_file.write(f"{function_name}\n")
        self._class_implementation_file.write("{\n\t")

    def write_set_function(self, struct, function_name):
        variable_name = function_name[function_name.find('set') + 3: function_name.find('(')]
        input_var_name = function_name[function_name.rfind(" ", function_name.find('('), -1):function_name.find(')')]
        if function_name.count("Wrapper") == 2:
            self._class_implementation_file.write(f"_{variable_name} ={input_var_name};\n")
        else:
            self._class_implementation_file.write(f"_{struct.name}.{variable_name} ={input_var_name};\n")
        self._class_implementation_file.write("}\n")

    def write_get_function(self, struct, function_name):
        variable_name = function_name[function_name.find('get') + 3: function_name.find('(')]
        return_type = function_name[:function_name.find(" ")].strip()
        if "Ptr" in function_name:
            self._class_implementation_file.write(f"return &_{struct.name};\n")
        elif "Const" in variable_name:
            self._class_implementation_file.write(f"return _{variable_name[:variable_name.find('Const')]};\n")
        elif function_name.count("Wrapper") == 2:
            self._class_implementation_file.write(f"return _{variable_name};\n")
        elif return_type == "float":
            self._class_implementation_file.write(f"return _{struct.name}.{variable_name};\n")
        else:
            self._class_implementation_file.write(f"return _{struct.name}.{variable_name};\n")
        self._class_implementation_file.write("}\n")

    def write_constructor(self, struct_name):
        class_name = struct_name + "Wrapper"
        self._class_implementation_file.write(f"{class_name}::{class_name}()\n")
        self._class_implementation_file.write("{\n\t")
        self._class_implementation_file.write(f"_{struct_name} = ")
        self._class_implementation_file.write("{};\n")
        self._class_implementation_file.write("}\n")

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
            class_file.write('# pragma once\n#include "sharedMemoryTopics.h"\n#include "WrapperFunctions.h"\n'
                             '#include "Shared_Memory_Topics_API.h"\n#include "GenericWrapperHandler.h"\n'
                             '#include <pybind11\pybind11.h>\n#include <pybind11\stl.h>\n'
                             '#include <pybind11\stl_bind.h>\n#include <iostream>\n'
                             f'namespace py = pybind11;\nvoid {struct.name}ClassRunner(py::module & SharedMemoryWrapperModule)\n'
                             '{\n')

    def write_class_call(self, structs):
        [self._pybind_classes_file.write(f"\n\n\t{struct.name}ClassRunner(SharedMemoryWrapperModule);") for struct in structs]

    def _find_struct(self, struct_name):
        for struct in self._structures:
            if struct.name == struct_name:
                return struct
        return None

    def write_file_ending(self):
        self._pybind_classes_file.write("\n}")

    def __del__(self):
        self._pybind_classes_file.close()
        self._class_definition_file.close()
        self._class_implementation_file.close()
        self._topics_file.close()
