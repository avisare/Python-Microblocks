

class Struct:
    def __init__(self, namespace, struct_name, variables, have_wrapper, suffix, need_smt_functions, topic_name, struct_size):
        self.namespace = namespace
        self.name = struct_name
        self.variables = variables
        self.need_smt_functions = need_smt_functions
        self.have_wrapper = have_wrapper
        self.topic_name = topic_name
        self.struct_size = struct_size
        if have_wrapper:
            self.full_name = struct_name + suffix
        else:
            if suffix == "":
                self.full_name = struct_name
            else:
                self.full_name = suffix + "::" + struct_name

