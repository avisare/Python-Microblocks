# pragma once

#include "C:\Users\Administrator\Documents\Python-Microblocks\test\collabs\test.h"

#include "C:\Users\Administrator\Documents\Python-Microblocks\test\collabs\test1.h"

#include "sharedMemoryTopics.h"

#include "Shared_Memory_Topics_API.h"

#include <pybind11\pybind11.h>

#include <pybind11\stl.h>

#include <pybind11\stl_bind.h>

#include <pybind11\numpy.h>

#include <pybind11\pytypes.h>

#include <iostream>

namespace py = pybind11;
void SharedMemoryContentClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::SharedMemoryContent>(SharedMemoryWrapperModule, "SharedMemoryContent")
		.def(py::init<>())

		.def_readwrite("intData", &sm_data::SharedMemoryContent::intData)
		.def_property("cstringData", [](sm_data::SharedMemoryContent & obj)->py::array{
		auto dtype = py::dtype(py::format_descriptor<unsigned char>::format());
		auto base = py::array(dtype, { CSTRING_DATA_MAX_LEN  }, { sizeof(unsigned char) * 1 });
		return py::array(dtype, {{ CSTRING_DATA_MAX_LEN }}, { sizeof(unsigned char) * 1 }, obj.cstringData, base);

	}, [](sm_data::SharedMemoryContent& obj, py::list setArr)
	{

		for (int i = 0; i < CSTRING_DATA_MAX_LEN; i++)
		{
			obj.cstringData[i] = setArr[i].cast<unsigned char>();
		}
	})
		.def_property("test", [](sm_data::SharedMemoryContent &obj)->std::vector<std::vector<sm_data::t*>> {
		std::vector<std::vector<sm_data::t*>> temp0;
		for (int i = 0; i < 2; i++)
		{
			std::vector<sm_data::t*> temp1;
			for (int j = 0; j < 2; j++)
			{
				temp1.push_back(&obj.test[i][j]);
			}
			temp0.push_back(temp1);
		}
		return temp0;

	}, [](sm_data::SharedMemoryContent& obj, std::vector<std::vector<sm_data::t*>> setArr)
	{
		for (int i = 0; i < 2; i++)
		{
			for (int j = 0; j < 2; j++)
			{
				obj.test[i][j] = *setArr[i][j];
			}
		}
	})
	.def(py::pickle(
		[](const sm_data::SharedMemoryContent &obj){
		
		std::vector<unsigned char> cstringDataVector;
		for (int i = 0; i < CSTRING_DATA_MAX_LEN; i++)
		{
			cstringDataVector.push_back(obj.cstringData[i]);
		}
		std::vector<std::vector<sm_data::t>> testVector;
		for (int i = 0; i < 2; i++)
		{
			std::vector<sm_data::t> temp1;
			for (int j = 0; j < 2; j++)
			{
				temp1.push_back(obj.test[i][j]);
			}
			testVector.push_back(temp1);
		}
		return py::make_tuple(obj.intData,cstringDataVector,testVector);
	},
		[](py::tuple t){
		sm_data::SharedMemoryContent obj = sm_data::SharedMemoryContent();
		obj.intData = t[0].cast<uint32_t>();
		auto cstringDataVector = t[1].cast<std::vector<unsigned char>>();
		for (int i = 0; i < CSTRING_DATA_MAX_LEN; i++)
		{
			obj.cstringData[i] = cstringDataVector[i];
		}
		auto testVector = t[2].cast<std::vector<std::vector<sm_data::t>>>();
		for (int i = 0; i < 2; i++)
		{
			for (int j = 0; j < 2; j++)
			{
				obj.test[i][j] = testVector[i][j];
			}
		}
		return obj;
	}
	));
}