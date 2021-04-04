from types import FunctionType

class topic:
    def __init__(self, topic_name):
        self.topic_name = topic_name


class test:
    def add_foo(self, name):
        f_code = compile(f'def get_topic(self): return(topic("{name}")) ', "<topic>", "exec")
        f_func = FunctionType(f_code.co_consts[0], globals(), "get_topic")
        setattr(test, name, f_func)
        #exec("""def get_topic(self):
         # return topic(name)""")
        #setattr(test, name, get_topic)



def foo(self):
    print(foo.__name__)

def main():
    t = test()
    t.add_foo("shalom")
    x = t.shalom()
    print(x.topic_name)
    #print(get_topic())

if __name__ == "__main__":
    main()