内存是很重要的，计算机和内存是紧密相联的，如果你只有一个 CPU 而没有 RAM 没有内存，那么你什么都做不了。现在内存问题不像 20 年前那么严重了，我们的电脑有了 8、16、32G 的内存。

而写一个 C++程序是比较难的，它会用到大量内存，所以了解你的程序什么时候分配内存，特别是堆内存是很有用的。如果你知道程序在哪里分配内存，你就有可能减少它，从而能优化你的程序并使其运行得更快，因为在堆上分配内存并不是最好的做法，尤其是在性能关键的代码中，除此之外，能够看到内存被分配到哪里，还可以帮助你更多地了解程序是如何工作的，即使所有正在运行的代码都是你写的，本节将讨论如何准确地看到每个分配从何而来，以及如何跟踪应用程序内内存的整体使用情况，只需编写代码而不依赖任何其它工具，所展示的东西都可以很容易地插入到你现有的应用程序中。

## 1. 重载 new 操作符

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

> 查看发现直接堆分配实例化和 unique_ptr 都会通过调用 new 在堆上分配对象。

可以看到，这样在 new 函数中插入一个断点来精确追踪内存分配的来源有多有用。

## 2. 重载 delete 操作符

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

现在使用这两个函数，我们可以创建内存分配跟踪器，我们可以维护一个*allocation metrics* ，可以确切地知道有多少内存被使用，有多少内存被分配，有多少内存被释放等，这是非常有用的。

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

当然你也可以使用 VS 内置的内存分配跟踪分析工具，还有 Valgrind 等一些很好的现成的工具，但本节只是一个快速简单的方法，可以看到你的代码中发生了什么并跟踪它
