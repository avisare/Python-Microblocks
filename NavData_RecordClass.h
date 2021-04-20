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
void NavData_RecordClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::NavData_Record>(SharedMemoryWrapperModule, "NavData_Record")
		.def(py::init<>())

		.def_readwrite("navStatus", &sm_data::NavData_Record::navStatus)
		.def_readwrite("timetag", &sm_data::NavData_Record::timetag)
		.def_readwrite("podSpeed", &sm_data::NavData_Record::podSpeed)
		.def_readwrite("podPosition", &sm_data::NavData_Record::podPosition)
		.def_readwrite("losQuaternion", &sm_data::NavData_Record::losQuaternion)
		.def_readwrite("rangeToTarget", &sm_data::NavData_Record::rangeToTarget)
		.def_readwrite("gimbalDirection", &sm_data::NavData_Record::gimbalDirection)
		.def_readwrite("losAngels", &sm_data::NavData_Record::losAngels)
		.def_readwrite("losRate", &sm_data::NavData_Record::losRate)
		.def_readwrite("navAlignmentEvent", &sm_data::NavData_Record::navAlignmentEvent)
		.def_property("spare", [](sm_data::NavData_Record & obj)->py::array{
		auto dtype = py::dtype(py::format_descriptor<uint8_t>::format());
		auto base = py::array(dtype, { NAV_RECORD_SPARE }, { sizeof(uint8_t) * 1 });
		return py::array(dtype, { NAV_RECORD_SPARE }, { sizeof(uint8_t) * 1 }, obj.spare, base);

	}, [](sm_data::NavData_Record& obj, py::list setArr)
	{

		for (int i = 0; i < NAV_RECORD_SPARE; i++)
		{
			obj.spare[i] = setArr[i].cast<uint8_t>();
		}
	})
	.def(py::pickle(
		[](const sm_data::NavData_Record &obj){
		
		std::vector<uint8_t> spareVector;
		for (int i = 0; i < NAV_RECORD_SPARE; i++)
		{
			spareVector.push_back(obj.spare[i]);
		}
		return py::make_tuple(obj.navStatus,obj.timetag,obj.podSpeed,obj.podPosition,obj.losQuaternion,obj.rangeToTarget,obj.gimbalDirection,obj.losAngels,obj.losRate,obj.navAlignmentEvent,spareVector);
	},
		[](py::tuple t){
		sm_data::NavData_Record obj = sm_data::NavData_Record();
		obj.navStatus = t[0].cast<sm_data::NavData_Status>();
		obj.timetag = t[1].cast<sm_data::SystemTime64Us>();
		obj.podSpeed = t[2].cast<sm_data::NavData_Speed>();
		obj.podPosition = t[3].cast<sm_data::NavData_Position>();
		obj.losQuaternion = t[4].cast<sm_data::NavData_Quaternion>();
		obj.rangeToTarget = t[5].cast<double>();
		obj.gimbalDirection = t[6].cast<sm_data::NavData_Quaternion>();
		obj.losAngels = t[7].cast<sm_data::NavData_EulerAngels>();
		obj.losRate = t[8].cast<sm_data::NavData_EulerAngels>();
		obj.navAlignmentEvent = t[9].cast<sm_data::NavData_AlignmentEvent>();
		auto spareVector = t[10].cast<std::vector<uint8_t>>();
		for (int i = 0; i < NAV_RECORD_SPARE; i++)
		{
			obj.spare[i] = spareVector[i];
		}
		return obj;
	}
	));
}