/////////////////////////////////////////////////////////////////////////////
// File Name  : SharedMemoryConent.h
//
// Description: Shared Memory Topics
//
// Copyright (c) 2021 (year of creation) Rafael Ltd. All rights reserved.
/////////////////////////////////////////////////////////////////////////////
#ifndef SHARED_MEMORY_CONTENT_H
#define SHARED_MEMORY_CONTENT_H

#include "data_info.h"
#include <cstdint>

#define CSTRING_DATA_MAX_LEN 32

#define INT_ARRAY_MAX_LEN 10

#define INT_DIMENSIONAL_ARRAY_SIZE 2

namespace sm_data {

#pragma pack(push, 1)


struct SharedMemoryContent
{
	uint32_t intData;
	char	 cstringData[CSTRING_DATA_MAX_LEN];
};
struct testStructThree
{
	bool booleanValue;
	char charArray[CSTRING_DATA_MAX_LEN];
};

struct testStructOne
{
	int intNumber;
	float floatNumber;
	char character;
	int dimensionalArray [INT_DIMENSIONAL_ARRAY_SIZE][INT_DIMENSIONAL_ARRAY_SIZE];
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
	int intArray[INT_ARRAY_MAX_LEN];
};
enum NavCov_Status
{
    NAV_COV_STS_NO_DATA = 0,  /*  No valid data in covData */
    NAV_COV_STS_DIAGONAL_ONLY = 1,  /*  covData(0,0) = azimuthCov;
                                        covData(1,1) = pitchCov;
                                        covData(2,2) = rollCov;
                                        covData(3,3) = latitudeCov;
                                        covData(4,4) = longitudeCov;
                                        covData(5,5) = altitudeCov;

                                        all other cells are 0. */
    NAV_COV_STS_FULL_MATRIX = 2   /*  covData matrix is full */
};

struct NavCov_Record
{
    NavCov_Status           covStatus;
    float                   floatVar;
};
#pragma pack(pop)

// Topic name with content version,
// increase the version every update that break backward compatibility
const char* const SHARED_MEMORY_CONTENT_TOPIC_NAME    = "SharedMemoryContent_01";
const int         SHARED_MEMORY_CONTENT_DATA_SIZE     = sizeof(SharedMemoryContent);
const int         SHARED_MEMORY_CONTENT_HISTORY_DEPTH = 10;
const int         SHARED_MEMORY_CONTENT_CELLS_COUNT   = 20;

} // namespace sm_data


#endif // SHARED_MEMORY_CONTENT_H
