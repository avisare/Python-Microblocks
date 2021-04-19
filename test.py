def main():
    with open("SMT_DataInfoClass.h", "w") as data_info_file:
        data_info_file.write(r"""# pragma once

#include "SharedMemoryStructs.h"

#include "sharedMemoryTopics.h"

#include "Shared_Memory_Topics_API.h"

#include <pybind11\pybind11.h>

#include <pybind11\stl.h>

#include <pybind11\stl_bind.h>

#include <pybind11\numpy.h>

#include <pybind11\pytypes.h>

#include <iostream>

namespace py = pybind11;
void SMT_DataInfoClassRunner(py::module & SharedMemoryWrapperModule)
{

    py::class_<SMT_DataInfo>(SharedMemoryWrapperModule, "SMT_DataInfo")
        .def(py::init<>())
        .def_readwrite("m_dataSize", &SMT_DataInfo::m_dataSize)
        .def_readwrite("m_publishCount", &SMT_DataInfo::m_publishCount)
        .def_readwrite("m_publishTime", &SMT_DataInfo::m_publishTime)
        .def(py::pickle(
            [](const ::SMT_DataInfo &obj) {

        return py::make_tuple(obj.m_dataSize, obj.m_publishCount, obj.m_publishTime);
    },
            [](py::tuple t) {
        SMT_DataInfo obj = SMT_DataInfo();
        obj.m_dataSize = t[0].cast<unsigned int>();
        obj.m_publishCount = t[1].cast<unsigned int>();
        obj.m_publishTime = t[2].cast<uint64_t>();
        return obj;
    }
    ));
}""")

if __name__ == "__main__":
    main()