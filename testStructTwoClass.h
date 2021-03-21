# pragma once
#include "sharedMemoryTopics.h"
#include "Shared_Memory_Topics_API.h"
#include "GenericWrapperHandler.h"
#include <pybind11\pybind11.h>
#include <pybind11\stl.h>
#include <pybind11\stl_bind.h>
#include <iostream>
namespace py = pybind11;
void testStructTwoClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<testStructTwoWrapper>(SharedMemoryWrapperModule, "testStructTwo")
		.def(py::init<>())
		.def_property("longNumber", &testStructTwoWrapper::getlongNumber, &testStructTwoWrapper::setlongNumber, py::return_value_policy::copy)
		.def_property("uintNumber", &testStructTwoWrapper::getuintNumber, &testStructTwoWrapper::setuintNumber, py::return_value_policy::copy)
		.def_property("boolean", &testStructTwoWrapper::getboolean, &testStructTwoWrapper::setboolean, py::return_value_policy::copy)
		.def_property("structThree", &testStructTwoWrapper::getstructThree, &testStructTwoWrapper::setstructThree, py::return_value_policy::reference)
		.def(py::pickle(
			[](const testStructTwoWrapper &obj){
			return py::make_tuple(obj.getlongNumber(),obj.getuintNumber(),obj.getboolean(),obj.getstructThreeConst());
		},
			[](py::tuple t){
			testStructTwoWrapper obj = testStructTwoWrapper();
			obj.setlongNumber(t[0].cast<long>());
			obj.setuintNumber(t[1].cast<unsigned int>());
			obj.setboolean(t[2].cast<bool>());
			obj.setstructThree(t[3].cast<testStructThreeWrapper>());
			return obj;
		}
		));

	py::class_<testStructTwoTopic>(SharedMemoryWrapperModule, "testStructTwoTopic")
		.def(py::init<>())
		.def("getOldest", py::overload_cast<void*, SMT_DataInfo&>(&testStructTwoTopic::GetOldest),py::return_value_policy::copy)
		.def("getOldest", py::overload_cast<void*>(&testStructTwoTopic::GetOldest),py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t, SMT_DataInfo&>(&testStructTwoTopic::GetByCounter), py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t>(&testStructTwoTopic::GetByCounter), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*>(&testStructTwoTopic::Publish), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*, size_t>(&testStructTwoTopic::Publish), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*, SMT_DataInfo&>(&testStructTwoTopic::GetLatest), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*>(&testStructTwoTopic::GetLatest), py::return_value_policy::copy);
}