/////////////////////////////////////////////////////////////////////////////
// File Name  : SharedMemoryConent.h
//
// Description: Shared Memory Topics
//
// Copyright (c) 2021 (year of creation) Rafael Ltd. All rights reserved.
/////////////////////////////////////////////////////////////////////////////
#if 0
# pragma once

//#ifndef SHARED_MEMORY_CONTENT_H
#define SHARED_MEMORY_CONTENT_H

#include <cstdint>
#include "..\test\test2.h"

#define CSTRING_DATA_MAX_LEN 32
#define INT_ARRAY_MAX_LEN 10

namespace sm_data {

struct SharedMemoryContent
{
	uint32_t intData;
	char	 cstringData[CSTRING_DATA_MAX_LEN];
	t test[2][2];
};
}
#endif 