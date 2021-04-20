#pragma once

#include "C:\Users\Administrator\Documents\Python-Microblocks\real_collab_test\collabs\SM_NavCovData.h"

#include "C:\Users\Administrator\Documents\Python-Microblocks\real_collab_test\collabs\SM_NavData.h"

#include "C:\Users\Administrator\Documents\Python-Microblocks\real_collab_test\collabs\SM_SystemTime.h"

#include "C:\Users\Administrator\Documents\Python-Microblocks\real_collab_test\collabs\SM_Topic_NavData.h"

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
		.export_values();

	py::enum_<sm_data::NavData_Status>(SharedMemoryWrapperModule, "NavData_Status")
		.value("NAV_DATA_STS_NA", sm_data::NAV_DATA_STS_NA)
		.value("NAV_DATA_STS_FULL_ATT", sm_data::NAV_DATA_STS_FULL_ATT)
		.value("NAV_DATA_STS_FULL_LEVEL", sm_data::NAV_DATA_STS_FULL_LEVEL)
		.value("NAV_DATA_STS_REDUCED", sm_data::NAV_DATA_STS_REDUCED)
		.value("NAV_DATA_STS_FAIL", sm_data::NAV_DATA_STS_FAIL)
		.export_values();

	py::enum_<sm_data::NavData_AlignmentEvent>(SharedMemoryWrapperModule, "NavData_AlignmentEvent")
		.value("NAV_DATA_NO_ALIGNMENT_EVENT", sm_data::NAV_DATA_NO_ALIGNMENT_EVENT)
		.value("NAV_DATA_ALIGNMENT_EVENT", sm_data::NAV_DATA_ALIGNMENT_EVENT)
		.export_values();
}