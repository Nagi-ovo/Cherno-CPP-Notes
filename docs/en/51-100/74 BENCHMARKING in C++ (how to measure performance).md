## 1. Benchmarking

Benchmarking here is not just a tool you use to benchmark your code; it's about how to correctly write C++ code if you want to measure its performance. There are multiple ways to measure the performance of C++ code, and here we only discuss the method used by Cherno.

First, let's write some code that we want to test:

```cpp
int main()
{
	int value = 0;
	for (int i = 0; i < 1000000; i++)
		value += 2;

	std::cout << value << std::endl;   // 2000000

	__debugbreak(); // VS-specific syntax for breakpoints
}
```

Now, to analyze how fast our code is, we can create a simple scoped timer (refer to [63 Timing in C++](63%20Timing%20in%20C++.md)):

```cpp
#include <chrono>

class Timer
{
private:
	std::chrono::time_point<std::chrono::high_resolution_clock> m_StartTimepoint;
public:
	Timer()
	{
		m_StartTimepoint = std::chrono::high_resolution_clock::now();
	}

	~Timer()
	{
		Stop();
	}
	void Stop()
	{
		auto endTimepoint = std::chrono::high_resolution_clock::now();

		auto start = std::chrono::time_point_cast<std::chrono::microseconds>(m_StartTimepoint).time_since_epoch().count();

		auto end = std::chrono::time_point_cast<std::chrono::microseconds>(endTimepoint).time_since_epoch().count();

		auto duration = end - start;
		double ms = duration * 0.001;

		std::cout << duration << "us (" << ms << "ms)\n";
	}
};

int main()
{
	int value = 0; // Moved outside the scope to ensure it can be printed
	{
		Timer timer;
		for (int i = 0; i < 1000000; i++)
			value += 2;
	}
	std::cout << value << std::endl;
	__debugbreak();
}
```

Output of the timer:
![](./storage%20bag/Pasted%20image%2020230731161600.png)

It's important to ensure that what you're measuring is actually the compiled code, because in Release mode, the compiler optimizes the assembly instructions. In this example, it only records the time needed to print the variable 1E8480h (two million) (since the print is outside the scope, it even counts nothing):
![](./storage%20bag/Pasted%20image%2020230731162520.png)

Instead of the time you want to measure for adding a million times:
![](./storage%20bag/Pasted%20image%2020230731162208.png)

## 2. Performance Comparison of Smart Pointers

```cpp
int main()
{
	struct Vector2
	{
		float x, y;
	};

	std::cout << "Make Shared\n";
	{
		std::array < std::shared_ptr<Vector2>, 1000> sharedPtrs;
		Timer timer;  // Not counting the time to create the array
		for (int i = 0; i < sharedPtrs.size(); i++)
			sharedPtrs[i] = std::make_shared<Vector2>();
	}
	std::cout << "New Shared\n";
	{
		std::array < std::shared_ptr<Vector2>, 1000> sharedPtrs;
		Timer timer;
		for (int i = 0; i < sharedPtrs.size(); i++)
			sharedPtrs[i] = std::shared_ptr<Vector2>(new Vector2());
	}
	std::cout << "Make Unique\n";
	{
		std::array < std::unique_ptr<Vector2>, 1000> sharedPtrs;
		Timer timer;
		for (int i = 0; i < sharedPtrs.size(); i++)
			sharedPtrs[i] = std::make_unique<Vector2>();
	}
	__debugbreak();
}
```

Measuring the performance comparison of `shared_ptr` and `unique_ptr` twice:

![](./storage%20bag/Pasted%20image%2020230731163728.png)

![](./storage%20bag/Pasted%20image%2020230731163913.png)

As expected, `unique_ptr` takes less time than `shared_ptr`, but the time difference between `make_shared` and `new` is minimal. An important thing to note is that we are actually analyzing in Debug mode, which has many additional safety measures that take time and are not ideal for measuring performance.

Switching to Release mode, we can see that `make_shared` is significantly faster than `new`:

![](./storage%20bag/Pasted%20image%2020230731164128.png)

Therefore, it's crucial to ensure that the code you're analyzing is meaningful in Release mode, as you won't be releasing code in Debug mode.