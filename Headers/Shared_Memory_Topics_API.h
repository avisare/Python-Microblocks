#ifndef __SM_TOPIC_API_H__
#define __SM_TOPIC_API_H__

#include <stdint.h>

#ifdef SHARED_MEMORY_TOPICS_IMPLEMENTATION_DLL
#define DECLARE_API_FUNCTION extern "C" __declspec(dllexport)
#elif __linux__
#define DECLARE_API_FUNCTION extern "C" 
#else
#define DECLARE_API_FUNCTION extern "C" __declspec(dllimport)
#endif


////////////////////////////////////////////////////////////////////////////////
// Class Name:  SMT_DataInfo
// Description: Descriptor for the data received by a Reader from the mechanism.
//              It includes getters for the pointer to the buffer, its size,
//              time tag, and running counter.
////////////////////////////////////////////////////////////////////////////////
struct SMT_DataInfo
{
	unsigned int m_dataSize;
	unsigned int m_publishCount;
	uint64_t m_publishTime;
};

///////////////////////////////////////////////////////////////////////////////////////////////////
//  Function: SMT_Version
//    Return the version as null terminated string.
//
//  Parameters:
//    none
//
//  Returns:
//    pointer to version in string format
///////////////////////////////////////////////////////////////////////////////////////////////////
DECLARE_API_FUNCTION const char* SMT_Version();

///////////////////////////////////////////////////////////////////////////////////////////////////
//  Function: SMT_Init
//    Shared memory topic's initialization. should be called only once.
//
//  Parameters:
//    none
//
//  Returns:
//    true for initialization success, false otherwise
///////////////////////////////////////////////////////////////////////////////////////////////////
DECLARE_API_FUNCTION bool SMT_Init();

///////////////////////////////////////////////////////////////////////////////////////////////////
//  Function: SMT_Show
//    Print general status and topics information to stdout.
//
//  Parameters:
//    none
//
//  Returns:
//    void
///////////////////////////////////////////////////////////////////////////////////////////////////
DECLARE_API_FUNCTION void SMT_Show(const char* topicName);

///////////////////////////////////////////////////////////////////////////////////////////////////
//  Function: SMT_CreateTopic
//    Create and initialize a particular shared memory topic by name.
//
//  Parameters:
//    const char* topicName, const uint32_t maxDataSize, const uint32_t historyDepth, const uint32_t cellsCount
//
//  Returns:
//    true for initialization success, false otherwise
///////////////////////////////////////////////////////////////////////////////////////////////////
DECLARE_API_FUNCTION bool SMT_CreateTopic(const char* topicName, const uint32_t maxDataSize, const uint32_t historyDepth, const uint32_t cellsCount);


///////////////////////////////////////////////////////////////////////////////////////////////////
//  Function: SMT_Publish
//    Create and initialize a particular shared memory topic by name.
//
//  Parameters:
//    const char* topicName, void* ptr, uint32_t counter, uint64_t timeout_us
//
//  Returns:
//    true for initialization success, false otherwise
///////////////////////////////////////////////////////////////////////////////////////////////////
DECLARE_API_FUNCTION bool SMT_Publish(const char* topicName, void* ptr, uint32_t size);

///////////////////////////////////////////////////////////////////////////////////////////////////
//  Function: SMT_GetByCounter
//    Get a shared memory publication by counter. returns false if times.
//
//  Parameters:
//    const char* topicName, void* ptr, uint32_t counter, uint64_t timeout_us
//    IMPORTANT: counter starts at 1
//    
//  Returns:
//    true for publication existed and copied, false if timed out or topic not exist in history.
//	  WARNING: ptr must be allocated enough space to copy data, otherwise risk access violation
///////////////////////////////////////////////////////////////////////////////////////////////////
DECLARE_API_FUNCTION bool SMT_GetByCounter(const char* topicName, void* ptr, uint32_t counter, uint64_t timeout_us, SMT_DataInfo* dataInfo);

///////////////////////////////////////////////////////////////////////////////////////////////////
//  Function: SMT_GetLatest
//    Return the latest valid data item in the history
//
//  Parameters:
//    const char* topicName, void* ptr
//
//	  Returns:
//    true for publication existed and copied, false if topic not exist.
//	  WARNING: ptr must be allocated enough space to copy data, otherwise risk access violation
///////////////////////////////////////////////////////////////////////////////////////////////////
DECLARE_API_FUNCTION bool SMT_GetLatest(const char* topicName, void* ptr, SMT_DataInfo* dataInfo);

///////////////////////////////////////////////////////////////////////////////////////////////////
//  Function: SMT_GetOldest
//    Return the oldest valid data item in the history
//
//  Parameters:
//    const char* topicName, void* ptr
//
//	  Returns:
//    true for publication existed and copied, false if topic not exist.
//	  WARNING: ptr must be allocated enough space to copy data, otherwise risk access violation
///////////////////////////////////////////////////////////////////////////////////////////////////
DECLARE_API_FUNCTION bool SMT_GetOldest(const char* topicName, void* ptr, SMT_DataInfo* dataInfo);

///////////////////////////////////////////////////////////////////////////////////////////////////
//  Function: SMT_GetPublishCount
//    Get the publish count of a particular topic.
//
//  Parameters:
//    const char* topicName
//
//	  Returns:
//    amount of times topic has been published successfully. 0 if topic does not exist
///////////////////////////////////////////////////////////////////////////////////////////////////
DECLARE_API_FUNCTION int SMT_GetPublishCount(const char* topicName);

///////////////////////////////////////////////////////////////////////////////////////////////////
//  Function: SMT_ClearHistory
//    Clear the history a particular topic. All 'get' functions will fail until new publish
//
//  Parameters:
//    const char* topicName
//
//	  Returns:
//    true if topic exists, false otherwise
///////////////////////////////////////////////////////////////////////////////////////////////////
DECLARE_API_FUNCTION bool SMT_ClearHistory(const char* topicName);

// --- END OF FILE ---
#endif