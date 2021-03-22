

class Struct:
    def __init__(self, namespace, struct_name, variables, suffix, need_smt_functions, topic_name, struct_size, file):
        self.namespace = namespace
        self.name = struct_name
        self.variables = variables
        self.need_smt_functions = need_smt_functions
        self.topic_name = topic_name
        self.struct_size = struct_size
        self.inner_structs = []
        self.file_name = file
        if suffix == "":
            self.full_name = struct_name
        else:
            self.full_name = suffix + "::" + struct_name

