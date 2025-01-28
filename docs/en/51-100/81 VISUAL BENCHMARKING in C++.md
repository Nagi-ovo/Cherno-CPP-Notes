# How to Visually Measure Performance. Prerequisite Knowledge: [74 BENCHMARKING in C++ (how to measure performance)](<74%20BENCHMARKING%20in%20C++%20(how%20to%20measure%20performance).md>)

## 1. Basic Benchmark

```cpp
#include "pch.h"
#include <cmath>
#include <chrono>

class Timer // Benchmarking, see lesson 74
{
public:
	Timer(const char* name)
		: m_Name(name), m_Stopped(false)
	{
		m_StartTimepoint = std::chrono::high_resolution_clock::now();
	}

	void Stop()
	{
		auto endTimepoint = std::chrono::high_resolution_clock::now();

		long long start = std::chrono::time_point_cast<std::chrono::milliseconds>(m_StartTimepoint).time_since_epoch().count();
		auto end = std::chrono::time_point_cast<std::chrono::milliseconds>(endTimepoint).time_since_epoch().count(); // also long long

		std::cout << m_Name << ": " << (end - start) << "ms\n";

		m_Stopped = true;
	}

	~Timer()
	{
		if (m_Stopped = true)
			Stop();
	}

private:
	const char* m_Name;
	std::chrono::time_point<std::chrono::steady_clock> m_StartTimepoint;
	bool m_Stopped;
};

void Function1()
{
	Timer time("Function1");
	for (int i = 0; i < 1000; i++)
		std::cout << "Hello World #" << i << std::endl;
}

void Function2()
{
	Timer time("Function2");
	for (int i = 0; i < 1000; i++)
		std::cout << "Hello World #" << sqrt(i) << std::endl;
}

int main()
{
	Function1();
	Function2();
	std::cin.get();
}

// Results:
/*
HelloWorld#0 ...
HelloWorld#999 ...
Function1: 611ms
HellowWorld#0 ...
Hello World #31.607
Function2: 1037ms
*/
```

Now the results are just numbers, and it's cumbersome to browse through them, so let's move on to the Visualization section:

## 2. Visualization

We are going to use Google Chrome, which I never guessed could be used for visualization analysis...

Chrome comes with its own set of analysis tools and other development tools, clearly aimed at web applications or web pages, and there's a special one called Chrome Tracing, which is very *barebone*, simple and basic, allowing us to visualize our analysis and stack trace views.

Enter `chrome://tracing` to access it, and it's likely already installed on your computer:
![](./storage%20bag/Pasted%20image%2020230804140336.png)

It works by loading a JSON file containing all the data. Our next step is to take all the timing data we recorded with the timer and put it into a JSON format file for Chrome tracing.

```cpp
// Struct ProfileResult, used to store performance test results
struct ProfileResult
{
    std::string Name;  // Test name
    long long Start, End;  // Test start and end time points
    uint32_t ThreadID;  // Thread ID executing the test
};

// Struct InstrumentationSession, used to store information about a test session
struct InstrumentationSession
{
    std::string Name;  // Session name
};

// Class Instrumentor, used for performance testing and result output
class Instrumentor
{
private:
    InstrumentationSession* m_CurrentSession;  // Current test session
    std::ofstream m_OutputStream;  // Output stream, used to write test results
    int m_ProfileCount;  // Records the number of tests completed in the current session
public:
    // Constructor
    Instrumentor()
        : m_CurrentSession(nullptr), m_ProfileCount(0)
    {
    }

    // Start a new test session
    void BeginSession(const std::string& name, const std::string& filepath = "results.json")
    {
        m_OutputStream.open(filepath);  // Open output file
        WriteHeader();  // Write the header information of the test results
        m_CurrentSession = new InstrumentationSession{ name };  // Create a new session
    }

    // End the current test session
    void EndSession()
    {
        WriteFooter();  // Write the footer information of the test results
        m_OutputStream.close();  // Close the output file
        delete m_CurrentSession;  // Delete the current session
        m_CurrentSession = nullptr;  // Set the current session pointer to nullptr
        m_ProfileCount = 0;  // Reset the test count
    }

    // Write a test result to the output file
    void WriteProfile(const ProfileResult& result)
    {
        if (m_ProfileCount++ > 0)
            m_OutputStream << ",";  // If there are already test results, add a comma before the new test result

        // Handle possible double quote characters in the test name
        std::string name = result.Name;
        std::replace(name.begin(), name.end(), '"', '\'');

        // Write the test result
        // The test result format is JSON, containing test name, start and end time, thread ID, etc.
        m_OutputStream << "{";
        m_OutputStream << "\"cat\":\"function\",";
        m_OutputStream << "\"dur\":" << (result.End - result.Start) << ',';
        m_OutputStream << "\"name\":\"" << name << "\",";
        m_OutputStream << "\"ph\":\"X\",";
        m_OutputStream << "\"pid\":0,";
        m_OutputStream << "\"tid\":" << result.ThreadID << ",";
        m_OutputStream << "\"ts\":" << result.Start;
        m_OutputStream << "}";

        m_OutputStream.flush();  // Flush the output stream to ensure the result is written to the file
    }

    // Write the header information of the test results
    void WriteHeader()
    {
        m_OutputStream << "{\"otherData\": {},\"traceEvents\":[";
        m_OutputStream.flush();
    }

    // Write the footer information of the test results
    void WriteFooter()
    {
        m_OutputStream << "]}";
        m_OutputStream.flush();
    }

    // Get the singleton of Instrumentor
    // Since this is a performance testing tool, we usually only need one instance
    static Instrumentor& Get()
    {
        static Instrumentor instance;
        return instance;
    }
};

// Class InstrumentationTimer, used for timing and performance testing
class InstrumentationTimer
{
public:
    // Constructor
    // Start timing when the object is created
    InstrumentationTimer(const char* name)
        : m_Name(name), m_Stopped(false)
    {
        m_StartTimepoint = std::chrono::high_resolution_clock::now();
    }

    // Destructor
    // If the timer is not stopped, automatically stop timing when the object is destroyed and record the test result
    ~InstrumentationTimer()
    {
        if (!m_Stopped)
            Stop();
    }

    // Stop timing and record the test result
    void Stop()
    {
        // Get the current time point
        auto endTimepoint = std::chrono::high_resolution_clock::now();

        // Calculate the start and end time (in microseconds)
        long long start = std::chrono::time_point_cast<std::chrono::microseconds>(m_StartTimepoint).time_since_epoch().count();
        long long end = std::chrono::time_point_cast<std::chrono::microseconds>(endTimepoint).time_since_epoch().count();

        // Get the ID of the current thread
        uint32_t threadID = std::hash<std::thread::id>{}(std::this_thread::get_id());

        // Write the test result to the output file
        Instrumentor::Get().WriteProfile({ m_Name, start, end, threadID });

        m_Stopped = true;  // Mark the timer as stopped
    }
private:
    const char* m_Name;  // Test name
    std::chrono::time_point<std::chrono::high_resolution_clock> m_StartTimepoint;  // Time point when timing started
    bool m_Stopped;  // Mark whether timing has stopped
};

void Function1()
{
	InstrumentationTimer time("Function1");
	for (int i = 0; i < 1000; i++)
		std::cout << "Hello World #" << i << std::endl;
}

void Function2()
{
    InstrumentationTimer time("Function2");
	for (int i = 0; i < 1000; i++)
		std::cout << "Hello World #" << sqrt(i) << std::endl;
}

int main()
{
    Instrumentor::Get().BeginSession("Profile"); // Start session
	Function1();
	Function2();
    Instrumentor::Get().EndSession();
	std::cin.get();
}

```

![](./storage%20bag/Pasted%20image%2020230804153050.png)

![](./storage%20bag/Pasted%20image%2020230804153918.png)

```cpp
void RunBenchmarks()
{
    InstrumentationTimer timer("RunBenchMarks");
    std::cout << "Running Benchmarks...\n";
    Function1();
    Function2();
}

int main()
{
    Instrumentor::Get().BeginSession("Profile");
    RunBenchmarks();
	Instrumentor::Get().EndSession();
	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230804154014.png)

But this RunBenchmark must copy and paste the name of each function we call, which is cumbersome. Additionally, such timing code is not something we want to run in the program all the time. There should be a simple way to turn it off to reduce overhead, so we can write some macros to solve these two problems:

```cpp
#define PROFILING 1
#if PROFILING
#define PROFILE_SCOPE(name) InstrumentationTimer timer##__LINE__(name);
#define PROFILE_FUNCTION() PROFILE_SCOPE(__FUNCTION__)// Predefined macro that returns a string containing the current function name.
#else
#define PROFILE_SCOPE(name)
#endif

void Function1()
{
    PROFILE_FUNCTION();
	for (int i = 0; i < 1000; i++)
		std::cout << "Hello World #" << i << std::endl;
}

void Function2()
{
    PROFILE_FUNCTION();
	for (int i = 0; i < 1000; i++)
		std::cout << "Hello World #" << sqrt(i) << std::endl;
}

void RunBenchmarks()
{
    PROFILE_FUNCTION();
    std::cout << "Running Benchmarks...\n";
    Function1();
    Function2();
```

> Let the preprocessor do the work for us, so we don't have to input strings manually.

If we want more information, such as in cases of function overloading:

![](./storage%20bag/Pasted%20image%2020230804161636.png)

The names printed by these two functions are the same. What if we want the function signature?

Just modify the macro:

```cpp
#define PROFILE_FUNCTION() PROFILE_SCOPE(__FUNCSIG__)// Predefined macro that returns a string containing the current function signature
```

![](./storage%20bag/Pasted%20image%2020230804161705.png)

You can add a namespace, `__FUNGSIG__` will give you all the information:

![](./storage%20bag/Pasted%20image%2020230804162151.png)

Another cool thing supported by ChromeTracing is multithreading. The previous complete code already included threading, but it was not called, so:

```cpp
	void RunBenchmarks()
	{
		PROFILE_FUNCTION();
		std::cout << "Running Benchmarks...\n";
		std::thread a([]() {PrintFunction(1); });
		std::thread b([]() {PrintFunction(); });
		// The last two joins ensure that these two threads complete their work before the Benchmark function truly exits
		a.join();
		b.join();
	}

```

![](./storage%20bag/Pasted%20image%2020230804162801.png)