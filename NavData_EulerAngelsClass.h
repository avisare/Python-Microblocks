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
void NavData_EulerAngelsClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::NavData_EulerAngels>(SharedMemoryWrapperModule, "NavData_EulerAngels")
		.def(py::init<>())

		.def_readwrite("yaw", &sm_data::NavData_EulerAngels::yaw)
		.def_readwrite("pitch", &sm_data::NavData_EulerAngels::pitch)
		.def_readwrite("roll", &sm_data::NavData_EulerAngels::roll)
	.def(py::pickle(
		[](const sm_data::NavData_EulerAngels &obj){
		
		return py::make_tuple(obj.yaw,obj.pitch,obj.roll);
	},
		[](py::tuple t){
		sm_data::NavData_EulerAngels obj = sm_data::NavData_EulerAngels();
		obj.yaw = t[0].cast<double>();
		obj.pitch = t[1].cast<double>();
		obj.roll = t[2].cast<double>();
		return obj;
	}
	));
}