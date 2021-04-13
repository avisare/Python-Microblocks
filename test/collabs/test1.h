/////////////////////////////////////////////////////////////////////////////
// File Name  : SharedMemoryConent.h
//
// Description: Shared Memory Topics
//
// Copyright (c) 2021 (year of creation) Rafael Ltd. All rights reserved.
/////////////////////////////////////////////////////////////////////////////

#ifndef SHARED_MEMORY_CONTENT_H
#define SHARED_MEMORY_CONTENT_H

#include <cstdint>

#define CSTRING_DATA_MAX_LEN 32
#define INT_ARRAY_MAX_LEN 10

namespace sm_data {

struct testStructOne
{
	int intNumber;
	float floatNumber;
	char character;
	float arr[10];
};
}