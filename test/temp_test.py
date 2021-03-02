from os import path


class test:
    def get_includes_recursive(self, includes, file_path):
        with open(file_path, "r") as sub_file:
            for line in sub_file:
                if "#include" in line:
                    include_file = line[line.find('#include "') + len('#include "'):line.rfind('"')]
                    if path.exists(include_file) and include_file not in includes:
                        includes.append(include_file)
                        self.get_includes_recursive(includes, include_file)

test_obj = test()
includes_list = []
test_obj.get_includes_recursive(includes_list, "example.h")
print(includes_list)