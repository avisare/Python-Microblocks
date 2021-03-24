import inspect


def wrapper_func(topic_name):
    setattr(hello, topic_name, test(topic_name))


class wrapper_class:
    def __init__(self, topic_name, name):
        self._topic_name = test(name)



class test:
    def __init__(self, name):
        self._name = name

    def print_name(self):
        print(self._name)
    def __call__(self):
        return self


class hello:
    def create_topic(self, topic_name):
        wrapper_func(topic_name)

x = hello()
x.create_topic("noder")
x.noder().print_name()





"""x = sharedMemoryWrapper()
topic = x.topicName()
topic.foo()"""