## 1. Log Class

Logging is crucial during development and debugging, and it serves as a great example.

```cpp
#include <iostream>

class Log
{
public:  // public methods, variables, and static variables can be separated
	const int LogLevelError = 0;
	const int LogLevelWarning = 1;
	const int LogLevelInfo = 2;
private:
	int m_LogLevel = LogLevelInfo;  // stands for member
public:
	void SetLevel(int level)
	{
		m_LogLevel = level; // helps distinguish between member variables and local variables
	}

	void Error(const char* message)
	{
		if (m_LogLevel >= LogLevelError)
			std::cout << "[ERROR]:" << message << std::endl;
	}

	void Warn(const char* message)
	{
		if (m_LogLevel >= LogLevelWarning)
			std::cout << "[WARNING]:" << message << std::endl;
	}

	void Info(const char* message)
	{
		if (m_LogLevel >= LogLevelInfo)
		std::cout << "[INFO]:" << message << std::endl;
	}
};

int main()
{
	Log log;
	log.SetLevel(log.LogLevelWarning);  // m_LogLevel = 1
	log.Warn("Hello!");
	log.Error("Hello!");
	log.Info("Hello");    // Warn + Error 
	std::cin.get();
}
```

This code is quite rough, but it follows a general approach. That is, first write the methods and variables that might be used in `main`, and then expand the class. Later, we will learn how to improve it.

```cpp
class Log
{
public:
	enum Level
	{
		LevelError = 0, LevelWarning, LevelInfo
	};
private:
	Level m_LogLevel = LevelInfo;  
public:
	void SetLevel(Level level)
	{
		m_LogLevel = level; 
	}

	void Error(const char* message)
	{
		if (m_LogLevel >= LevelError)
			std::cout << "[ERROR]:" << message << std::endl;
	}

	void Warn(const char* message)
	{
		if (m_LogLevel >= LevelWarning)
			std::cout << "[WARNING]:" << message << std::endl;
	}

	void Info(const char* message)
	{
		if (m_LogLevel >= LevelInfo)
			std::cout << "[INFO]:" << message << std::endl;
	}
};

int main()
{
	Log log;
	log.SetLevel(log.LevelError);  // m_LogLevel = 0, Log::LevelError
	log.Warn("Hello!");
	log.Error("Hello!");
	log.Info("Hello");    // Warn + Error 
	std::cin.get();
}
```