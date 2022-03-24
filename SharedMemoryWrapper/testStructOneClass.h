# pragma once
#include "WrapperFunctions.h"
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
			[](const sm_data::testStructOne &obj) {
		return py::make_tuple(obj.intNumber, obj.floatNumber, obj.character);
	},
			[](py::tuple t) {
		sm_data::testStructOne obj = sm_data::testStructOne();
		obj.intNumber = t[0].cast<int>();
		obj.floatNumber = t[1].cast<float>();
		obj.character = t[2].cast<char>();
		return obj;
	}
	));	
	SharedMemoryWrapperModule.def("oldestRx", py::overload_cast<sm_data::testStructOne&, SMT_DataInfo&>(&GetOldest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getOldest", py::overload_cast<sm_data::testStructOne&, SMT_DataInfo&>(&GetOldest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getOldest", py::overload_cast<sm_data::testStructOne&>(&GetOldest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("oldestRx", py::overload_cast<sm_data::testStructOne&>(&GetOldest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("receive", py::overload_cast<sm_data::testStructOne&, uint32_t, uint64_t, SMT_DataInfo&>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getByCounter", py::overload_cast<sm_data::testStructOne&, uint32_t, uint64_t, SMT_DataInfo&>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("receive", py::overload_cast<sm_data::testStructOne&, uint32_t, uint64_t>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getByCounter", py::overload_cast<sm_data::testStructOne&, uint32_t, uint64_t>(&GetByCounter), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("send", py::overload_cast<sm_data::testStructOne&>(&Publish), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("publish", py::overload_cast<sm_data::testStructOne&>(&Publish), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("latestRx", py::overload_cast<sm_data::testStructOne&, SMT_DataInfo&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getLatest", py::overload_cast<sm_data::testStructOne&, SMT_DataInfo&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("latestRx", py::overload_cast<sm_data::testStructOne&>(&GetLatest), py::return_value_policy::copy);
	SharedMemoryWrapperModule.def("getLatest", py::overload_cast<sm_data::testStructOne&>(&GetLatest), py::return_value_policy::copy);
}