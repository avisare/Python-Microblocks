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
void testStructTwoClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::testStructTwo>(SharedMemoryWrapperModule, "testStructTwo")
		.def(py::init<>())

		.def_readwrite("longNumber", &sm_data::testStructTwo::longNumber)
		.def_readwrite("uintNumber", &sm_data::testStructTwo::uintNumber)
		.def_readwrite("boolean", &sm_data::testStructTwo::boolean)
		.def_readwrite("structThree", &sm_data::testStructTwo::structThree)
	.def(py::pickle(
		[](const sm_data::testStructTwo &obj){
		
		return py::make_tuple(obj.longNumber,obj.uintNumber,obj.boolean,obj.structThree);
	},
		[](py::tuple t){
		sm_data::testStructTwo obj = sm_data::testStructTwo();
		obj.longNumber = t[0].cast<long>();
		obj.uintNumber = t[1].cast<unsigned int>();
		obj.boolean = t[2].cast<bool>();
		obj.structThree = t[3].cast<sm_data::testStructThree>();
		return obj;
	}
	));
}