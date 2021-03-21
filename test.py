import CppHeaderParser

headers = CppHeaderParser.CppHeader("test.h")
enums_cpp_file = open("enums.cpp", "w")


def write_enums(enums):
    for enum in enums:
        for enum_value in enum["values"]:
            enums_cpp_file.write(f'\n\tSharedMemoryWrapperModule.def("{enum_value["name"]}", []() '
                                 '{return '
                                 f'{enum["namespace"]}{enum["name"]}::{enum_value["name"]}; '
                                 '});')


write_enums(headers.enums)