import SharedMemoryWrapper


def main():
    intinfo = SharedMemoryWrapper.intInfo()
    intinfo.singleInfo = 9
    intinfo.arrayInfo = [1, 2, 3, 4, 5]
    floatinfo = SharedMemoryWrapper.floatInfo(5.5, [1.1,2.2,3.3,4.4,5.5])
    generalInfo = SharedMemoryWrapper.Info(intinfo, floatinfo)
    print("printing integer info")
    SharedMemoryWrapper.printInfo(generalInfo.intinfo)
    print("printing floating info")
    SharedMemoryWrapper.printInfo(generalInfo.floatinfo)


if __name__ == "__main__":
    main()
