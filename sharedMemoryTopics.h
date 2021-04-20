#pragma once

#pragma warning( disable:4267 )

#include "NavCov_RecordClass.h"

#include "NavData_SpeedClass.h"

#include "NavData_PositionClass.h"

#include "NavData_QuaternionClass.h"

#include "NavData_EulerAngelsClass.h"

#include "NavData_RecordClass.h"

#include "enums.h"

#include "Shared_Memory_Topics_API.h"

#include <iostream>


std::map<std::string, std::array<uint32_t, 3>> getTopicsInfo()
{
	std::map<std::string, std::array<uint32_t, 3>> topicsInfo;
	topicsInfo["NavCov_01"] = { 256, 10, 20};
	topicsInfo["NavData_01"] = { 256, 100, 120};
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
class NavCov_01
{
private:
	std::string _topicName;
	int _topicSize;
public:
	NavCov_01()
	{
		_topicName="NavCov_01";
		_topicSize=256;
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
class NavData_01
{
private:
	std::string _topicName;
	int _topicSize;
public:
	NavData_01()
	{
		_topicName="NavData_01";
		_topicSize=256;
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
