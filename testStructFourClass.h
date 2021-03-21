# pragma once
#include "sharedMemoryTopics.h"
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
			[](const testStructFourWrapper &obj){
			return py::make_tuple(obj.getsingleInteger(),obj.intArray);
		},
			[](py::tuple t){
			testStructFourWrapper obj = testStructFourWrapper();
			obj.setsingleInteger(t[0].cast<int>());
			obj.intArray = t[1].cast<std::vector<int>>();
			return obj;
		}
		));

	py::class_<testStructFourTopic>(SharedMemoryWrapperModule, "testStructFourTopic")
		.def(py::init<>())
		.def("getOldest", py::overload_cast<void*, SMT_DataInfo&>(&testStructFourTopic::GetOldest),py::return_value_policy::copy)
		.def("getOldest", py::overload_cast<void*>(&testStructFourTopic::GetOldest),py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t, SMT_DataInfo&>(&testStructFourTopic::GetByCounter), py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t>(&testStructFourTopic::GetByCounter), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*>(&testStructFourTopic::Publish), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*, size_t>(&testStructFourTopic::Publish), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*, SMT_DataInfo&>(&testStructFourTopic::GetLatest), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*>(&testStructFourTopic::GetLatest), py::return_value_policy::copy);
}