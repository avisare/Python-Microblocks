from os import getcwd
import subprocess

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
    compile_command = r""""C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\bin\HostX86\x64\CL.exe" /c /Idll_path_dll /Idll_path_headers /Zi /nologo /W3 /WX- /diagnostics:classic /sdl /O2 /Oi /GL /D NDEBUG /D _CONSOLE /D _WINDLL /D _UNICODE /D UNICODE /Gm- /EHsc /MD /GS /Gy /fp:precise /Zc:wchar_t /Zc:forScope /Zc:inline /Yu"stdafx.h" /Fp"x64\Release\SharedMemoryWrapper.pch" /Fo"x64\Release\\" /Fd"x64\Release\vc141.pdb" /Gd /TP /errorReport:prompt SharedMemoryWrapper.cpp"""
    compile_command = compile_command.replace("dll_path_dll", dll_path_dll)
    compile_command = compile_command.replace("dll_path_headers", dll_path_headers)
    link_command = r""""C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.11.25503\bin\HostX86\x64\link.exe" /ERRORREPORT:PROMPT /OUT:"current_directory_path\x64\Release\SharedMemoryWrapper.pyd" /INCREMENTAL:NO /NOLOGO /LIBPATH:dll_path_dll python38.lib Shared_Memory_Topics_x64.lib kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /MANIFEST /MANIFESTUAC:"level='asInvoker' uiAccess='false'" /manifest:embed /DEBUG /PDB:"/OUT:"current_directory_path\x64\Release\SharedMemoryWrapper.pdb" /SUBSYSTEM:CONSOLE /OPT:REF /OPT:ICF /LTCG:incremental /TLBID:1 /DYNAMICBASE /NXCOMPAT /IMPLIB:"/OUT:"current_directory_path\x64\Release\SharedMemoryWrapper.lib" /MACHINE:X64 /DLL x64\Release\SharedMemoryWrapper.obj x64\Release\stdafx.obj & """
    link_command = link_command.replace("current_directory_path", current_directory)
    link_command = link_command.replace("dll_path_dll", dll_path_dll)
    copy_command = r"""xcopy /y /d "dll_file_path" "current_directory_path\x64\Release\""""
    copy_command = copy_command.replace("dll_file_path", dll_file_path)
    copy_command = copy_command.replace("current_directory_path", current_directory)
    one_line_command = preparation_command + compile_command
    subprocess.run(one_line_command, shell=True)
    subprocess.run(link_command + copy_command, shell=True)


if __name__ == "__main__":
    main()
    