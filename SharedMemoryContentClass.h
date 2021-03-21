# pragma once
#include "sharedMemoryTopics.h"
#include "Shared_Memory_Topics_API.h"
#include "GenericWrapperHandler.h"
#include <pybind11\pybind11.h>
#include <pybind11\stl.h>
#include <pybind11\stl_bind.h>
#include <iostream>
namespace py = pybind11;
void SharedMemoryContentClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<SharedMemoryContentWrapper>(SharedMemoryWrapperModule, "SharedMemoryContent")
		.def(py::init<>())
		.def_property("intData", &SharedMemoryContentWrapper::getintData, &SharedMemoryContentWrapper::setintData, py::return_value_policy::copy)
		.def_readwrite("cstringData", &SharedMemoryContentWrapper::cstringData)
		.def(py::pickle(
			[](const SharedMemoryContentWrapper &obj){
			return py::make_tuple(obj.getintData(),obj.cstringData);
		},
			[](py::tuple t){
			SharedMemoryContentWrapper obj = SharedMemoryContentWrapper();
			obj.setintData(t[0].cast<uint32_t>());
			obj.cstringData = t[1].cast<std::vector<char>>();
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