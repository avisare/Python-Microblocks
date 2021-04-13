import CppHeaderParser
import linecache
import functools


def write_for_loop_get(characters, array_type, variable_name, sizes, call_index, file, is_pickle):
    loop_character = characters[call_index]
    if call_index == 0 and is_pickle:
        file.write("\n\t\t" + call_index*'\t' + "std::vector<"*(len(sizes)-call_index) + array_type + '>'*(len(sizes) - call_index) + f" {variable_name}Vector;")
    else:
        file.write("\n\t\t" + call_index*'\t' + "std::vector<"*(len(sizes)-call_index) + array_type + '>'*(len(sizes) - call_index) + f" temp{call_index};")
    file.write("\n\t\t" + call_index*'\t' + f"for (int {loop_character} = 0; {loop_character} < {sizes[call_index]}; {loop_character}++)")
    file.write("\n\t\t" + call_index*'\t' + "{")
    if call_index == len(sizes) - 1:
        file.write("\n\t\t" + (call_index + 1) * '\t')
        call_stack = ""
        for char in characters:
            call_stack += "[" + char + "]"
        file.write(f"temp{call_index}.push_back(&obj.{variable_name}{call_stack});")
        file.write("\n\t\t" + call_index * '\t' + "}")
    else:
        write_for_loop_get(characters, array_type, variable_name, sizes, call_index + 1, file, is_pickle)
        if call_index == 0 and is_pickle:
            file.write("\n\t\t" + (call_index + 1) * '\t' + f"{variable_name}Vector.push_back(temp{call_index + 1});")
        else:
            file.write("\n\t\t" + (call_index+1) * '\t' + f"temp{call_index}.push_back(temp{call_index + 1});")
        file.write("\n\t\t" + call_index * '\t' + "}")
        if call_index == 0 and not is_pickle:
            file.write("\n\t\t" + "return temp0;")


def write_for_loop_set(characters, variable_name, sizes, call_index, file, is_pickle):
    loop_character = characters[call_index]
    file.write("\n\t\t" + call_index*'\t' + f"for (int {loop_character} = 0; {loop_character} < {sizes[call_index]}; {loop_character}++)")
    file.write("\n\t\t" + call_index*'\t' + "{")
    if call_index == len(sizes) - 1:
        call_stack = ""
        file.write("\n\t\t" + (call_index + 1)*'\t')
        for char in characters:
            call_stack += "[" + char + "]"
        if is_pickle:
            file.write(f"obj.{variable_name}{call_stack} = {variable_name}Vector{call_stack};")
        else:
            file.write(f"obj.{variable_name}{call_stack} = *setArr{call_stack};")
        file.write("\n\t\t" + call_index * '\t' + "}")
    else:
        write_for_loop_set(characters, variable_name, sizes, call_index + 1, file, is_pickle)
        file.write("\n\t\t" + call_index * '\t' + "}")


def write_set_array(characters, array_type, variable_name, sizes, call_index, file):
    loop_character = characters[call_index]
    file.write(
        "\n\t\t" + call_index * '\t' + f"for (int {loop_character} = 0; {loop_character} < {sizes[call_index]}; {loop_character}++)")
    file.write("\n\t\t" + call_index * '\t' + "{")
    if call_index == len(sizes) - 1:
        call_stack = ""
        for char in characters:
            call_stack += "[" + char + "]"
        file.write("\n\t\t" + (call_index + 1) * '\t')
        file.write(f"obj.{variable_name}{call_stack} = temp{call_index}[{loop_character}].cast<{array_type}>();")
        file.write("\n\t\t" + call_index * '\t' + "}")
    elif call_index == 0:
        file.write("\n\t\t" + (call_index + 1) * '\t')
        file.write(f"py::list temp{call_index} = setArr[{loop_character}].cast<py::list>();")
        write_set_array(characters, array_type, variable_name, sizes, call_index + 1, file)
        file.write("\n\t\t" + call_index * '\t' + "}")
    else:
        file.write("\n\t\t" + (call_index + 1) * '\t')
        file.write(f"py::list temp{call_index} = temp{call_index-1}[{loop_character}].cast<py::list>();")
        write_set_array(characters, array_type, variable_name, sizes, call_index + 1, file)
        file.write("\n\t\t" + call_index * '\t' + "}")


def get_sizes(full_declaration):
    sizes = list()
    while full_declaration.find("[") != -1:
        sizes.append(full_declaration[full_declaration.find("[")+1:full_declaration.find("]")])
        full_declaration = full_declaration[full_declaration.find("]")+1:]
    return sizes


def get_multiply(array_sizes, array_type):
    multiply_lst = list()
    index = 1
    for size in array_sizes:
        if size == array_sizes[-1]:
            multiply_lst.append(1)
        else:
            multiply_lst.append(functools.reduce(lambda a,b: int(a)*int(b), array_sizes[index:]))
        index += 1
    final_multiply = "{ "
    for multiply in multiply_lst:
        final_multiply += f"sizeof({array_type}) * {multiply}, "
    final_multiply += "}"
    final_multiply = final_multiply.replace(", }", " }")
    return final_multiply


def write_array(name, full_name, array_type, array_sizes, file):
    sizes = "{ " + ",".join(array_sizes) + " }"
    multipliers = get_multiply(array_sizes, array_type)
    file.write(f'\t\t.def_property("{name}", []({full_name}t & obj)->py::array')
    file.write("{\n\t\tauto dtype = "
               f"py::dtype(py::format_descriptor <{array_type}>::format());\n\t")
    file.write("\tauto base = py::array(dtype, {"
               f"{sizes}, "
               "}, "
               f"{multipliers});"
               "\n\t\treturn py::array(dtype, {"
               f"{sizes}"
               "}, "
               f"{multipliers})"
               ", "
               f"obj.{name}, base);\n")
    characters = [chr(ord('i') + i) for i in range(len(array_sizes))]
    write_set_array(characters, array_type, name, array_sizes, 0, file)
    write_pickle(full_name, array_sizes, array_type, name, file)


def write_pickle(full_name, array_sizes, array_type, name, file):
    file.write(f"\n\t\t.def(py::pickle(\n\t\t\t[](const {full_name} &obj)"
               "{")
    characters = [chr(ord('i') + i) for i in range(len(array_sizes))]
    write_for_loop_set(characters, name, array_sizes, 0, file, True)
    file.write("\n\t\t\t[](py::tuple t) {")
    write_for_loop_get(characters, array_type, name, array_sizes, 0, file, True)


def main():
    #header = CppHeaderParser.CppHeader("test.h")
    sizes = []
    print(testing("std::vector<std::vector<std::vector<g>>>"))
    print(testing("std::vector<std::vector<std::vector<std::vector<g>>>>"))
    print(testing("std::vector<std::vector<std::vector<std::vector<std::vector<g>>>>>"))
    """for struct_name, struct_content in header.classes.items():
        for variable in struct_content["properties"]["public"]:
            if variable['name'] == "test":
                full_declaration = linecache.getline("test.h", variable["line_number"])
                sizes = get_sizes(full_declaration)
                with open("test.txt", "w") as test:
                    write_array(variable['name'], "sm_data::" + variable['name'], variable['raw_type'], sizes, test)
                    characters = [chr(ord('i') + i) for i in range(len(sizes))]
                    variable['type'] = "sm_data::t*"
                    write_for_loop_get(characters, variable, sizes, 0, test)
                    test.write("\n\n")
                    write_for_loop_set(characters, variable, sizes, 0, test, True)"""


def testing(vector):
    inner_list = []
    while vector.count("std::vector") > 1:
        inner_list.append(vector[vector.find("std::vector") + len("std::vector") + 1:-1])
        vector = vector[vector.find("std::vector") + len("std::vector") + 1:-1]
    return inner_list

if __name__ == "__main__":
    main()

