#include "stdafx.h"
#include "GenericWrapperHandler.h"
#include <iostream>
testWrapper::testWrapper()
{
	_test = {};
}
void testWrapper::updatePublish()
{
	int max_index = (testArr.size() >= 10) ? 10 : testArr.size();
	for (int i = 0; i < max_index; i++)
	{
		int second_max_index = (i.size() >= 10) ? 10 : i.size();
		for (int j = 0; j < second_max_index; j++)
		{
			_test.testArr[i][j] = testArr[i][j];
		}
	}
	int max_index = (regularArr.size() >= 10) ? 10 : regularArr.size();
	for (int i = 0; i < max_index; i++)
	{
		_test.regularArr[i] = regularArr[i];
	}
}
void testWrapper::updateGet()
{
	testArr.clear();
	for (int i = 0; i < 10; i++)
	{
		for (int j = 0; j < 10; j++)
		{
			testArr[i].push_back(_test.testArr[i][j]);
	
		}
	}
	regularArr.clear();
	for (int i = 0; i < 10; i++)
	{
		regularArr.push_back(_test.regularArr[i]);
	}
}
sm_data::test* testWrapper::getPtr()
{
	return &_test;
}
