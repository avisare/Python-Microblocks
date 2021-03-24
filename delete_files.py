import os


def delete_parser_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def delete_files():
    files_to_delete = ("testStructOneClass.h", "testStructTwoClass.h",
                       "testStructThreeClass.h", "testStructFourClass.h",
                       "SharedMemoryContentClass.h", "SharedMemoryWrapper.cpp", "SMT_DataInfoClass.h",
                       "classImplementationFile.cpp", "classDefinitionFile.h", "WrapperFunctionsFile.h",
                       "WrapperFunctions.h", "pybindClassesFile.cpp", "pybindClassesFile.h", "GenericWrapperHandler.h",
                       "GenericWrapperHandler.cpp", "sharedMemoryTopics.h", "enums.cpp", "enums.h", "NavCov_RecordClass.h",
                       "testClass.h")
    for file in files_to_delete:
        delete_parser_file(file)

delete_files()