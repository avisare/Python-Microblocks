SharedMemoryContentWrapper::SharedMemoryContentWrapper()
{
	_SharedMemoryContent = {};
}
void SharedMemoryContentWrapper::updatePublish()
{
	int max_index = (cstringData.size() >= CSTRING_DATA_MAX_LEN) ? CSTRING_DATA_MAX_LEN : cstringData.size();
	for (int i = 0; i < max_index; i++)
	{
		_SharedMemoryContent.cstringData[i] = cstringData[i];
	}
}
void SharedMemoryContentWrapper::updateGet()
{
	cstringData.clear();
	for (int i = 0; i < CSTRING_DATA_MAX_LEN; i++)
	{
		cstringData.push_back(_SharedMemoryContent.cstringData[i]);
	}
}
uint32_t SharedMemoryContentWrapper::getintData() const
{
	return _SharedMemoryContent.intData;
}
void SharedMemoryContentWrapper::setintData(uint32_t setVarintData)
{
	_SharedMemoryContent.intData = setVarintData;
}
sm_data::SharedMemoryContent* SharedMemoryContentWrapper::getSharedMemoryContentPtr()
{
	return &_SharedMemoryContent;
}
testStructThreeWrapper::testStructThreeWrapper()
{
	_testStructThree = {};
}
void testStructThreeWrapper::updatePublish()
{
	int max_index = (charArray.size() >= CSTRING_DATA_MAX_LEN) ? CSTRING_DATA_MAX_LEN : charArray.size();
	for (int i = 0; i < max_index; i++)
	{
		_testStructThree.charArray[i] = charArray[i];
	}
}
void testStructThreeWrapper::updateGet()
{
	charArray.clear();
	for (int i = 0; i < CSTRING_DATA_MAX_LEN; i++)
	{
		charArray.push_back(_testStructThree.charArray[i]);
	}
}
bool testStructThreeWrapper::getbooleanValue() const
{
	return _testStructThree.booleanValue;
}
void testStructThreeWrapper::setbooleanValue(bool setVarbooleanValue)
{
	_testStructThree.booleanValue = setVarbooleanValue;
}
sm_data::testStructThree* testStructThreeWrapper::gettestStructThreePtr()
{
	return &_testStructThree;
}
testStructTwoWrapper::testStructTwoWrapper()
{
	_testStructTwo = {};
}
long testStructTwoWrapper::getlongNumber() const
{
	return _testStructTwo.longNumber;
}
void testStructTwoWrapper::setlongNumber(long setVarlongNumber)
{
	_testStructTwo.longNumber = setVarlongNumber;
}
unsigned testStructTwoWrapper::int getuintNumber() const
{
	return _testStructTwo.uintNumber;
}
void testStructTwoWrapper::setuintNumber(unsigned int setVaruintNumber)
{
	_testStructTwo.uintNumber = setVaruintNumber;
}
bool testStructTwoWrapper::getboolean() const
{
	return _testStructTwo.boolean;
}
void testStructTwoWrapper::setboolean(bool setVarboolean)
{
	_testStructTwo.boolean = setVarboolean;
}
testStructThreeWrapper& testStructTwoWrapper::getstructThree() const
{
	return _structThree;
}
void testStructTwoWrapper::setstructThree(testStructThreeWrapper setstructThree)
{
	_structThree = setstructThree;
}
sm_data::testStructTwo* testStructTwoWrapper::gettestStructTwoPtr()
{
	return &_testStructTwo;
}
testStructFourWrapper::testStructFourWrapper()
{
	_testStructFour = {};
}
void testStructFourWrapper::updatePublish()
{
	int max_index = (intArray.size() >= INT_ARRAY_MAX_LEN) ? INT_ARRAY_MAX_LEN : intArray.size();
	for (int i = 0; i < max_index; i++)
	{
		_testStructFour.intArray[i] = intArray[i];
	}
}
void testStructFourWrapper::updateGet()
{
	intArray.clear();
	for (int i = 0; i < INT_ARRAY_MAX_LEN; i++)
	{
		intArray.push_back(_testStructFour.intArray[i]);
	}
}
int testStructFourWrapper::getsingleInteger() const
{
	return _testStructFour.singleInteger;
}
void testStructFourWrapper::setsingleInteger(int setVarsingleInteger)
{
	_testStructFour.singleInteger = setVarsingleInteger;
}
sm_data::testStructFour* testStructFourWrapper::gettestStructFourPtr()
{
	return &_testStructFour;
}
