#include "stdafx.h"

#include "SharedMemoryContentClass.h"

#include "testStructOneClass.h"

#include "testStructThreeClass.h"

#include "testStructTwoClass.h"

#include "testStructFourClass.h"

#include "NavCov_RecordClass.h"

#include "SMT_DataInfoClass.h"

#include "enums.h"

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

	SharedMemoryWrapperModule.def("SMT_CreateTopic", &SMT_CreateTopic, py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_GetPublishCount", &SMT_GetPublishCount, py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_ClearHistory", &SMT_ClearHistory, py::return_value_policy::copy);


	SharedMemoryContentClassRunner(SharedMemoryWrapperModule);

	testStructOneClassRunner(SharedMemoryWrapperModule);

	testStructThreeClassRunner(SharedMemoryWrapperModule);

	testStructTwoClassRunner(SharedMemoryWrapperModule);

	testStructFourClassRunner(SharedMemoryWrapperModule);

	NavCov_RecordClassRunner(SharedMemoryWrapperModule);

	SMT_DataInfoClassRunner(SharedMemoryWrapperModule);

	enumsRunner(SharedMemoryWrapperModule);
}