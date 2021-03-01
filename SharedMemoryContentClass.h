# pragma once
#include "WrapperFunctions.h"
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
	SharedMemoryWrapperModule.def("oldestRx", py::overload_cast<SharedMemoryContentWrapper&, SMT_DataInfo&>(&GetOldest),py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getOldest", py::overload_cast<SharedMemoryContentWrapper&, SMT_DataInfo&>(&GetOldest),py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getOldest", py::overload_cast<SharedMemoryContentWrapper&>(&GetOldest),py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("oldestRx", py::overload_cast<SharedMemoryContentWrapper&>(&GetOldest),py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("receive", py::overload_cast<SharedMemoryContentWrapper&, uint32_t, uint64_t, SMT_DataInfo&>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getByCounter", py::overload_cast<SharedMemoryContentWrapper&, uint32_t, uint64_t, SMT_DataInfo&>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("receive", py::overload_cast<SharedMemoryContentWrapper&, uint32_t, uint64_t>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getByCounter", py::overload_cast<SharedMemoryContentWrapper&, uint32_t, uint64_t>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("send", py::overload_cast<SharedMemoryContentWrapper&>(&Publish), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("publish", py::overload_cast<SharedMemoryContentWrapper&>(&Publish), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("latestRx", py::overload_cast<SharedMemoryContentWrapper&, SMT_DataInfo&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getLatest", py::overload_cast<SharedMemoryContentWrapper&, SMT_DataInfo&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("latestRx", py::overload_cast<SharedMemoryContentWrapper&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getLatest", py::overload_cast<SharedMemoryContentWrapper&>(&GetLatest), py::return_value_policy::copy);
}