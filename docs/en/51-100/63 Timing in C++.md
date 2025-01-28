How do we calculate the time it takes to complete a certain operation or execute a piece of code?

Timing is useful for many things, whether you want certain events to happen at specific times, or simply to evaluate performance or conduct benchmarking to see how fast your code runs. You need to know the actual runtime of your application.

There are several ways to achieve this. Since C++11, we have "chrono," which is part of the C++ library and doesn't require the use of operating system libraries. However, before chrono, if you wanted high-resolution timing, you needed to use operating system libraries. For example, in Windows, there is something called "QueryPerformanceCounter," which we can still use. In fact, if you want more control over timing, such as controlling the CPU's timing capabilities, you might use platform-specific libraries. However, this section will only look at the platform-independent C++ standard library method (part of the chrono library), which can calculate the elapsed time between code executions.

## 1. Platform-Independent Method

Recording the time taken by `sleep_for`:

```cpp
#include <iostream>
#include <chrono>
#include <thread>

int main()
{
	using namespace std::literals::chrono_literals;

	auto start = std::chrono::high_resolution_clock::now();
	std::this_thread::sleep_for(1s);
	auto end = std::chrono::high_resolution_clock::now();

	std::chrono::duration<float> duration = end - start;
	std::cout << duration.count() << "s" << std::endl;

	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230723220443.png)

The chrono library is excellent for high-precision timing and is almost universally applicable across platforms. Therefore, it is highly recommended to use this method for all your timing needs, unless you are doing something specific at a lower level.

## 2. A Smarter Approach

You want to time a function:

```cpp
void Function()
{
	for (int i = 0; i < 100; i++)
		std::cout << "Hello" << std::endl; // We want to measure the time taken by these cout statements
}
```

Setting up a simple struct:

```cpp
struct Timer
{
	std::chrono::time_point<std::chrono::steady_clock> start, end;
	std::chrono::duration<float> duration;
	Timer()
	{
		start = std::chrono::high_resolution_clock::now();
	}
	~Timer()
	{
		end = std::chrono::high_resolution_clock::now();
		duration = end - start;
			float ms = duration.count() * 1000.0f;
		std::cout << "Timer took" << ms << "ms" << std::endl;
	}
};

void Function()
{
	Timer timer;  // Use constructor and destructor for timing
	for (int i = 0; i < 100; i++)
		std::cout << "Hello" << std::endl; // We want to measure the time taken by these cout statements
}

int main()
{
	Function();

	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230723222600.png)

You can optimize performance by replacing `endl` with `\n`.
![](./storage%20bag/Pasted%20image%2020230723222922.png)