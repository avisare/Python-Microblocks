# pragma once
#include "sharedMemoryTopics.h"
#include "Shared_Memory_Topics_API.h"
#include "GenericWrapperHandler.h"
#include <pybind11\pybind11.h>
#include <pybind11\stl.h>
#include <pybind11\stl_bind.h>
#include <iostream>
namespace py = pybind11;
void testStructOneClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::testStructOne>(SharedMemoryWrapperModule, "testStructOne")
		.def(py::init<>())
		.def_readwrite("intNumber", &sm_data::testStructOne::intNumber, py::return_value_policy::copy)
		.def_readwrite("floatNumber", &sm_data::testStructOne::floatNumber, py::return_value_policy::copy)
		.def_readwrite("character", &sm_data::testStructOne::character, py::return_value_policy::copy)
		.def(py::pickle(
			[](const sm_data::testStructOne &obj){
			return py::make_tuple(obj.intNumber,obj.floatNumber,obj.character);
		},
			[](py::tuple t){
			sm_data::testStructOne obj = sm_data::testStructOne();
			obj.intNumber = t[0].cast<int>();
			obj.floatNumber = t[1].cast<float>();
			obj.character = t[2].cast<char>();
			return obj;
		}
		));

	py::class_<testStructOneTopic>(SharedMemoryWrapperModule, "testStructOneTopic")
		.def(py::init<>())
		.def("getOldest", py::overload_cast<void*, SMT_DataInfo&>(&testStructOneTopic::GetOldest),py::return_value_policy::copy)
		.def("getOldest", py::overload_cast<void*>(&testStructOneTopic::GetOldest),py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t, SMT_DataInfo&>(&testStructOneTopic::GetByCounter), py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t>(&testStructOneTopic::GetByCounter), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*>(&testStructOneTopic::Publish), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*, size_t>(&testStructOneTopic::Publish), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*, SMT_DataInfo&>(&testStructOneTopic::GetLatest), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*>(&testStructOneTopic::GetLatest), py::return_value_policy::copy);
}