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
void tClassRunner(py::module & SharedMemoryWrapperModule)
{

	py::class_<sm_data::t>(SharedMemoryWrapperModule, "t")
		.def(py::init<>())

		.def("paramsCtor", [](sm_data::t& obj, int seti)
	{
		obj.i = seti;
	})
		.def_readwrite("i", &sm_data::t::i)
	.def(py::pickle(
		[](const sm_data::t &obj){
		
		return py::make_tuple(obj.i);
	},
		[](py::tuple t){
		sm_data::t obj = sm_data::t();
		obj.i = t[0].cast<int>();
		return obj;
	}
	));
}