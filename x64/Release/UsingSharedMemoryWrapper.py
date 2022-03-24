import SharedMemoryWrapper


def main():
    print("Init the SMT...")
    print(SharedMemoryWrapper.SMT_Init())
    print("Create a shared memory wrapper object with Set 'first' as data...")
    SMWFirstObject = SharedMemoryWrapper.SharedMemoryContent(15, "first")
    print("set the shared memory with the object we created")
    SharedMemoryWrapper.setSharedMemoryContentMsg(SMWFirstObject)
    print("Create a shared memory wrapper object with Set 'Second' as data...")
    SMWSecondObject = SharedMemoryWrapper.SharedMemoryContent(15, "Second")
    print("set the shared memory with the object we created")
    SharedMemoryWrapper.setSharedMemoryContentMsg(SMWSecondObject)
    print("Create a shared memory wrapper object with 'Bad' as data...")
    SMWThirdObject = SharedMemoryWrapper.SharedMemoryContent(15, "Bad")
    print("Get the shared memory content of the first message with timeout of 100")
    print(SharedMemoryWrapper.getSharedMemoryContentMsg(SMWThirdObject, 100))
    print(f"The data in the third object created is {SMWThirdObject.getCstring()}")
    print("Get the latest message content to the third object")
    SharedMemoryWrapper.getLatestMsgContent(SMWThirdObject)
    print(f"The data in the third object created is {SMWThirdObject.getCstring()}")
    print("Show the SMT...")
    SharedMemoryWrapper.SMT_Show()


if __name__ == "__main__":
    main()

