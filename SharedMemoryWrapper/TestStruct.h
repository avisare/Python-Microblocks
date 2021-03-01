#pragma once

#include <iostream>
#include <pybind11\stl.h>
#include <pybind11\complex.h>
#include <pybind11\pybind11.h>

namespace py = pybind11;
#define MAX_CHAR 20

struct ComplexStruct
{
	unsigned long unsignedLongNumber;
	float floatNumber;
	char charArray[MAX_CHAR];
	char* intArray;
	char* cStr;
	std::string str;
	uint16_t uint16Number;
	int* intPtr;
	bool boolean;
	char32_t char32Var;
	signed short int ssiNumber;
	void initalize()
	{
		intPtr = new int();
		memset(charArray, '\0', sizeof(charArray));
	}
	void setArray(char* setCharArray)
	{
		strncpy_s(charArray, setCharArray, MAX_CHAR-1); //need space for the \0 at the end
	}
	std::vector<int> getArray()
	{
		std::vector<int> vec;
		for (int i = 0; i < sizeof(intArray); i++)
		{
			vec.push_back()
		}
		return ;
	}
	void setIntPtrValue(int intValue)
	{
		*intPtr = intValue;
	}
	int getIntPtrValue()
	{
		return *intPtr;
	}
};
