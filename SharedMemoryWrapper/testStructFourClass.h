# pragma once
#include "WrapperFunctions.h"
#include "Shared_Memory_Topics_API.h"
#include "GenericWrapperHandler.h"
#include <pybind11\pybind11.h>
#include <pybind11\stl.h>
#include <pybind11\stl_bind.h>
#include <iostream>
namespace py = pybind11;
void testStructFourClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<testStructFourWrapper>(SharedMemoryWrapperModule, "testStructFour")
		.def(py::init<>())
		.def_property("singleInteger", &testStructFourWrapper::getsingleInteger, &testStructFourWrapper::setsingleInteger, py::return_value_policy::copy)
		.def_readwrite("intArray", &testStructFourWrapper::intArray)
		.def(py::pickle(
			[](const testStructFourWrapper &obj) {
		return py::make_tuple(obj.getsingleInteger(), obj.intArray);
	},
			[](py::tuple t) {
		testStructFourWrapper obj = testStructFourWrapper();
		obj.setsingleInteger(t[0].cast<int>());
		obj.intArray = t[1].cast<std::vector<int>>();
		return obj;
	}
	));
	SharedMemoryWrapperModule.def("oldestRx", py::overload_cast<testStructFourWrapper&, SMT_DataInfo&>(&GetOldest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getOldest", py::overload_cast<testStructFourWrapper&, SMT_DataInfo&>(&GetOldest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getOldest", py::overload_cast<testStructFourWrapper&>(&GetOldest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("oldestRx", py::overload_cast<testStructFourWrapper&>(&GetOldest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("receive", py::overload_cast<testStructFourWrapper&, uint32_t, uint64_t, SMT_DataInfo&>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getByCounter", py::overload_cast<testStructFourWrapper&, uint32_t, uint64_t, SMT_DataInfo&>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("receive", py::overload_cast<testStructFourWrapper&, uint32_t, uint64_t>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getByCounter", py::overload_cast<testStructFourWrapper&, uint32_t, uint64_t>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("send", py::overload_cast<testStructFourWrapper&>(&Publish), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("publish", py::overload_cast<testStructFourWrapper&>(&Publish), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("latestRx", py::overload_cast<testStructFourWrapper&, SMT_DataInfo&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getLatest", py::overload_cast<testStructFourWrapper&, SMT_DataInfo&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("latestRx", py::overload_cast<testStructFourWrapper&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getLatest", py::overload_cast<testStructFourWrapper&>(&GetLatest), py::return_value_policy::copy);
}