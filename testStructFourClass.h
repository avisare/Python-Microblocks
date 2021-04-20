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
void testStructFourClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::testStructFour>(SharedMemoryWrapperModule, "testStructFour")
		.def(py::init<>())

		.def("paramsCtor", [](sm_data::testStructFour& obj, int setsingleInteger, py::list setdimensionalArray, sm_data::testStructOne setstructOne)
	{
		obj.singleInteger = setsingleInteger;
		for (int i = 0; i < 2; i++)
		{
			py::list temp0 = setdimensionalArray[i].cast<py::list>();
			for (int j = 0; j < 3; j++)
			{
				py::list temp1 = temp0[j].cast<py::list>();
				for (int k = 0; k < 4; k++)
				{
					obj.dimensionalArray[i][j][k] = temp1[k].cast<int>();
				}
			}
		}
		obj.structOne = setstructOne;
	})
		.def_readwrite("singleInteger", &sm_data::testStructFour::singleInteger)
		.def_property("dimensionalArray", [](sm_data::testStructFour & obj)->py::array{
		auto dtype = py::dtype(py::format_descriptor<int>::format());
		auto base = py::array(dtype, { 2,3,4 }, { sizeof(int) * 12, sizeof(int) * 4, sizeof(int) * 1 });
		return py::array(dtype, { 2,3,4 }, { sizeof(int) * 12, sizeof(int) * 4, sizeof(int) * 1 }, obj.dimensionalArray, base);

	}, [](sm_data::testStructFour& obj, py::list setArr)
	{

		for (int i = 0; i < 2; i++)
		{
			py::list temp0 = setArr[i].cast<py::list>();
			for (int j = 0; j < 3; j++)
			{
				py::list temp1 = temp0[j].cast<py::list>();
				for (int k = 0; k < 4; k++)
				{
					obj.dimensionalArray[i][j][k] = temp1[k].cast<int>();
				}
			}
		}
	})
		.def_readwrite("structOne", &sm_data::testStructFour::structOne)
	.def(py::pickle(
		[](const sm_data::testStructFour &obj){
		
		std::vector<std::vector<std::vector<int>>> dimensionalArrayVector;
		for (int i = 0; i < 2; i++)
		{
			std::vector<std::vector<int>> temp1;
			for (int j = 0; j < 3; j++)
			{
				std::vector<int> temp2;
				for (int k = 0; k < 4; k++)
				{
					temp2.push_back(obj.dimensionalArray[i][j][k]);
				}
				temp1.push_back(temp2);
			}
			dimensionalArrayVector.push_back(temp1);
		}
		return py::make_tuple(obj.singleInteger,dimensionalArrayVector,obj.structOne);
	},
		[](py::tuple t){
		sm_data::testStructFour obj = sm_data::testStructFour();
		obj.singleInteger = t[0].cast<int>();
		auto dimensionalArrayVector = t[1].cast<std::vector<std::vector<std::vector<int>>>>();
		for (int i = 0; i < 2; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				for (int k = 0; k < 4; k++)
				{
					obj.dimensionalArray[i][j][k] = dimensionalArrayVector[i][j][k];
				}
			}
		}
		obj.structOne = t[2].cast<sm_data::testStructOne>();
		return obj;
	}
	));
}