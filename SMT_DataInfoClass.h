# pragma once
#include "WrapperFunctions.h"
#include "Shared_Memory_Topics_API.h"
#include "GenericWrapperHandler.h"
#include <pybind11\pybind11.h>
#include <pybind11\stl.h>
#include <pybind11\stl_bind.h>
#include <iostream>
namespace py = pybind11;
void SMT_DataInfoClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<SMT_DataInfo>(SharedMemoryWrapperModule, "SMT_DataInfo")
		.def(py::init<>())
		.def_readwrite("m_dataSize", &SMT_DataInfo::m_dataSize, py::return_value_policy::copy)
		.def_readwrite("m_publishCount", &SMT_DataInfo::m_publishCount, py::return_value_policy::copy)
		.def_readwrite("m_publishTime", &SMT_DataInfo::m_publishTime, py::return_value_policy::copy)
		.def(py::pickle(
			[](const SMT_DataInfo &obj){
			return py::make_tuple(obj.m_dataSize,obj.m_publishCount,obj.m_publishTime);
		},
			[](py::tuple t){
			SMT_DataInfo obj = SMT_DataInfo();
			obj.m_dataSize = t[0].cast<unsigned int>();
			obj.m_publishCount = t[1].cast<unsigned int>();
			obj.m_publishTime = t[2].cast<uint64_t>();
			return obj;
		}
		));
}