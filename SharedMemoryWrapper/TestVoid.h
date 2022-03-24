#pragma once
#include <pybind11\stl.h>
#include <iostream>
#include <array>

struct intInfo
{
	int singleInfo;
	std::array<int, 5> arrayInfo;
};
struct floatInfo
{
	float singleInfo;
	std::array<float, 5> arrayInfo;
};
struct info
{
	intInfo intinfo;
	floatInfo floatinfo;
};
void printSpecificInfo(void* structInfo, std::string type)
{
	if (type.compare("int") == 0)
	{
		intInfo realInfo = (*(intInfo*)structInfo);
		std::cout << "single info: " << realInfo.singleInfo << std::endl;
		for (int i = 0; i < 5; i++)
		{
			std::cout << "info in location " << i << " :" << realInfo.arrayInfo[i] << std::endl;
		}
	}
	else
	{
		floatInfo realInfo = (*(floatInfo*)structInfo);
		std::cout << "single info: " << realInfo.singleInfo << std::endl;
		for (int i = 0; i < 5; i++)
		{
			std::cout << "info in location " << i << " :" << realInfo.arrayInfo[i] << std::endl;
		}
	}
}
void printInfo(floatInfo floatinfo)
{
	printSpecificInfo(&floatinfo, "float");
}

void printInfo(intInfo intinfo)
{
	printSpecificInfo(&intinfo, "int");
}

