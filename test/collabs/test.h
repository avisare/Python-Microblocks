/////////////////////////////////////////////////////////////////////////////
// File Name  : SharedMemoryConent.h
//
// Description: Shared Memory Topics
//
// Copyright (c) 2021 (year of creation) Rafael Ltd. All rights reserved.
/////////////////////////////////////////////////////////////////////////////
# pragma once
#ifndef SHARED_MEMORY_CONTENT_H
#define SHARED_MEMORY_CONTENT_H

#include <cstdint>
#define CSTRING_DATA_MAX_LEN 32
#define INT_ARRAY_MAX_LEN 10

namespace sm_data {

#pragma pack(push, 1)

struct t
{
	int i;
};

struct SharedMemoryContent
{
	uint32_t intData;
	char	 cstringData[CSTRING_DATA_MAX_LEN];
	t test[2][2];
};

struct testStructOne
{
	int intNumber;
	float floatNumber;
	char character;
	float arr[10];
};

struct testStructThree
{
	bool booleanValue;
	float floatValue;
	char charArray[CSTRING_DATA_MAX_LEN];
};
struct testStructTwo
{
	long longNumber;
	unsigned int uintNumber;
	bool boolean;
	struct testStructThree structThree;
};

struct testStructFour
{
	int singleInteger;
	int dimensionalArray[2][3][4];
	testStructOne structOne;
};
#pragma pack(pop)

// Topic name with content version,
// increase the version every update that break backward compatibility
const char* const SHARED_MEMORY_CONTENT_TOPIC_NAME    = "SharedMemoryContent_01";
const int         SHARED_MEMORY_CONTENT_DATA_SIZE     = sizeof(testStructFour);
const int         SHARED_MEMORY_CONTENT_HISTORY_DEPTH = 10;
const int         SHARED_MEMORY_CONTENT_CELLS_COUNT   = 20;

} // namespace sm_data


#endif // SHARED_MEMORY_CONTENT_H
