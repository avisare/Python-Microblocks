import SharedMemoryWrapper


def menu():
    option = '0'
    exit_program = False
    while not exit_program:
        option = '0'
        while not ('0'< option < '6'):
            print("Enter the option you want:")
            print("1. Run the demo test")
            print("2. Create and publish shared memory topic")
            print("3. Get shared memory by counter")
            print("4. Get shared latest shared memory")
            print("5. Exit")
            option = input()
            if option == '1':
                demo_test()
            elif option == '2':
                create_struct_option()
            elif option == '3':
                get_shared_memory_by_counter_option()
            elif option == '4':
                get_latest_shared_memory()
            else:
                exit_program = True


def demo_test():
    SharedMemoryWrapper.SMT_CreateTopic("SharedMemoryContent", 50, 2, 2)
    sharedMemoryObjectFirst = SharedMemoryWrapper.SharedMemoryContent()
    sharedMemoryObjectFirst.cstringData = "first"
    sharedMemoryObjectFirst.intData = 1111
    print(f"Created shared memory object with cstring data of '{sharedMemoryObjectFirst.cstringData}' and int data equal to {sharedMemoryObjectFirst.intData}")
    print("Create new topic in the shared memory library called SharedMemoryContentWrapper,\n"
          " with max data size of 50, history depth of 2 and 6 cells")
    sharedMemoryObjectSecond = SharedMemoryWrapper.SharedMemoryContent()
    sharedMemoryObjectSecond.cstringData = "second"
    sharedMemoryObjectSecond.intData = 2222
    print(f"Created another shared memory object with cstring data of '{sharedMemoryObjectSecond.cstringData}' and int data equal to {sharedMemoryObjectSecond.intData}")
    print("set the first object in the shared memory...")
    SharedMemoryWrapper.SMT_Publish(sharedMemoryObjectFirst)
    print("set the second object in the shared memory...")
    SharedMemoryWrapper.SMT_Publish(sharedMemoryObjectSecond)
    tempObject = SharedMemoryWrapper.SharedMemoryContent()
    tempObject.cstringData = "temp"
    tempObject.intData = 9999
    print(f"Create template object with cstring data of '{tempObject.cstringData}' and int value equal to {tempObject.intData}")
    SharedMemoryWrapper.SMT_GetByCounter(tempObject, 1, 30)
    print("Change the template object to contain the values of the first one")
    print(f"Now the template object contain cstring data of '{tempObject.cstringData}' and int data of {tempObject.intData}")
    SharedMemoryWrapper.SMT_GetLatest(tempObject)
    print("Change the template object to contain the values of the second one")
    print(f"Now the template object contain cstring data of '{tempObject.cstringData}' and int data is equal to {tempObject.intData}")


def create_struct_option():
    print("The optional structs to create are:")
    print("1. testStructOne - contains int, float and char")
    print("2. testStructThree - contains boolean and char array (string)")
    print("3. testStructFour - contains int, and int array")
    struct_to_create = input()
    if struct_to_create == '1':
        int_number = int(input("Enter integer"))
        float_number = float(input("Enter float number"))
        character = input("Enter character")
        structOneObject = SharedMemoryWrapper.testStructOne()
        structOneObject.intNumber = int_number
        structOneObject.floatNumber = float_number
        structOneObject.character = character
        print(f"Created new object with values of: {structOneObject.intNumber}, {structOneObject.floatNumber}, {structOneObject.character}")
        SharedMemoryWrapper.SMT_Publish(structOneObject)
    elif struct_to_create == '2':
        char_array = input("Your char array (max size of 32)")
        structThreeObject = SharedMemoryWrapper.testStructThree()
        structThreeObject.charArray = char_array
        structThreeObject.booleanValue = True
        print(f"Created new object with values of: {structThreeObject.booleanValue}, {structThreeObject.charArray}")
        SharedMemoryWrapper.SMT_Publish(structThreeObject)
    elif struct_to_create == '3':
        int_number = input("Enter integer")
        int_array = input("Enter integer array each integer seperate by space (size of 10)")
        int_array.split(" ")
        final_array = list(map(int, int_array))
        structFourObject = SharedMemoryWrapper.testStructFour()
        structFourObject.singleInteger = int_number
        structFourObject.intArray = final_array
        print(f"Created new object with values of: {structFourObject.singleInteger}, {structFourObject.intArray}")
        SharedMemoryWrapper.SMT_Publish(structFourObject)


def get_shared_memory_by_counter_option():
    print("Which kind of struct do you want to get:")
    print("1. testStructOne - contains int, float and char")
    print("2. testStructThree - contains boolean and char array (string)")
    print("3. testStructFour - contains int, and int array")
    struct_to_create = input()
    if struct_to_create == '1':
        structOneObject = SharedMemoryWrapper.testStructOne()
        SharedMemoryWrapper.SMT_GetByCounter(structOneObject, 1, 100)
        print(f"The new object contains: {structOneObject.intNumber}, {structOneObject.floatNumber}, {structOneObject.character}")
    elif struct_to_create == '2':
        structThreeObject = SharedMemoryWrapper.testStructThree()
        SharedMemoryWrapper.SMT_GetByCounter(structThreeObject, 1, 100)
        print(f"The new object contains: {structThreeObject.booleanValue}, {structThreeObject.charArray}")
    elif struct_to_create == '3':
        structFourObject = SharedMemoryWrapper.testStructFour()
        SharedMemoryWrapper.SMT_GetByCounter(structFourObject, 1, 100)
        print(f"The new object contains: {structFourObject.singleInteger}, {structFourObject.intArray}")


def get_latest_shared_memory():
    print("Which kind of struct do you want to get:")
    print("1. testStructOne - contains int, float and char")
    print("2. testStructThree - contains boolean and char array (string)")
    print("3. testStructFour - contains int, and int array")
    struct_to_create = input()
    if struct_to_create == '1':
        structOneObject = SharedMemoryWrapper.testStructOne()
        SharedMemoryWrapper.SMT_GetLatest(structOneObject)
        print(f"The new object contains: {structOneObject.intNumber}, {structOneObject.floatNumber}, {structOneObject.character}")
    elif struct_to_create == '2':
        structThreeObject = SharedMemoryWrapper.testStructThree()
        SharedMemoryWrapper.SMT_GetLatest(structThreeObject)
        print(f"The new object contains: {structThreeObject.booleanValue}, {structThreeObject.charArray}")
    elif struct_to_create == '3':
        structFourObject = SharedMemoryWrapper.testStructFour()
        SharedMemoryWrapper.SMT_GetLatest(structFourObject)
        print(f"The new object contains: {structFourObject.singleInteger}, {structFourObject.intArray}")


def main():
    print("Initialize the shared memory...")
    SharedMemoryWrapper.SMT_Init()
    SharedMemoryWrapper.SMT_CreateTopic("testStructOne", 20, 2, 6)
    SharedMemoryWrapper.SMT_CreateTopic("testStructFour", 40, 2, 6)
    SharedMemoryWrapper.SMT_CreateTopic("testStructThree", 50, 2, 6)
    menu()


if __name__ == "__main__":
    main()
