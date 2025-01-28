# Notes on C++ Standard Library's Static Array Handling Class (Non-Growing Arrays)

## 1. Static Arrays

```cpp
std::array<int, 5> data;
data[0] = 2;
data[4] = 1;

// C-style plain array
int dataOld[5];
dataOld[0];
```

```cpp
// Use templates to pass the size to std::array, avoiding explicit calls
template<int T>
void PrintArray(std::array<int,T>& array)
{
	for(int i=0;i<T;i++)
	{
		std::cout << array[i] << std::endl;
	}
}

// Or use iterators
for (std::array<int, data.size()>::iterator it = data.begin();
		it != data.end();it++)
	{
		std::cout << *it << std::endl;
	}
```

## 2. Differences and Similarities Between Static Arrays and Plain Arrays

`std::array` and plain arrays are the same in terms of memory layout, both allocated on the stack, unlike `std::vector` which is allocated on the heap.

However, `std::array` includes boundary checks (only in Debug mode), and under optimal conditions, it performs the same as plain arrays.

`std::array` does not actually store its own size; the size is a template parameter you provide, meaning that calling the size function directly returns 5 instead of returning a size variable stored in memory.

You can see that the boundary check is within a macro, meaning it only occurs at that debug level. If the level is 0, it works the same way as a C-style array.
![](./storage%20bag/Pasted%20image%2020230721005311.png)

You should start choosing `std::array` over C-style arrays because it adds a layer of debugging (when you expect to protect your code), with no performance cost, and it also allows you to record the size of the array.