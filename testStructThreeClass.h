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
void testStructThreeClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::testStructThree>(SharedMemoryWrapperModule, "testStructThree")
		.def(py::init<>())

		.def_readwrite("booleanValue", &sm_data::testStructThree::booleanValue)
		.def_readwrite("floatValue", &sm_data::testStructThree::floatValue)
		.def_property("charArray", [](sm_data::testStructThree & obj)->py::array{
		auto dtype = py::dtype(py::format_descriptor<char>::format());
		auto base = py::array(dtype, { CSTRING_DATA_MAX_LEN }, { sizeof(char) * 1 });
		return py::array(dtype, { CSTRING_DATA_MAX_LEN }, { sizeof(char) * 1 }, obj.charArray, base);

	}, [](sm_data::testStructThree& obj, py::list setArr)
	{

		for (int i = 0; i < CSTRING_DATA_MAX_LEN; i++)
		{
			obj.charArray[i] = setArr[i].cast<char>();
		}
	})
	.def(py::pickle(
		[](const sm_data::testStructThree &obj){
		
		std::vector<char> charArrayVector;
		for (int i = 0; i < CSTRING_DATA_MAX_LEN; i++)
		{
			charArrayVector.push_back(obj.charArray[i]);
		}
		return py::make_tuple(obj.booleanValue,obj.floatValue,charArrayVector);
	},
		[](py::tuple t){
		sm_data::testStructThree obj = sm_data::testStructThree();
		obj.booleanValue = t[0].cast<bool>();
		obj.floatValue = t[1].cast<float>();
		auto charArrayVector = t[2].cast<std::vector<char>>();
		for (int i = 0; i < CSTRING_DATA_MAX_LEN; i++)
		{
			obj.charArray[i] = charArrayVector[i];
		}
		return obj;
	}
	));
}