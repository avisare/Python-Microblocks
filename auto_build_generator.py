from os import getcwd
from subprocess import run


"""
This script have to be run from the same directory that the parser was run from
"""


def main():
    current_directory = getcwd()
    dll_file_path = current_directory + "\\DLL\\Shared_Memory_Topics_x64.dll"
    dll_path_dll = current_directory + "\\DLL"
    dll_path_headers = current_directory + "\\Headers"
    preparation_command = r""""C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\Common7\Tools\vsdevcmd.bat" & cd C:\Users\Administrator\Documents\Python-Microblocks & "C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\bin\HostX86\x64\CL.exe" /c /IC:\Users\Administrator\Documents\Python-Microblocks\DLL /IC:\Users\Administrator\Documents\Python-Microblocks\Headers /Zi /nologo /W3 /WX- /diagnostics:classic /sdl /O2 /Oi /GL /D NDEBUG /D _CONSOLE /D _WINDLL /D _UNICODE /D UNICODE /Gm- /EHsc /MD /GS /Gy /fp:precise /Zc:wchar_t /Zc:forScope /Zc:inline /Yc"stdafx.h" /Fp"x64\Release\SharedMemoryWrapper.pch" /Fo"x64\Release\\" /Fd"x64\Release\vc141.pdb" /Gd /TP /errorReport:prompt stdafx.cpp & """
    preparation_command = preparation_command.replace("dll_path_dll", dll_path_dll)
    preparation_command = preparation_command.replace("dll_path_headers", dll_path_headers)
    compile_command = r""""C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\bin\HostX86\x64\CL.exe" /c /Idll_path_dll /Idll_path_headers /Zi /nologo /W3 /WX- /diagnostics:classic /sdl /O2 /Oi /GL /D NDEBUG /D _CONSOLE /D _WINDLL /D _UNICODE /D UNICODE /Gm- /EHsc /MD /GS /Gy /fp:precise /Zc:wchar_t /Zc:forScope /Zc:inline /Yu"stdafx.h" /Fp"x64\Release\SharedMemoryWrapper.pch" /Fo"x64\Release\\" /Fd"x64\Release\vc141.pdb" /Gd /TP /errorReport:prompt SharedMemoryWrapper.cpp & """
    compile_command = compile_command.replace("dll_path_dll", dll_path_dll)
    compile_command = compile_command.replace("dll_path_headers", dll_path_headers)
    link_command = r""""C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\bin\HostX86\x64\link.exe" /ERRORREPORT:PROMPT /OUT:"current_directory_path\x64\Release\SharedMemoryWrapper.pyd" /INCREMENTAL:NO /NOLOGO /LIBPATH:dll_path_dll python38.lib Shared_Memory_Topics_x64.lib kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /MANIFEST /MANIFESTUAC:"level='asInvoker' uiAccess='false'" /manifest:embed /DEBUG /PDB:"/OUT:"current_directory_path\x64\Release\SharedMemoryWrapper.pdb" /SUBSYSTEM:CONSOLE /OPT:REF /OPT:ICF /LTCG:incremental /TLBID:1 /DYNAMICBASE /NXCOMPAT /IMPLIB:"/OUT:"current_directory_path\x64\Release\SharedMemoryWrapper.lib" /MACHINE:X64 /DLL x64\Release\SharedMemoryWrapper.obj x64\Release\stdafx.obj & """
    link_command = link_command.replace("current_directory_path", current_directory)
    link_command = link_command.replace("dll_path_dll", dll_path_dll)
    copy_command = r"""xcopy /y /d "dll_file_path" "current_directory_path\x64\Release\""""
    copy_command = copy_command.replace("dll_file_path", dll_file_path)
    copy_command = copy_command.replace("current_directory_path", current_directory)
    one_line_command = preparation_command +\
                       r"""PATH=C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\bin\HostX86\x64;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\bin\HostX86\x86;C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0\x86;;C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.6.1 Tools;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\Common7\tools;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\Common7\ide;C:\Program Files (x86)\HTML Help Workshop;;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\MSBuild\15.0\Bin;C:\windows\Microsoft.NET\Framework\v4.0.30319\;;C:\windows\system32;C:\windows;C:\windows\System32\Wbem;C:\windows\System32\WindowsPowerShell\v1.0\;C:\windows\System32\OpenSSH\;C:\Program Files\Git\cmd;C:\Users\Administrator\AppData\Local\Programs\Python\Python38\Scripts\;C:\Users\Administrator\AppData\Local\Programs\Python\Python38\;"C:\Users\Administrator\AppData\Local\Programs\Python\Python39\Scripts;C:\Users\Administrator\AppData\Local\Programs\Python\Python39;C:\Python27\Tools\Scripts;C:\Python27";C:\Python27\Tools\Scripts;; & """ +\
                       r"""set LIB=C:\Users\Administrator\AppData\Local\Programs\Python\Python38\libs;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\lib\x64;;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\atlmfc\lib\x64;;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Auxiliary\VS\lib\x64;;C:\Program Files (x86)\Windows Kits\10\lib\10.0.16299.0\ucrt\x64;;;C:\Program Files (x86)\Windows Kits\10\lib\10.0.16299.0\um\x64;lib\um\x64;;C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6.1\Lib\um\x64 & """ +\
                       r"""set INCLUDE=C:\Users\Administrator\AppData\Local\Programs\Python\Python38\Lib\site-packages\pybind11\include;C:\Users\Administrator\AppData\Local\Programs\Python\Python38\include;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\include;;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\atlmfc\include;;C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Auxiliary\VS\include;;C:\Program Files (x86)\Windows Kits\10\Include\10.0.16299.0\ucrt;;;C:\Program Files (x86)\Windows Kits\10\Include\10.0.16299.0\um;C:\Program Files (x86)\Windows Kits\10\Include\10.0.16299.0\shared;C:\Program Files (x86)\Windows Kits\10\Include\10.0.16299.0\winrt;Include\um; & """ +\
                       compile_command + link_command + copy_command
    run(one_line_command, shell=True)


if __name__ == "__main__":
    main()
