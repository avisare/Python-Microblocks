#include "stdafx.h"
#include "NavCov_RecordClass.h"

#include "testClass.h"

#include "enums.h"
#include "WrapperFunctions.h"

#include "Shared_Memory_Topics_API.h"

#include "GenericWrapperHandler.h"

#include <pybind11\pybind11.h>

#include <pybind11\stl.h>

#include <pybind11\stl_bind.h>

#include <iostream>

PYBIND11_MAKE_OPAQUE(std::vector<std::vector<int>>);
PYBIND11_MAKE_OPAQUE(std::vector<int>);
namespace py = pybind11;

PYBIND11_MODULE(SharedMemoryWrapper, SharedMemoryWrapperModule)
{
	py::bind_vector<std::vector<std::vector<int>>> (SharedMemoryWrapperModule, "std::vector<int>List");
	py::bind_vector<std::vector<int>> (SharedMemoryWrapperModule, "intList");
	

	SharedMemoryWrapperModule.def("SMT_Version", &SMT_Version, py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_Init", &SMT_Init, py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_Show", &SMT_Show, py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_CreateTopic", &SMT_CreateTopic, py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_GetPublishCount", &SMT_GetPublishCount, py::return_value_policy::copy);

	SharedMemoryWrapperModule.def("SMT_ClearHistory", &SMT_ClearHistory, py::return_value_policy::copy);


	NavCov_RecordClassRunner(SharedMemoryWrapperModule);

	testClassRunner(SharedMemoryWrapperModule);

	enumsRunner(SharedMemoryWrapperModule);
}