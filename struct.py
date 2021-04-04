

class Struct:
    def __init__(self, namespace, struct_name, variables, file):
        self.namespace = namespace
        self.name = struct_name
        self.variables = variables
        self.need_smt_functions = True
        self.inner_structs = []
        self.file_name = file
        if namespace == "":
            self.full_name = struct_name
        else:
            self.full_name = namespace + "::" + struct_name

