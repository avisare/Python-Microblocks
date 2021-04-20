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
void NavData_PositionClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::NavData_Position>(SharedMemoryWrapperModule, "NavData_Position")
		.def(py::init<>())

		.def_readwrite("latitude", &sm_data::NavData_Position::latitude)
		.def_readwrite("longitude", &sm_data::NavData_Position::longitude)
		.def_readwrite("altitude", &sm_data::NavData_Position::altitude)
	.def(py::pickle(
		[](const sm_data::NavData_Position &obj){
		
		return py::make_tuple(obj.latitude,obj.longitude,obj.altitude);
	},
		[](py::tuple t){
		sm_data::NavData_Position obj = sm_data::NavData_Position();
		obj.latitude = t[0].cast<double>();
		obj.longitude = t[1].cast<double>();
		obj.altitude = t[2].cast<double>();
		return obj;
	}
	));
}