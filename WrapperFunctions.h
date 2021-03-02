#pragma once
#include "Shared_Memory_Topics_API.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <iostream>

bool GetByCounter(SharedMemoryContentWrapper& structObject, uint32_t counter, uint64_t timeout_us, SMT_DataInfo& data_info)
{
	bool result = SMT_GetByCounter("SharedMemoryContent", structObject.getSharedMemoryContentPtr(), counter, timeout_us, &data_info);
	structObject.updateGet();
	return result;
}

bool GetByCounter(SharedMemoryContentWrapper& structObject, uint32_t counter, uint64_t timeout_us)
{
	SMT_DataInfo data_info = {0,0,0};
	bool result = SMT_GetByCounter("SharedMemoryContent", structObject.getSharedMemoryContentPtr(), counter, timeout_us, &data_info);
	structObject.updateGet();
	return result;
}

bool GetLatest(SharedMemoryContentWrapper& structObject, SMT_DataInfo& data_info)
{
	bool result = SMT_GetLatest("SharedMemoryContent", structObject.getSharedMemoryContentPtr(), &data_info);
	structObject.updateGet();
	return result;
}

bool GetLatest(SharedMemoryContentWrapper& structObject)
{
	SMT_DataInfo data_info = {0,0,0};
	bool result = SMT_GetLatest("SharedMemoryContent", structObject.getSharedMemoryContentPtr(), &data_info);
	structObject.updateGet();
	return result;
}

bool Publish(SharedMemoryContentWrapper& structObject)
{
	structObject.updatePublish();
	return SMT_Publish("SharedMemoryContent", structObject.getSharedMemoryContentPtr(), sizeof(sm_data::SharedMemoryContent));
}

bool GetOldest(SharedMemoryContentWrapper& structObject, SMT_DataInfo& data_info)
{
	bool result =  SMT_GetOldest("SharedMemoryContent", structObject.getSharedMemoryContentPtr(), &data_info);
	structObject.updateGet();
	return result;
}

bool GetOldest(SharedMemoryContentWrapper& structObject)
{
	SMT_DataInfo data_info = {0,0,0};
	bool result =  SMT_GetOldest("SharedMemoryContent", structObject.getSharedMemoryContentPtr(), &data_info);
	structObject.updateGet();
	return result;
}

bool GetByCounter(testStructThreeWrapper& structObject, uint32_t counter, uint64_t timeout_us, SMT_DataInfo& data_info)
{
	bool result = SMT_GetByCounter("testStructThree", structObject.gettestStructThreePtr(), counter, timeout_us, &data_info);
	structObject.updateGet();
	return result;
}

bool GetByCounter(testStructThreeWrapper& structObject, uint32_t counter, uint64_t timeout_us)
{
	SMT_DataInfo data_info = {0,0,0};
	bool result = SMT_GetByCounter("testStructThree", structObject.gettestStructThreePtr(), counter, timeout_us, &data_info);
	structObject.updateGet();
	return result;
}

bool GetLatest(testStructThreeWrapper& structObject, SMT_DataInfo& data_info)
{
	bool result = SMT_GetLatest("testStructThree", structObject.gettestStructThreePtr(), &data_info);
	structObject.updateGet();
	return result;
}

bool GetLatest(testStructThreeWrapper& structObject)
{
	SMT_DataInfo data_info = {0,0,0};
	bool result = SMT_GetLatest("testStructThree", structObject.gettestStructThreePtr(), &data_info);
	structObject.updateGet();
	return result;
}

bool Publish(testStructThreeWrapper& structObject)
{
	structObject.updatePublish();
	return SMT_Publish("testStructThree", structObject.gettestStructThreePtr(), sizeof(sm_data::testStructThree));
}

bool GetOldest(testStructThreeWrapper& structObject, SMT_DataInfo& data_info)
{
	bool result =  SMT_GetOldest("testStructThree", structObject.gettestStructThreePtr(), &data_info);
	structObject.updateGet();
	return result;
}

bool GetOldest(testStructThreeWrapper& structObject)
{
	SMT_DataInfo data_info = {0,0,0};
	bool result =  SMT_GetOldest("testStructThree", structObject.gettestStructThreePtr(), &data_info);
	structObject.updateGet();
	return result;
}

bool GetByCounter(sm_data::testStructOne& structObject, uint32_t counter, uint64_t timeout_us, SMT_DataInfo& data_info)
{
	return SMT_GetByCounter("testStructOne", &structObject, counter, timeout_us, &data_info);
}

bool GetByCounter(sm_data::testStructOne& structObject, uint32_t counter, uint64_t timeout_us)
{
	SMT_DataInfo data_info = SMT_DataInfo{0,0,0};
	return SMT_GetByCounter("testStructOne", &structObject, counter, timeout_us, &data_info);
}

bool GetLatest(sm_data::testStructOne& structObject, SMT_DataInfo& data_info)
{
	return SMT_GetLatest("testStructOne", &structObject, &data_info);
}

bool GetLatest(sm_data::testStructOne& structObject)
{
	SMT_DataInfo data_info = SMT_DataInfo{0,0,0};
	return SMT_GetLatest("testStructOne", &structObject, &data_info);
}

bool Publish(sm_data::testStructOne& structObject)
{
	return SMT_Publish("testStructOne", &structObject, sizeof(sm_data::testStructOne));
}

bool GetOldest(sm_data::testStructOne& structObject, SMT_DataInfo& data_info)
{
	return SMT_GetOldest("testStructOne", &structObject, &data_info);
}

bool GetOldest(sm_data::testStructOne& structObject)
{
	SMT_DataInfo data_info = SMT_DataInfo{0,0,0};
	return SMT_GetOldest("testStructOne", &structObject, &data_info);
}

bool GetByCounter(testStructTwoWrapper& structObject, uint32_t counter, uint64_t timeout_us, SMT_DataInfo& data_info)
{
	return SMT_GetByCounter("testStructTwo", structObject.gettestStructTwoPtr(), counter, timeout_us, &data_info);
}

bool GetByCounter(testStructTwoWrapper& structObject, uint32_t counter, uint64_t timeout_us)
{
	SMT_DataInfo data_info = SMT_DataInfo{0,0,0};
	return SMT_GetByCounter("testStructTwo", structObject.gettestStructTwoPtr(), counter, timeout_us, &data_info);
}

bool GetLatest(testStructTwoWrapper& structObject, SMT_DataInfo& data_info)
{
	return SMT_GetLatest("testStructTwo", structObject.gettestStructTwoPtr(), &data_info);
}

bool GetLatest(testStructTwoWrapper& structObject)
{
	SMT_DataInfo data_info = SMT_DataInfo{0,0,0};
	return SMT_GetLatest("testStructTwo", structObject.gettestStructTwoPtr(), &data_info);
}

bool Publish(testStructTwoWrapper& structObject)
{
	return SMT_Publish("testStructTwo", structObject.gettestStructTwoPtr(), sizeof(sm_data::testStructTwo));
}

bool GetOldest(testStructTwoWrapper& structObject, SMT_DataInfo& data_info)
{
	return SMT_GetOldest("testStructTwo", structObject.gettestStructTwoPtr(), &data_info);
}

bool GetOldest(testStructTwoWrapper& structObject)
{
	SMT_DataInfo data_info = SMT_DataInfo{0,0,0};
	return SMT_GetOldest("testStructTwo", structObject.gettestStructTwoPtr(), &data_info);
}

bool GetByCounter(testStructFourWrapper& structObject, uint32_t counter, uint64_t timeout_us, SMT_DataInfo& data_info)
{
	bool result = SMT_GetByCounter("testStructFour", structObject.gettestStructFourPtr(), counter, timeout_us, &data_info);
	structObject.updateGet();
	return result;
}

bool GetByCounter(testStructFourWrapper& structObject, uint32_t counter, uint64_t timeout_us)
{
	SMT_DataInfo data_info = {0,0,0};
	bool result = SMT_GetByCounter("testStructFour", structObject.gettestStructFourPtr(), counter, timeout_us, &data_info);
	structObject.updateGet();
	return result;
}

bool GetLatest(testStructFourWrapper& structObject, SMT_DataInfo& data_info)
{
	bool result = SMT_GetLatest("testStructFour", structObject.gettestStructFourPtr(), &data_info);
	structObject.updateGet();
	return result;
}

bool GetLatest(testStructFourWrapper& structObject)
{
	SMT_DataInfo data_info = {0,0,0};
	bool result = SMT_GetLatest("testStructFour", structObject.gettestStructFourPtr(), &data_info);
	structObject.updateGet();
	return result;
}

bool Publish(testStructFourWrapper& structObject)
{
	structObject.updatePublish();
	return SMT_Publish("testStructFour", structObject.gettestStructFourPtr(), sizeof(sm_data::testStructFour));
}

bool GetOldest(testStructFourWrapper& structObject, SMT_DataInfo& data_info)
{
	bool result =  SMT_GetOldest("testStructFour", structObject.gettestStructFourPtr(), &data_info);
	structObject.updateGet();
	return result;
}

bool GetOldest(testStructFourWrapper& structObject)
{
	SMT_DataInfo data_info = {0,0,0};
	bool result =  SMT_GetOldest("testStructFour", structObject.gettestStructFourPtr(), &data_info);
	structObject.updateGet();
	return result;
}
