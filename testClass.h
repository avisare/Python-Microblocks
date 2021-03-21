# pragma once
#include "sharedMemoryTopics.h"
#include "Shared_Memory_Topics_API.h"
#include "GenericWrapperHandler.h"
#include <pybind11\pybind11.h>
#include <pybind11\stl.h>
#include <pybind11\stl_bind.h>
#include <iostream>
namespace py = pybind11;
void testClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<testWrapper>(SharedMemoryWrapperModule, "test")
		.def(py::init<>())
		.def_readwrite("testArr", &testWrapper::testArr)
		.def_readwrite("regularArr", &testWrapper::regularArr)
		.def(py::pickle(
			[](const testWrapper &obj){
			return py::make_tuple(obj.testArr,obj.regularArr);
		},
			[](py::tuple t){
			testWrapper obj = testWrapper();
			obj.testArr = t[0].cast<std::vector<int>>();
			obj.regularArr = t[1].cast<std::vector<int>>();
			return obj;
		}
		));

	py::class_<testTopic>(SharedMemoryWrapperModule, "testTopic")
		.def(py::init<>())
		.def("getOldest", py::overload_cast<void*, SMT_DataInfo&>(&testTopic::GetOldest),py::return_value_policy::copy)
		.def("getOldest", py::overload_cast<void*>(&testTopic::GetOldest),py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t, SMT_DataInfo&>(&testTopic::GetByCounter), py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t>(&testTopic::GetByCounter), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*>(&testTopic::Publish), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*, size_t>(&testTopic::Publish), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*, SMT_DataInfo&>(&testTopic::GetLatest), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*>(&testTopic::GetLatest), py::return_value_policy::copy);
}