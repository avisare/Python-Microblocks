#pragma once
#include "test.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <iostream>
namespace py = pybind11;
void enumsRunner(py::module & SharedMemoryWrapperModule)
{
	py::enum_<sm_data::NavCov_Status>(SharedMemoryWrapperModule, "NavCov_Status")
		.value("NAV_COV_STS_NO_DATA", sm_data::NAV_COV_STS_NO_DATA)
		.value("NAV_COV_STS_DIAGONAL_ONLY", sm_data::NAV_COV_STS_DIAGONAL_ONLY)
		.value("NAV_COV_STS_FULL_MATRIX", sm_data::NAV_COV_STS_FULL_MATRIX)
		.export_values();}