#include <iostream>
#include <memory>
#include <string>

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