# Python-Microblocks

# Explanation
This parser should parse one header file, In this example
SharedMemoryContent.h into a couple of output files, that will
contain the WrapperFunctionsFile.h - file that contain the implementation
of the microblocks functions lik publish, getByCounter, etc...
structNameClass.h file for each struct in the main header file. This file
will contain the call and the binding for each python and cpp function
of the class. all this files will be called from the main file named
pybindClassesFile. The file classDefinitionFile.h will contain all the wrapper
classes definitions, and the file classImplementationFile, will contain al the implementation 
of the functions.

# Usage
In order to use the parser, just run the file recursive_parser
and as argument give it the header file name