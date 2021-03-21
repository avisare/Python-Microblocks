# pragma once
#include "sharedMemoryTopics.h"
#include "Shared_Memory_Topics_API.h"
#include "GenericWrapperHandler.h"
#include <pybind11\pybind11.h>
#include <pybind11\stl.h>
#include <pybind11\stl_bind.h>
#include <iostream>
namespace py = pybind11;
void NavCov_RecordClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::NavCov_Record>(SharedMemoryWrapperModule, "NavCov_Record")
		.def(py::init<>())
		.def_readwrite("covStatus", &sm_data::NavCov_Record::covStatus, py::return_value_policy::copy)
		.def_readwrite("floatVar", &sm_data::NavCov_Record::floatVar, py::return_value_policy::copy)
		.def(py::pickle(
			[](const sm_data::NavCov_Record &obj){
			return py::make_tuple(obj.covStatus,obj.floatVar);
		},
			[](py::tuple t){
			sm_data::NavCov_Record obj = sm_data::NavCov_Record();
			obj.covStatus = t[0].cast<int>();
			obj.floatVar = t[1].cast<float>();
			return obj;
		}
		));

	py::class_<NavCov_RecordTopic>(SharedMemoryWrapperModule, "NavCov_RecordTopic")
		.def(py::init<>())
		.def("getOldest", py::overload_cast<void*, SMT_DataInfo&>(&NavCov_RecordTopic::GetOldest),py::return_value_policy::copy)
		.def("getOldest", py::overload_cast<void*>(&NavCov_RecordTopic::GetOldest),py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t, SMT_DataInfo&>(&NavCov_RecordTopic::GetByCounter), py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t>(&NavCov_RecordTopic::GetByCounter), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*>(&NavCov_RecordTopic::Publish), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*, size_t>(&NavCov_RecordTopic::Publish), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*, SMT_DataInfo&>(&NavCov_RecordTopic::GetLatest), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*>(&NavCov_RecordTopic::GetLatest), py::return_value_policy::copy);
}