import SharedMemoryWrapper
import pickle
obj = SharedMemoryWrapper.SharedMemoryContent()
obj.cstringData = SharedMemoryWrapper.charList("abc")
obj.intData = 99
pickled_obj = pickle.dumps(obj)
x = pickle.loads(pickled_obj)
print(x.cstringData, x.intData)
