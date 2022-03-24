import SharedMemoryWrapper


def main():
    myStruct = SharedMemoryWrapper.ComplexStruct()
    print("Inittalizing the struct")
    myStruct.Initalize()
    myStruct.charArray = "Hello World"
    print(f"The char array is equal to: {myStruct.charArray}")
    myStruct.charArray = "This string is bigger than the size of charArray"
    print(f"The char array is equal to: {myStruct.charArray}")
    myStruct.unsignedLong = 4294967294
    print(f"The unsinged long number is equal to: {myStruct.unsignedLong}")
    myStruct.float = 33.87
    print(f"The float number is equal to: {myStruct.float}")
    myStruct.cStr = "This is a c string"
    print(f"The c string is equal to: {myStruct.cStr}")
    myStruct.str = "This is a simple c++ string"
    print(f"The string is equal to: {myStruct.str}")
    myStruct.uint16Number = 65530
    print(f"The unsigned int 16 value is equal to: {myStruct.uint16Number}")
    myStruct.intValue = -80
    print(f"The int value of the pointer is {myStruct.intValue}")
    myStruct.boolean = True
    print(f"The boolean is equal to: {myStruct.boolean}")
    myStruct.char32 = "N"
    print(f"The char32 variable is equal to: {myStruct.char32}")
    myStruct.ssiNumber = 1234
    print(f"The short signed integer is equal to: {myStruct.ssiNumber}")


if __name__ == "__main__":
    main()




