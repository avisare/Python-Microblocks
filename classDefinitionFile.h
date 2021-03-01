
class SharedMemoryContentWrapper
{
public:
	SharedMemoryContentWrapper();
	void updatePublish();
	void updateGet();
	uint32_t getintData() const;
	void setintData(uint32_t setVarintData);
	std::vector<char> cstringData;
	sm_data::SharedMemoryContent* getSharedMemoryContentPtr();
private:
	sm_data::SharedMemoryContent _SharedMemoryContent;
};

class testStructThreeWrapper
{
public:
	testStructThreeWrapper();
	void updatePublish();
	void updateGet();
	bool getbooleanValue() const;
	void setbooleanValue(bool setVarbooleanValue);
	std::vector<char> charArray;
	sm_data::testStructThree* gettestStructThreePtr();
private:
	sm_data::testStructThree _testStructThree;
};

class testStructTwoWrapper
{
public:
	testStructTwoWrapper();

	long getlongNumber() const;
	void setlongNumber(long setVarlongNumber);
	unsigned int getuintNumber() const;
	void setuintNumber(unsigned int setVaruintNumber);
	bool getboolean() const;
	void setboolean(bool setVarboolean);
	testStructThreeWrapper& getstructThree() const;
	void setstructThree(testStructThreeWrapper setstructThree);
	sm_data::testStructTwo* gettestStructTwoPtr();
private:
	sm_data::testStructTwo _testStructTwo;
	testStructThreeWrapper _structThree;
};

class testStructFourWrapper
{
public:
	testStructFourWrapper();
	void updatePublish();
	void updateGet();
	int getsingleInteger() const;
	void setsingleInteger(int setVarsingleInteger);
	std::vector<int> intArray;
	sm_data::testStructFour* gettestStructFourPtr();
private:
	sm_data::testStructFour _testStructFour;
};
