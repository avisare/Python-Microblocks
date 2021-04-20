import threading
import time


def foo():
    time.sleep(2)


t = threading.Thread(target=foo, name="noder")
t.start()
for thread in threading.enumerate():
    print(thread.name)