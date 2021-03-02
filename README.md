# Welcome to Shared Memory Wrapper Module!

In this file you can find all the **necessary** documentation about the shared memory wrapper module, and about how to use it correctly.


# How it works

So basically, all the functions that exists in the shared memory topic dynamic library can be accessible by **python!!**
By using pybind11 library, I created python module that bind between c++ dynamic library and python code. 

# How to use

In order to use the module, all you need to do is import it in the top of your python file, like :`import SharedMemoryWrapper`.

After that, if you want to use for example,the `SMT_Init` function, just type the module name following by a dot, and after that the name of the function with the corresponding arguments.

For example:
`SharedMemoryWrapper.SMT_Init()`  

Another example:
`SharedMemoryWrapper.SMT_Show("topic name")`

Couple of things to keep in mind:

1. using lists in the wrapper is quite different then python:
`array = intList({1,2,3})` creating integer list
   
`array[1] = 4` change the second number in the list

 `array.append(6)` add 6 to the list

 `array.pop()` remove the last inserted element from the list and return it

`string = charList({'a','b','c'})`   in string you can do this also

!!WARNING you cant use this initalization in order to save the original letters order.
In oreder to save the original order, use the following initialize or append each letter seperately.

`string = charList('abc')`   this is also work

2. The float type in the dll does not precise,
in order to precise the value of returning float from function (for example),
download numpy module (pip install numpy) and wrap the return value with:
`numpy.float32(function_that_return_float())`
#Struct Available 
Currently, the Shared memory wrapper support couple of  struct that can be read and write from the shared memory

The structs are:
1.
```c
struct SharedMemoryContent
{
	uint32_t intData;
	char	 cstringData[CSTRING_DATA_MAX_LEN];
};
```
2.
```c
struct testStructOne
{
	int intNumber;
	float floatNumber;
	char character;
};
```
3.
```c
struct testStructTwo
{
	long longNumber;
	unsigned int uintNumber;
	bool boolean;
	struct testStructThree structThree;
};
```
4.
```c
struct testStructThree
{
	bool booleanValue;
	float floatValue;
	char charArray[CSTRING_DATA_MAX_LEN];
	// CSTRING_DATA_MAX_LEN = 32
};
```
5.
```c
struct testStructFour
{
	int singleInteger;
	int intArray[INT_ARRAY_MAX_LEN];
	// INT_ARRAY_MAX_LEN = 10
};
```

6. 
```c
struct SMT_DataInfo
{
	unsigned int m_dataSize;
	unsigned int m_publishCount;
	uint64_t m_publishTime;
};
```

# Functions
This version of the wrapper module contains access to the following functions:
___
**Function Name:**  SMT_Version

**Function Signature:**  const char* SMT_Version();
Return the version as null terminated string.

**Parameters:**  none

**Returns:**  pointer to version in string format
___
**Function Name:**  SMT_Init

**Function Signature**: bool SMT_Init();
Shared memory topic's initialization. should be called only once.

**Parameters:**  none

**Returns:** true for initialization success, false otherwise
___
**Function Name:** SMT_Show

**Function Signature:** void SMT_Show(const char* topicName);
Print general status and topics information to stdout.

**Parameters:** none

**Returns:** void
___
**Function Name:** SMT_CreateTopic

**Function Signature:**  bool SMT_CreateTopic(const char* topicName, const uint32_t maxDataSize, const uint32_t historyDepth, const uint32_t cellsCount);
 Create and initialize a particular shared memory topic by name.

**Parameters:** const char* topicName, const uint32_t maxDataSize, const uint32_t historyDepth, const uint32_t cellsCount

**Returns:** true for initialization success, false otherwise
___
 **Function Name:** send/publish
 
**Function Signature:** bool send(const char* topicName, void* ptr, uint32_t size);

Create and initialize a particular shared memory topic by name.

**Function Signature:** bool publish(const char* topicName, void* ptr, uint32_t size);

**Parameters:** const char* topicName, void* ptr, uint32_t counter, uint64_t timeout_us

**Returns:** true for initialization success, false otherwise
___
**Function Name:** receive/getByCounter

**Function Signature:** bool receive(const char* topicName, void* ptr, uint32_t counter, uint64_t timeout_us);

**Function Signature:** bool getByCounter(const char* topicName, void* ptr, uint32_t counter, uint64_t timeout_us);

**Overload:** bool receive(const char* topicName, void* ptr, uint32_t counter, uint64_t timeout_us, SMT_DataInfo data_info);

Get a shared memory publication by counter. returns false if times.

**Parameters:**

const char* topicName, void* ptr, uint32_t counter, uint64_t timeout_us, , SMT_DataInfo data_info (optional)

**IMPORTANT:** counter starts at 1

**Returns:** true for publication existed and copied, false if timed out or topic not exist in history.

**Data info:** Return info about the topic which got, in the data info struct

**WARNING:** ptr must be allocated enough space to copy data, otherwise risk access violation
___
**Function Name:** latestRx/getLatest

**Function Signature:**  bool latestRx(const char* topicName, void* ptr);

**Function Signature:**  bool getLatest(const char* topicName, void* ptr);

**Overload:** bool latestRx(const char* topicName, void* ptr, SMT_DataInfo data_info);

Return the latest valid data item in the history

**Parameters:** const char* topicName, void* ptr, , SMT_DataInfo data_info (optional)

**Returns:** true for publication existed and copied, false if topic not exist.

**Data info:** Return info about the topic which got, in the data info struct

**WARNING:** ptr must be allocated enough space to copy data, otherwise risk access violation
___
**Function Name:** oldestRx/getOldest

**Function Signature:**  bool oldestRx(const char* topicName, void* ptr);

**Function Signature:**  bool getOldest(const char* topicName, void* ptr);

**Overload:**  bool oldestRx(const char* topicName, void* ptr, SMT_DataInfo data_info);
Return the oldest valid data item in the history

**Parameters:** const char* topicName, void* ptr, SMT_DataInfo data_info (optional)

**Returns:** true for publication existed and copied, false if topic not exist.

**Data info:** Return info about the topic which got, in the data info struct

**WARNING:** ptr must be allocated enough space to copy data, otherwise risk access violation
___
**Function Name:** SMT_GetPublishCount
 
**Function Signature:** int SMT_GetPublishCount(const char* topicName);
Get the publish count of a particular topic.

**Parameters:** const char* topicName

**Returns:** amount of times topic has been published successfully. 0 if topic does not exist
___
**Function Name:** SMT_ClearHistory

**Function Signature:**  bool SMT_ClearHistory(const char* topicName);
Clear the history a particular topic. All 'get' functions will fail until new publish

**Parameters:** const char* topicName

**Returns:** true if topic exists, false otherwise
___
# Try it yourself
There is an example.py file in the download folder, open and run it
> If you would like to hear more about the wrapper, or you are facing any kind of problem with it, reach me whenever you want.
> @Noam Mizrahi
