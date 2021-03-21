# pragma once
#include "sharedMemoryTopics.h"
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
			[](const testStructThreeWrapper &obj){
			return py::make_tuple(obj.getbooleanValue(),obj.charArray);
		},
			[](py::tuple t){
			testStructThreeWrapper obj = testStructThreeWrapper();
			obj.setbooleanValue(t[0].cast<bool>());
			obj.charArray = t[1].cast<std::vector<char>>();
			return obj;
		}
		));

	py::class_<testStructThreeTopic>(SharedMemoryWrapperModule, "testStructThreeTopic")
		.def(py::init<>())
		.def("getOldest", py::overload_cast<void*, SMT_DataInfo&>(&testStructThreeTopic::GetOldest),py::return_value_policy::copy)
		.def("getOldest", py::overload_cast<void*>(&testStructThreeTopic::GetOldest),py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t, SMT_DataInfo&>(&testStructThreeTopic::GetByCounter), py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t>(&testStructThreeTopic::GetByCounter), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*>(&testStructThreeTopic::Publish), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*, size_t>(&testStructThreeTopic::Publish), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*, SMT_DataInfo&>(&testStructThreeTopic::GetLatest), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*>(&testStructThreeTopic::GetLatest), py::return_value_policy::copy);
}