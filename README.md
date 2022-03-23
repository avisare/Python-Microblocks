# Python-Microblocks

# Explanation
This parser should parse topics header files, into the ShaedMemoryWrapper python module.
In order to do so, the main script recursive_parser gets two arguments. 

## Base Directory
The first one is the base directory full path. base directory, it means the directory the includes all the 
topics header files, and also their include. In addition, for the parser would know how to get into relative included files,
it get to them from the base directory. It means that alll the relative includes are relative to the base directory.
In the base directory, should be another directory called collabs. In the collabs directory should find all the structs that you
want to create  on the python side. if there is an inner struct, that its decleration was not found in the collabs directory, the parser will
look for it in the includes of the file even if the file is not in the collabs directory.

## topics configuration file
The second argument being passed to the parser is the topics configuration file.
This file is a json configuration type file, which will include all the names of the topics 
you wish to create, and their details (Data Size, History Depth, Cells Count)
Example of topics configuration file:
{
  "SharedMemoryContentTopic": {
    "Data Size": 52,
    "History Depth": 3,
    "Cells Count": 10
  },
  "testStructOneTopic":{
    "Data Size": 25,
    "History Depth": 4,
    "Cells Count": 10
  },
  "testStructTwoTopic": {
    "Data Size": 52,
    "History Depth": 2,
    "Cells Count": 7
  },
  "testStructThreeTopic": {
    "Data Size": 40,
    "History Depth": 3,
    "Cells Count": 10
  },
  "testStructFourTopic": {
    "Data Size": 152,
    "History Depth": 5,
    "Cells Count": 12
  }
}

# Usage
In order to use the parser, just run the file recursive_parser
and as argument give it the base directory and the topics info json file.
After the parser produce the suitable files, you need to call to the auto_build_generator.py
script. This script will create the wanted .pyd file.

ATTENTION!!
Before using the script, you need to configure the environment variable to the following:
1. LIB = C:\Users\Administrator\AppData\Local\Programs\Python\Python38\libs(python 3.8 libs file);C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\lib\x64;;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\atlmfc\lib\x64;;
C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Auxiliary\VS\lib\x64;;C:\Program Files (x86)\Windows Kits\10\lib\10.0.16299.0\ucrt\x64;;;C:\Program Files (x86)\Windows Kits\10\lib\10.0.16299.0\um\x64;lib\um\x64;;C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6.1\Lib\um\x64
2. INCLUDE = C:\Users\Administrator\AppData\Local\Programs\Python\Python38\Lib\site-packages\pybind11\include(pybind include directory);C:\Users\Administrator\AppData\Local\Programs\Python\Python38\include(python include directory);
C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\include;;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\atlmfc\include;;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Auxiliary\VS\include;;
C:\Program Files (x86)\Windows Kits\10\Include\10.0.16299.0\ucrt;;;C:\Program Files (x86)\Windows Kits\10\Include\10.0.16299.0\um;C:\Program Files (x86)\Windows Kits\10\Include\10.0.16299.0\shared;C:\Program Files (x86)\Windows Kits\10\Include\10.0.16299.0\winrt;Include\um;
3. path environment variable should be the wanted path as default, but you should check it have the following at least
PATH = C:\windows\system32;C:\windows;C:\windows\System32\Wbem;C:\windows\System32\WindowsPowerShell\v1.0\;C:\windows\System32\OpenSSH\;C:\Program Files\Git\cmd;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\bin\HostX86\x64;
C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\bin\HostX86\x86;C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0\x86;;C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.6.1 Tools;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\Common7\tools;
C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\Common7\ide;C:\Program Files (x86)\HTML Help Workshop;;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\MSBuild\15.0\Bin;C:\windows\Microsoft.NET\Framework\v4.0.30319\;;C:\windows\system32;C:\windows;C:\windows\System32\Wbem;C:\windows\System32\WindowsPowerShell\v1.0\;
C:\windows\System32\OpenSSH\;C:\Program Files\Git\cmd;C:\Users\Administrator\AppData\Local\Programs\Python\Python38\Scripts\;C:\Users\Administrator\AppData\Local\Programs\Python\Python38\;"C:\Users\Administrator\AppData\Local\Programs\Python\Python39\Scripts;C:\Users\Administrator\AppData\Local\Programs\Python\Python39;
C:\Python27\Tools\Scripts;C:\Python27";C:\Python27\Tools\Scripts;;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\bin\HostX86\x64;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\bin\HostX86\x86;C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0\x86;
C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.6.1 Tools;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\Common7\tools;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\Common7\ide;C:\Program Files (x86)\HTML Help Workshop;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\MSBuild\15.0\Bin;
C:\windows\Microsoft.NET\Framework\v4.0.30319\;C:\windows\system32;C:\windows;C:\windows\System32\Wbem;C:\windows\System32\WindowsPowerShell\v1.0\;C:\windows\System32\OpenSSH\;C:\Program Files\Git\cmd;C:\Users\Administrator\AppData\Local\Programs\Python\Python38\Scripts\;C:\Users\Administrator\AppData\Local\Programs\Python\Python38\;
You should run the auto_build_generator.py script from the same diectory which all the files created by the parser are in.


# Usage Example
python recursive_parser.py C:\Users\Administrator\Documents\Python-Microblocks\test topics_info.json
python auto_build_generator.py