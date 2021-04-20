# pragma once

#include "C:\Users\Administrator\Documents\Python-Microblocks\real_collab_test\collabs\SM_NavCovData.h"

#include "C:\Users\Administrator\Documents\Python-Microblocks\real_collab_test\collabs\SM_NavData.h"

#include "C:\Users\Administrator\Documents\Python-Microblocks\real_collab_test\collabs\SM_SystemTime.h"

#include "C:\Users\Administrator\Documents\Python-Microblocks\real_collab_test\collabs\SM_Topic_NavData.h"

#include "sharedMemoryTopics.h"

#include "Shared_Memory_Topics_API.h"

#include <pybind11\pybind11.h>

#include <pybind11\stl.h>

#include <pybind11\stl_bind.h>

#include <pybind11\numpy.h>

#include <pybind11\pytypes.h>

#include <iostream>

namespace py = pybind11;
void NavData_SpeedClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::NavData_Speed>(SharedMemoryWrapperModule, "NavData_Speed")
		.def(py::init<>())

		.def_readwrite("vNorth", &sm_data::NavData_Speed::vNorth)
		.def_readwrite("vEast", &sm_data::NavData_Speed::vEast)
		.def_readwrite("vDown", &sm_data::NavData_Speed::vDown)
	.def(py::pickle(
		[](const sm_data::NavData_Speed &obj){
		
		return py::make_tuple(obj.vNorth,obj.vEast,obj.vDown);
	},
		[](py::tuple t){
		sm_data::NavData_Speed obj = sm_data::NavData_Speed();
		obj.vNorth = t[0].cast<double>();
		obj.vEast = t[1].cast<double>();
		obj.vDown = t[2].cast<double>();
		return obj;
	}
	));
}