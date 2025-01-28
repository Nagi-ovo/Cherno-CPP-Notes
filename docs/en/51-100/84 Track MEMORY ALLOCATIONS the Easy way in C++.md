Memory is crucial, and computers are closely tied to memory. If you only have a CPU without RAM or memory, you can't do anything. Nowadays, memory issues are not as severe as they were 20 years ago, as our computers come with 8, 16, or 32GB of memory.

Writing a C++ program is challenging; it uses a lot of memory. Therefore, it's useful to understand when your program allocates memory, especially heap memory. If you know where your program allocates memory, you can potentially reduce it, thereby optimizing your program and making it run faster. Allocating memory on the heap is not the best practice, especially in performance-critical code. Additionally, being able to see where memory is allocated can help you understand more about how your program works, even if all the running code is written by you. This section will discuss how to accurately see where each allocation comes from and how to track the overall memory usage within an application. The demonstrated techniques can be easily integrated into your existing application without relying on any other tools.

## 1. Overloading the `new` Operator

```cpp
void* operator new(size_t size)
{
	std::cout << "Allocating " << size << " bytes\n";
	return malloc(size);
} // breakpoint

struct Object
{
	int x, y, z;
};

int main()
{
	Object* obj = new Object;
	std::unique_ptr<Object> obj2 = std::make_unique<Object>();
}
```

![](./storage%20bag/Pasted%20image%2020230806145419.png)

> It is observed that both direct heap allocation instantiation and `unique_ptr` allocate objects on the heap by calling `new`.

You can see how useful it is to insert a breakpoint in the `new` function to precisely track the source of memory allocation.

## 2. Overloading the `delete` Operator

```cpp
#include <iostream>
#include <memory>
#include <string>

void* operator new(size_t size)
{
	std::cout << "Allocating " << size << " bytes\n";
	return malloc(size);
}

void operator delete(void* memory, size_t size)
{
	std::cout << "Freeing " << size << " bytes\n";
	free(memory);
}
struct Object
{
	int x, y, z;
};

int main()
{
	{
		std::unique_ptr<Object> obj2 = std::make_unique<Object>();
	}
	std::string string = "Cherno";
}
```

![](./storage%20bag/Pasted%20image%2020230806153409.png)

Now, using these two functions, we can create a memory allocation tracker. We can maintain *allocation metrics* to know exactly how much memory is being used, allocated, and freed. This is very useful.

```cpp
struct AllocationMetrics
{
	uint32_t TotalAllocated = 0;
	uint32_t TotalFreed = 0;

	uint32_t CurrentUsage() { return TotalAllocated - TotalFreed; }
};

static AllocationMetrics s_allocation_metrics;

void* operator new(size_t size)
{
	s_allocation_metrics.TotalAllocated += size;
	return malloc(size);
}

void operator delete(void* memory, size_t size)
{
	s_allocation_metrics.TotalFreed += size;
	free(memory);
}

struct Object
{
	int x, y, z;
};

static void PrintMemoryUsage()
{
	std::cout << "Memory Usage: " << s_allocation_metrics.CurrentUsage() << " bytes\n";
}

int main()
{
	PrintMemoryUsage();
	std::string string = "Cherno";
	PrintMemoryUsage();
	{
		std::unique_ptr<Object> obj2 = std::make_unique<Object>();
		PrintMemoryUsage();
	}
	PrintMemoryUsage();
}
```

![](./storage%20bag/Pasted%20image%2020230806154247.png)

Of course, you can also use built-in memory allocation tracking tools in Visual Studio or ready-made tools like Valgrind. However, this section provides a quick and simple method to see what's happening in your code and track it.