#pragma once

#include "sharedMemoryTopics.h"

#include "Shared_Memory_Topics_API.h"

#include <pybind11\pybind11.h>

#include <iostream>

namespace py = pybind11;
void smtRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<NavCov_01>(SharedMemoryWrapperModule, "NavCov_01")
		.def(py::init<>())
		.def("getOldest", py::overload_cast<void*, SMT_DataInfo&>(&NavCov_01::GetOldest),py::return_value_policy::copy)
		.def("getOldest", py::overload_cast<void*>(&NavCov_01::GetOldest),py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t, SMT_DataInfo&>(&NavCov_01::GetByCounter), py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t>(&NavCov_01::GetByCounter), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*>(&NavCov_01::Publish), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*, size_t>(&NavCov_01::Publish), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*, SMT_DataInfo&>(&NavCov_01::GetLatest), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*>(&NavCov_01::GetLatest), py::return_value_policy::copy);


	py::class_<NavData_01>(SharedMemoryWrapperModule, "NavData_01")
		.def(py::init<>())
		.def("getOldest", py::overload_cast<void*, SMT_DataInfo&>(&NavData_01::GetOldest),py::return_value_policy::copy)
		.def("getOldest", py::overload_cast<void*>(&NavData_01::GetOldest),py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t, SMT_DataInfo&>(&NavData_01::GetByCounter), py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t>(&NavData_01::GetByCounter), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*>(&NavData_01::Publish), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*, size_t>(&NavData_01::Publish), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*, SMT_DataInfo&>(&NavData_01::GetLatest), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*>(&NavData_01::GetLatest), py::return_value_policy::copy);


}