# pragma once

#include "SharedMemoryContent.h"

#include "sharedMemoryTopics.h"

#include "Shared_Memory_Topics_API.h"

#include <pybind11\pybind11.h>

#include <pybind11\stl.h>

#include <pybind11\stl_bind.h>

#include <pybind11\numpy.h>

#include <pybind11\pytypes.h>

#include <iostream>

namespace py = pybind11;
void SharedMemoryContentClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::SharedMemoryContent>(SharedMemoryWrapperModule, "SharedMemoryContent")
		.def(py::init<>())
		.def_readwrite("intData", &sm_data::SharedMemoryContent::intData)
		.def_property("cstringData", [](sm_data::SharedMemoryContent &obj)->py::array {
		auto dtype = py::dtype(py::format_descriptor<char>::format());
		auto base = py::array(dtype, { CSTRING_DATA_MAX_LEN }, { sizeof(char) });
		return py::array(dtype, {CSTRING_DATA_MAX_LEN }, { sizeof(char) }, obj.cstringData, base);
		},[](sm_data::SharedMemoryContent& obj, py::list setcstringData)
		{
			for (int i = 0; i < CSTRING_DATA_MAX_LEN; i++)
			{
				obj.cstringData[i] = setcstringData[i].cast<char>();
			}
		})
	.def(py::pickle(
		[](const sm_data::SharedMemoryContent &obj){
		
		std::vector<char> cstringDataVector;
		for (int i = 0; i < CSTRING_DATA_MAX_LEN; i++)
		{
			cstringDataVector.push_back(obj.cstringData[i]);
		}
		return py::make_tuple(obj.intData,cstringDataVector);
	},
		[](py::tuple t){
		sm_data::SharedMemoryContent obj = sm_data::SharedMemoryContent();
		obj.intData = t[0].cast<uint32_t>();
		auto cstringDataVector = t[1].cast<std::vector<char>>();
		for (int i = 0; i < CSTRING_DATA_MAX_LEN; i++)
		{
			obj.cstringData[i] = cstringDataVector[i];
		}
		return obj;
	}
	));

	py::class_<SharedMemoryContentTopic>(SharedMemoryWrapperModule, "SharedMemoryContentTopic")
		.def(py::init<>())
		.def("getOldest", py::overload_cast<void*, SMT_DataInfo&>(&SharedMemoryContentTopic::GetOldest),py::return_value_policy::copy)
		.def("getOldest", py::overload_cast<void*>(&SharedMemoryContentTopic::GetOldest),py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t, SMT_DataInfo&>(&SharedMemoryContentTopic::GetByCounter), py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t>(&SharedMemoryContentTopic::GetByCounter), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*>(&SharedMemoryContentTopic::Publish), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*, size_t>(&SharedMemoryContentTopic::Publish), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*, SMT_DataInfo&>(&SharedMemoryContentTopic::GetLatest), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*>(&SharedMemoryContentTopic::GetLatest), py::return_value_policy::copy);
}