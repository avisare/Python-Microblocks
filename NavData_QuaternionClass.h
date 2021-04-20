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
void NavData_QuaternionClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::NavData_Quaternion>(SharedMemoryWrapperModule, "NavData_Quaternion")
		.def(py::init<>())

		.def_readwrite("data1", &sm_data::NavData_Quaternion::data1)
		.def_readwrite("data2", &sm_data::NavData_Quaternion::data2)
		.def_readwrite("data3", &sm_data::NavData_Quaternion::data3)
		.def_readwrite("data4", &sm_data::NavData_Quaternion::data4)
	.def(py::pickle(
		[](const sm_data::NavData_Quaternion &obj){
		
		return py::make_tuple(obj.data1,obj.data2,obj.data3,obj.data4);
	},
		[](py::tuple t){
		sm_data::NavData_Quaternion obj = sm_data::NavData_Quaternion();
		obj.data1 = t[0].cast<double>();
		obj.data2 = t[1].cast<double>();
		obj.data3 = t[2].cast<double>();
		obj.data4 = t[3].cast<double>();
		return obj;
	}
	));
}