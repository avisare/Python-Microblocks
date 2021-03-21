#pragma once
#include "Shared_Memory_Topics_API.h"
#include "GenericWrapperHandler.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <iostream>
class NavCov_RecordTopic
{
private:
	std::string _topicName;
	int _topicSize;
public:
	NavCov_RecordTopic()
	{
		_topicName="NavCov_RecordTopic";
		_topicSize=8;
	}

	bool GetByCounter(void* structObject, uint32_t counter, uint64_t timeout_us, SMT_DataInfo& data_info)
	{
		return SMT_GetByCounter(_topicName.c_str(), structObject, counter, timeout_us, &data_info);
	}

	bool GetByCounter(void* structObject, uint32_t counter, uint64_t timeout_us)
	{
		SMT_DataInfo data_info = SMT_DataInfo{0,0,0};
		return SMT_GetByCounter(_topicName.c_str(), structObject, counter, timeout_us, &data_info);
	}

	bool GetLatest(void* structObject, SMT_DataInfo& data_info)
	{
		return SMT_GetLatest(_topicName.c_str(), structObject, &data_info);
	}

	bool GetLatest(void* structObject)
	{
		SMT_DataInfo data_info = SMT_DataInfo{0,0,0};
		return SMT_GetLatest(_topicName.c_str(), structObject, &data_info);
	}

	bool Publish(void* structObject)
	{
		return SMT_Publish(_topicName.c_str(), structObject, _topicSize);
	}

	bool Publish(void* structObject, size_t size)
	{
		return SMT_Publish(_topicName.c_str(), structObject, size);
	}

	bool GetOldest(void* structObject, SMT_DataInfo& data_info)
	{
		return SMT_GetOldest(_topicName.c_str(), structObject, &data_info);
	}

	bool GetOldest(void* structObject)
	{
		SMT_DataInfo data_info = SMT_DataInfo{0,0,0};
		return SMT_GetOldest(_topicName.c_str(), structObject, &data_info);
	}
};
class testTopic
{
private:
	std::string _topicName;
	int _topicSize;
public:
	testTopic()
	{
		_topicName="testTopic";
		_topicSize=440;
	}

	bool GetByCounter(void* structObject, uint32_t counter, uint64_t timeout_us, SMT_DataInfo& data_info)
	{
		bool result = SMT_GetByCounter(_topicName.c_str(), ((testWrapper*)structObject)->getPtr(), counter, timeout_us, &data_info);
		((testWrapper*)structObject)->updateGet();
		return result;
	}

	bool GetByCounter(void* structObject, uint32_t counter, uint64_t timeout_us)
	{
		SMT_DataInfo data_info = SMT_DataInfo{0,0,0};
		bool result = SMT_GetByCounter(_topicName.c_str(), ((testWrapper*)structObject)->getPtr(), counter, timeout_us, &data_info);
		((testWrapper*)structObject)->updateGet();
		return result;
	}

	bool GetLatest(void* structObject, SMT_DataInfo& data_info)
	{
		bool result = SMT_GetLatest(_topicName.c_str(), ((testWrapper*)structObject)->getPtr(), &data_info);
		((testWrapper*)structObject)->updateGet();
		return result;
	}

	bool GetLatest(void* structObject)
	{
		SMT_DataInfo data_info = SMT_DataInfo{0,0,0};
		bool result = SMT_GetLatest(_topicName.c_str(), ((testWrapper*)structObject)->getPtr(), &data_info);
		((testWrapper*)structObject)->updateGet();
		return result;
	}

	bool Publish(void* structObject)
	{
		((SharedMemoryContentWrapper*)structObject)->updatePublish();
		return SMT_Publish(_topicName.c_str(), ((testWrapper*)structObject)->getPtr(), _topicSize);
	}

	bool Publish(void* structObject, size_t size)
	{
		((SharedMemoryContentWrapper*)structObject)->updatePublish();
		return SMT_Publish(_topicName.c_str(), ((testWrapper*)structObject)->getPtr(), size);
	}

	bool GetOldest(void* structObject, SMT_DataInfo& data_info)
	{
		bool result = SMT_GetOldest(_topicName.c_str(), ((testWrapper*)structObject)->getPtr(), &data_info);
		((testWrapper*)structObject)->updateGet();
		return result;
	}

	bool GetOldest(void* structObject)
	{
		SMT_DataInfo data_info = SMT_DataInfo{0,0,0};
		bool result = SMT_GetOldest(_topicName.c_str(), ((testWrapper*)structObject)->getPtr(), &data_info);
		((testWrapper*)structObject)->updateGet();
		return result;
	}
};
