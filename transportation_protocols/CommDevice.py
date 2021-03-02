

class CommDeviceMeta(type):
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'send') and
                callable(subclass.send) and
                hasattr(subclass, 'receive') and
                callable(subclass.receive))


class CommDeviceInterface(metaclass=CommDeviceMeta):
    def send(self, message):
        pass

    def receive(self, buffer_size: 'int', timeout: 'float' = None):
        pass
