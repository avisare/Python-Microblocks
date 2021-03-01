# pragma once
#include "WrapperFunctions.h"
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
			return py::make_tuple(obj.getlongNumber(),obj.getuintNumber(),obj.getboolean(),obj.getstructThree());
		},
			[](py::tuple t){
			testStructTwoWrapper obj = testStructTwoWrapper();
			obj.setlongNumber(t[0].cast<long>());
			obj.setuintNumber(t[1].cast<unsigned int>());
			obj.setboolean(t[2].cast<bool>());
			obj.setstructThree(t[3].cast<struct testStructThree>());
			return obj;
		}
		));
	SharedMemoryWrapperModule.def("oldestRx", py::overload_cast<testStructTwoWrapper&, SMT_DataInfo&>(&GetOldest),py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getOldest", py::overload_cast<testStructTwoWrapper&, SMT_DataInfo&>(&GetOldest),py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getOldest", py::overload_cast<testStructTwoWrapper&>(&GetOldest),py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("oldestRx", py::overload_cast<testStructTwoWrapper&>(&GetOldest),py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("receive", py::overload_cast<testStructTwoWrapper&, uint32_t, uint64_t, SMT_DataInfo&>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getByCounter", py::overload_cast<testStructTwoWrapper&, uint32_t, uint64_t, SMT_DataInfo&>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("receive", py::overload_cast<testStructTwoWrapper&, uint32_t, uint64_t>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getByCounter", py::overload_cast<testStructTwoWrapper&, uint32_t, uint64_t>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("send", py::overload_cast<testStructTwoWrapper&>(&Publish), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("publish", py::overload_cast<testStructTwoWrapper&>(&Publish), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("latestRx", py::overload_cast<testStructTwoWrapper&, SMT_DataInfo&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getLatest", py::overload_cast<testStructTwoWrapper&, SMT_DataInfo&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("latestRx", py::overload_cast<testStructTwoWrapper&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getLatest", py::overload_cast<testStructTwoWrapper&>(&GetLatest), py::return_value_policy::copy);
}