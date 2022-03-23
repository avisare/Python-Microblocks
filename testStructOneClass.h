# pragma once

#include "C:\Users\noammi\Documents\Python-Microblocks\test\collabs\test.h"

#include "C:\Users\noammi\Documents\Python-Microblocks\test\collabs\test1.h"

#include "sharedMemoryTopics.h"

#include "Shared_Memory_Topics_API.h"

#include <pybind11\pybind11.h>

#include <pybind11\stl.h>

#include <pybind11\stl_bind.h>

#include <pybind11\numpy.h>

#include <pybind11\pytypes.h>

#include <iostream>

namespace py = pybind11;
void testStructOneClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::testStructOne>(SharedMemoryWrapperModule, "testStructOne")
		.def(py::init<>())

		.def("paramsCtor", [](sm_data::testStructOne& obj, int setintNumber, float setfloatNumber, char setcharacter, py::list setarr)
	{
		obj.intNumber = setintNumber;
		obj.floatNumber = setfloatNumber;
		obj.character = setcharacter;
		for (int i = 0; i < 10; i++)
		{
			obj.arr[i] = setarr[i].cast<float>();
		}
	})
		.def_readwrite("intNumber", &sm_data::testStructOne::intNumber)
		.def_readwrite("floatNumber", &sm_data::testStructOne::floatNumber)
		.def_readwrite("character", &sm_data::testStructOne::character)
		.def_property("arr", [](sm_data::testStructOne & obj)->py::array{
		auto dtype = py::dtype(py::format_descriptor<float>::format());
		auto base = py::array(dtype, { 10 }, { sizeof(float) * 1 });
		return py::array(dtype, { 10 }, { sizeof(float) * 1 }, obj.arr, base);

	}, [](sm_data::testStructOne& obj, py::list setArr)
	{

		for (int i = 0; i < 10; i++)
		{
			obj.arr[i] = setArr[i].cast<float>();
		}
	})
	.def(py::pickle(
		[](const sm_data::testStructOne &obj){
		
		std::vector<float> arrVector;
		for (int i = 0; i < 10; i++)
		{
			arrVector.push_back(obj.arr[i]);
		}
		return py::make_tuple(obj.intNumber,obj.floatNumber,obj.character,arrVector);
	},
		[](py::tuple t){
		sm_data::testStructOne obj = sm_data::testStructOne();
		obj.intNumber = t[0].cast<int>();
		obj.floatNumber = t[1].cast<float>();
		obj.character = t[2].cast<char>();
		auto arrVector = t[3].cast<std::vector<float>>();
		for (int i = 0; i < 10; i++)
		{
			obj.arr[i] = arrVector[i];
		}
		return obj;
	}
	));
}