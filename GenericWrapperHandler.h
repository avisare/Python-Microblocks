#pragma once
#include "test.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

class testWrapper
{
public:
	testWrapper();
	void updatePublish();
	void updateGet();
	std::vector<std::vector<int>> testArr;
	std::vector<int> regularArr;
	sm_data::test* getPtr();
private:
	sm_data::test _test;
};
