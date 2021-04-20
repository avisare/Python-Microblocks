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
void NavCov_RecordClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::NavCov_Record>(SharedMemoryWrapperModule, "NavCov_Record")
		.def(py::init<>())

		.def_readwrite("covStatus", &sm_data::NavCov_Record::covStatus)
		.def_readwrite("covTimeTag", &sm_data::NavCov_Record::covTimeTag)
		.def_property("covData", [](sm_data::NavCov_Record & obj)->py::array{
		auto dtype = py::dtype(py::format_descriptor<float>::format());
		auto base = py::array(dtype, { 6,6 }, { sizeof(float) * 1, sizeof(float) * 1 });
		return py::array(dtype, { 6,6 }, { sizeof(float) * 1, sizeof(float) * 1 }, obj.covData, base);

	}, [](sm_data::NavCov_Record& obj, py::list setArr)
	{

		for (int i = 0; i < 6; i++)
		{
			py::list temp0 = setArr[i].cast<py::list>();
			for (int j = 0; j < 6; j++)
			{
				obj.covData[i][j] = temp0[j].cast<float>();
			}
		}
	})
		.def_property("spare", [](sm_data::NavCov_Record & obj)->py::array{
		auto dtype = py::dtype(py::format_descriptor<uint8_t>::format());
		auto base = py::array(dtype, { NAV_COV_RECORD_SPARE }, { sizeof(uint8_t) * 1 });
		return py::array(dtype, { NAV_COV_RECORD_SPARE }, { sizeof(uint8_t) * 1 }, obj.spare, base);

	}, [](sm_data::NavCov_Record& obj, py::list setArr)
	{

		for (int i = 0; i < NAV_COV_RECORD_SPARE; i++)
		{
			obj.spare[i] = setArr[i].cast<uint8_t>();
		}
	})
	.def(py::pickle(
		[](const sm_data::NavCov_Record &obj){
		
		std::vector<std::vector<float>> covDataVector;
		for (int i = 0; i < 6; i++)
		{
			std::vector<float> temp1;
			for (int j = 0; j < 6; j++)
			{
				temp1.push_back(obj.covData[i][j]);
			}
			covDataVector.push_back(temp1);
		}
		std::vector<uint8_t> spareVector;
		for (int i = 0; i < NAV_COV_RECORD_SPARE; i++)
		{
			spareVector.push_back(obj.spare[i]);
		}
		return py::make_tuple(obj.covStatus,obj.covTimeTag,covDataVector,spareVector);
	},
		[](py::tuple t){
		sm_data::NavCov_Record obj = sm_data::NavCov_Record();
		obj.covStatus = t[0].cast<sm_data::NavCov_Status>();
		obj.covTimeTag = t[1].cast<sm_data::SystemTime64Us>();
		auto covDataVector = t[2].cast<std::vector<std::vector<float>>>();
		for (int i = 0; i < 6; i++)
		{
			for (int j = 0; j < 6; j++)
			{
				obj.covData[i][j] = covDataVector[i][j];
			}
		}
		auto spareVector = t[3].cast<std::vector<uint8_t>>();
		for (int i = 0; i < NAV_COV_RECORD_SPARE; i++)
		{
			obj.spare[i] = spareVector[i];
		}
		return obj;
	}
	));
}