#include "stdafx.h"

#include "smt.h"

#include "SMT_DataInfoClass.h"

#include "NavCov_RecordClass.h"

#include "NavData_SpeedClass.h"

#include "NavData_PositionClass.h"

#include "NavData_QuaternionClass.h"

#include "NavData_EulerAngelsClass.h"

#include "NavData_RecordClass.h"

#include "enums.h"

#include "SharedMemoryTopics.h"

#include "Shared_Memory_Topics_API.h"

#include <pybind11\pybind11.h>

#include <pybind11\stl.h>

#include <pybind11\stl_bind.h>

#include <iostream>

namespace py = pybind11;

PYBIND11_MODULE(SharedMemoryWrapper, SharedMemoryWrapperModule)
{

	SharedMemoryWrapperModule.def("SMT_Version", &SMT_Version, py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_Init", &SMT_Init, py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_Show", &SMT_Show, py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_CreateTopic", py::overload_cast<std::string>(&SMT_CreateTopic), py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_CreateTopic", py::overload_cast<const char*, const uint32_t, const uint32_t, const uint32_t>(&SMT_CreateTopic), py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_GetPublishCount", &SMT_GetPublishCount, py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_ClearHistory", &SMT_ClearHistory, py::return_value_policy::copy);


	smtRunner(SharedMemoryWrapperModule);

	SMT_DataInfoRunner(SharedMemoryWrapperModule);

	NavCov_RecordClassRunner(SharedMemoryWrapperModule);

	NavData_SpeedClassRunner(SharedMemoryWrapperModule);

	NavData_PositionClassRunner(SharedMemoryWrapperModule);

	NavData_QuaternionClassRunner(SharedMemoryWrapperModule);

	NavData_EulerAngelsClassRunner(SharedMemoryWrapperModule);

	NavData_RecordClassRunner(SharedMemoryWrapperModule);

	enumsRunner(SharedMemoryWrapperModule);
}