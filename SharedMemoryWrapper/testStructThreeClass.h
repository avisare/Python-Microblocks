# pragma once
#include "WrapperFunctions.h"
#include "Shared_Memory_Topics_API.h"
#include "GenericWrapperHandler.h"
#include <pybind11\pybind11.h>
#include <pybind11\stl.h>
#include <pybind11\stl_bind.h>
#include <iostream>
namespace py = pybind11;
void testStructThreeClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<testStructThreeWrapper>(SharedMemoryWrapperModule, "testStructThree")
		.def(py::init<>())
		.def_property("booleanValue", &testStructThreeWrapper::getbooleanValue, &testStructThreeWrapper::setbooleanValue, py::return_value_policy::copy)
		.def_readwrite("charArray", &testStructThreeWrapper::charArray)
		.def(py::pickle(
			[](const testStructThreeWrapper &obj) {
		return py::make_tuple(obj.getbooleanValue(), obj.charArray);
	},
			[](py::tuple t) {
		testStructThreeWrapper obj = testStructThreeWrapper();
		obj.setbooleanValue(t[0].cast<bool>());
		obj.charArray = t[1].cast<std::vector<char>>();
		return obj;
	}
	));
	SharedMemoryWrapperModule.def("oldestRx", py::overload_cast<testStructThreeWrapper&, SMT_DataInfo&>(&GetOldest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getOldest", py::overload_cast<testStructThreeWrapper&, SMT_DataInfo&>(&GetOldest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getOldest", py::overload_cast<testStructThreeWrapper&>(&GetOldest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("oldestRx", py::overload_cast<testStructThreeWrapper&>(&GetOldest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("receive", py::overload_cast<testStructThreeWrapper&, uint32_t, uint64_t, SMT_DataInfo&>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getByCounter", py::overload_cast<testStructThreeWrapper&, uint32_t, uint64_t, SMT_DataInfo&>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("receive", py::overload_cast<testStructThreeWrapper&, uint32_t, uint64_t>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getByCounter", py::overload_cast<testStructThreeWrapper&, uint32_t, uint64_t>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("send", py::overload_cast<testStructThreeWrapper&>(&Publish), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("publish", py::overload_cast<testStructThreeWrapper&>(&Publish), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("latestRx", py::overload_cast<testStructThreeWrapper&, SMT_DataInfo&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getLatest", py::overload_cast<testStructThreeWrapper&, SMT_DataInfo&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("latestRx", py::overload_cast<testStructThreeWrapper&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getLatest", py::overload_cast<testStructThreeWrapper&>(&GetLatest), py::return_value_policy::copy);
}