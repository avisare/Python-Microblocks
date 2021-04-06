import CppHeaderParser
import linecache


def write_for_loop_get(characters, variable, sizes, call_index, file):
    loop_character = characters[call_index]
    print(len(sizes) - call_index)
    file.write("\n" + call_index*'\t' + "std::vector<"*(len(sizes)-call_index) + variable['type'] + '>'*(len(sizes)-call_index) + f" temp{call_index};")
    file.write("\n" + call_index*'\t' + f"for (int {loop_character} = 0; {loop_character} < {sizes[call_index]}; {loop_character}++)")
    file.write("\n" + call_index*'\t' + "{")
    if call_index == len(sizes) - 1:
        file.write("\n" + (call_index + 1) * '\t')
        call_stack = ""
        for char in characters:
            call_stack += "[" + char + "]"
        file.write(f"temp{call_index}.push_back(&obj.{variable['name']}{call_stack});")
        file.write("\n" + call_index * '\t' + "}")
    else:
        write_for_loop_get(characters, variable, sizes, call_index + 1, file)
        file.write("\n" + (call_index+1) * '\t' + f"temp{call_index}.push_back(temp{call_index + 1});")
        file.write("\n" + call_index * '\t' + "}")
        if call_index == 0:
            file.write("\n" + "return temp0;")


def write_for_loop_set(characters, variable, sizes, call_index, file):
    loop_character = characters[call_index]
    file.write("\n" + call_index*'\t' + f"for (int {loop_character} = 0; {loop_character} < {sizes[call_index]}; {loop_character}++)")
    file.write("\n" + call_index*'\t' + "{")
    if call_index == len(sizes) - 1:
        call_stack = ""
        file.write("\n" + (call_index + 1)*'\t')
        for char in characters:
            call_stack += "[" + char + "]"
        file.write(f"obj.{variable['name']}{call_stack} = *setArr{call_stack};")
        file.write("\n" + call_index * '\t' + "}")
    else:
        write_for_loop_set(characters, variable, sizes, call_index + 1, file)
        file.write("\n" + call_index * '\t' + "}")


def get_sizes(full_declaration):
    sizes = list()
    while full_declaration.find("[") != -1:
        sizes.append(full_declaration[full_declaration.find("[")+1:full_declaration.find("]")])
        full_declaration = full_declaration[full_declaration.find("]")+1:]
    return sizes


"""def main():
    header = CppHeaderParser.CppHeader("test.h")
    sizes = []
    for struct_name, struct_content in header.classes.items():
        for variable in struct_content["properties"]["public"]:
            if variable['name'] == "test":
                full_declaration = linecache.getline("test.h", variable["line_number"])
                sizes = get_sizes(full_declaration)
                with open("test.txt", "w") as test:
                    characters = [chr(ord('i') + i) for i in range(len(sizes))]
                    variable['type'] = "sm_data::t*"
                    write_for_loop_get(characters, variable, sizes, 0, test)
                    test.write("\n\n")
                    write_for_loop_set(characters, variable, sizes, 0, test)"""

def main(name, full_name, type, array_size):
    with open("test.h", "w") as test:
        test.write(f'.def_property("{name}", []({full_name}t & obj)->py::array')
        test.write("{\n\tauto dtype = "
                   f"py::dtype(py::format_descriptor <{type}>::format());\n\t"
        test.write("auto base = py::array(dtype, {"
                   f"{array_size}, "
                   "}, {sizeof("
                   f"{array_size}"
                   "});\nreturn py::array(dtype, {"
                   f"{array_size}"
                   "}, {sizeof({"
                   f"{type})"
                   "}, "
                   f"obj.{name}, base);\n"
        test.write("}, "
                   f"[]({full_name} & obj, py::list setArr"))
    {
    for (int i = 0; i < CSTRING_DATA_MAX_LEN; i++)
        {
            obj.cstringData[i] = setcstringData[i].cast < char > ();
        }
        })
if __name__ == "__main__":
    main()

