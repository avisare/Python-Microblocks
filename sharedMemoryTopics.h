#pragma once

#include "SharedMemoryContent.h"

#include "Shared_Memory_Topics_API.h"

#include <pybind11/pybind11.h>

#include <pybind11/stl.h>

#include <pybind11/stl_bind.h>

#include <iostream>

class SharedMemoryContentTopic
{
private:
	std::string _topicName;
	int _topicSize;
public:
	SharedMemoryContentTopic()
	{
		_topicName="SharedMemoryContentTopic";
		_topicSize=36;
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
class testStructOneTopic
{
private:
	std::string _topicName;
	int _topicSize;
public:
	testStructOneTopic()
	{
		_topicName="testStructOneTopic";
		_topicSize=25;
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
class testStructThreeTopic
{
private:
	std::string _topicName;
	int _topicSize;
public:
	testStructThreeTopic()
	{
		_topicName="testStructThreeTopic";
		_topicSize=33;
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
class testStructTwoTopic
{
private:
	std::string _topicName;
	int _topicSize;
public:
	testStructTwoTopic()
	{
		_topicName="testStructTwoTopic";
		_topicSize=42;
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
class testStructFourTopic
{
private:
	std::string _topicName;
	int _topicSize;
public:
	testStructFourTopic()
	{
		_topicName="testStructFourTopic";
		_topicSize=44;
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
