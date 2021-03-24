# pragma once

#include "SharedMemoryContent.h"

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
		.def_readwrite("singleInteger", &sm_data::testStructFour::singleInteger)
		.def_property("dimensionalArray", [](sm_data::testStructFour &obj)->py::array{
		auto dtype = py::dtype(py::format_descriptor<int>::format());
		auto base = py::array(dtype, { 2, 3 }, { sizeof(int) * 3, sizeof(int) });
		return py::array(dtype, {2, 3 }, { sizeof(int) * 3, sizeof(int) }, obj.dimensionalArray, base);
		},[](sm_data::testStructFour& obj, py::list setdimensionalArray)
		{
			for (int i = 0; i < 2; i++)
			{
				py::list temp = setdimensionalArray[i].cast<py::list>();
				for (int j =0; j < 3; j++)
				{
					obj.dimensionalArray[i][j] = temp[j].cast<int>();
				}
			}
		})
		.def_readwrite("structOne", &sm_data::testStructFour::structOne)
	.def(py::pickle(
		[](const sm_data::testStructFour &obj){
		std::vector<std::vector<int>> dimensionalArrayVector;
		for (int i = 0; i < 2; i++)
		{
			std::vector<int> temp;
			for (int j = 0; j < 3; j++)
			{
				temp.push_back(obj.dimensionalArray[i][j]);
			}
			dimensionalArrayVector.push_back(temp);
		}
		return py::make_tuple(obj.singleInteger,dimensionalArrayVector,obj.structOne);
	},
		[](py::tuple t){
		sm_data::testStructFour obj = sm_data::testStructFour();
		obj.singleInteger = t[0].cast<int>();
		auto dimensionalArrayVector = t[1].cast<std::vector<std::vector<int>>>();
		for (int i = 0; i < 2; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				obj.dimensionalArray[i][j] = dimensionalArrayVector[i][j];
			}
		}
		
		obj.structOne = t[2].cast<testStructOne>();
		return obj;
	}
	));

	py::class_<testStructFourTopic>(SharedMemoryWrapperModule, "testStructFourTopic")
		.def(py::init<>())
		.def("getOldest", py::overload_cast<void*, SMT_DataInfo&>(&testStructFourTopic::GetOldest),py::return_value_policy::copy)
		.def("getOldest", py::overload_cast<void*>(&testStructFourTopic::GetOldest),py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t, SMT_DataInfo&>(&testStructFourTopic::GetByCounter), py::return_value_policy::copy)
		.def("getByCounter", py::overload_cast<void*, uint32_t, uint64_t>(&testStructFourTopic::GetByCounter), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*>(&testStructFourTopic::Publish), py::return_value_policy::copy)
		.def("publish", py::overload_cast<void*, size_t>(&testStructFourTopic::Publish), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*, SMT_DataInfo&>(&testStructFourTopic::GetLatest), py::return_value_policy::copy)
		.def("getLatest", py::overload_cast<void*>(&testStructFourTopic::GetLatest), py::return_value_policy::copy);
}