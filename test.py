import CppHeaderParser


def main():


    header = CppHeaderParser.CppHeader("C:\\Users\\Administrator\\Documents\\Python-Microblocks\\real_collab_test\\collabs\\SM_NavCovData.h")
    for struct_name, struct_content in header.classes.items():
        for var in struct_content["properties"]["public"]:
            if var["name"] == "spare":
                print(var['aliases'])
                print(var['aliases'][0] in fixed_width_integer_types)


if __name__ == "__main__":
    main()
