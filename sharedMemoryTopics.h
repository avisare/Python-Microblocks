#pragma once

#pragma warning( disable:4267 )

#include "tClass.h"

#include "SharedMemoryContentClass.h"

#include "testStructOneClass.h"

#include "testStructThreeClass.h"

#include "testStructTwoClass.h"

#include "testStructFourClass.h"

#include "SharedMemoryContentClass.h"

#include "Shared_Memory_Topics_API.h"

#include <iostream>


std::map<std::string, std::array<uint32_t, 3>> getTopicsInfo()
{
	std::map<std::string, std::array<uint32_t, 3>> topicsInfo;
	topicsInfo["SharedMemoryContentTopic"] = { 52, 3, 10};
	topicsInfo["testStructOneTopic"] = { 25, 4, 10};
	topicsInfo["testStructTwoTopic"] = { 52, 2, 7};
	topicsInfo["testStructThreeTopic"] = { 40, 3, 10};
	topicsInfo["testStructFourTopic"] = { 152, 5, 12};
	return topicsInfo;
}
struct topicsInfo
{
	static std::map<std::string, std::array<uint32_t, 3>> topicsInfoMap;
};
std::map<std::string, std::array<uint32_t, 3>> topicsInfo::topicsInfoMap = getTopicsInfo();
bool SMT_CreateTopic(std::string topicName)
{
	if (topicsInfo::topicsInfoMap.find(topicName) == topicsInfo::topicsInfoMap.end())
	{
		std::cerr << "ERROR!! No topic named " + topicName << std::endl;
		return false;
	}
	else
	{
		auto topic_info = topicsInfo::topicsInfoMap[topicName];
		return SMT_CreateTopic(topicName.c_str(), topic_info[0], topic_info[1], topic_info[2]);
	}
}
class SharedMemoryContentTopic
{
private:
	std::string _topicName;
	int _topicSize;
public:
	SharedMemoryContentTopic()
	{
		_topicName="SharedMemoryContentTopic";
		_topicSize=52;
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
class testStructTwoTopic
{
private:
	std::string _topicName;
	int _topicSize;
public:
	testStructTwoTopic()
	{
		_topicName="testStructTwoTopic";
		_topicSize=52;
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
		_topicSize=40;
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
		_topicSize=152;
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
