# Learning Notes on Cherno's C++ Tutorial: Optimizing String Operations

When dealing with strings, many people are unaware of the impact strings can have on program performance, especially since string operations are frequently used in programs. There is a very simple thing we can do to make our strings and string operations faster.

## 1. Memory Allocation in `std::string`

One of the main issues with `std::string` is string formatting and string operations, as they require memory allocation. Allocating memory on the heap is unavoidable, but it should be minimized because it slows down the program, and `std::string` and many of its functions tend to allocate memory.

```cpp
static uint32_t s_AllocCount = 0;

// We can track memory allocations by overloading the new operator
void* operator new(size_t size)
{
	s_AllocCount++;
	std::cout << "Allocating " << size << " bytes\n";
	return malloc(size);
}

void PrintName(const std::string& name)
{
	std::cout << name << std::endl;
}

int main()
{
	std::string name = "Yan Chernikov";
	PrintName(name);

	std::cout << s_AllocCount << " allocations" << std::endl;
	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230803230516.png)

By setting a breakpoint at the memory allocation point, we can see that the heap allocation occurs when the string is created.

![](./storage%20bag/屏幕截图%202023-08-03%20230727.jpg)

What if we remove this string and just pass a `const char` array directly to the `PrintName` function? Will it still allocate memory?

```cpp
//std::string name = "Yan Chernikov";
PrintName("Yan Chernikov");
```

The result is that it still allocates memory because, although the function accepts a `const` reference, it still needs to construct a `std::string`, which requires memory allocation.

Now let's make it a bit more complex:

```cpp
std::string name = "Yan Chernikov";

std::string firstName = name.substr(0, 3);

std::string lastName = name.substr(4, 9);
PrintName(firstName);
```

![](./storage%20bag/Pasted%20image%2020230803231541.png)

Even such simple operations result in three allocations. Imagine this happening frequently in your program. If you have a real-time application, like a game, and you do this every frame, it will accumulate and negatively impact your frame rate.

How can we make this better?

There is a simple way to modify the existing code to reduce the allocations to just one. By the end of this section, we will eliminate all allocations, meaning there will be zero allocations.

First, let's look at the code and think about what you are trying to achieve. Often, this will give you a direction for optimization. What you really need here is a view of the string, not the creation of multiple new strings by copying data.

This is where `std::string_view` comes into play:

## 2. `std::string_view`

`std::string_view` is a new class introduced in C++17. It is essentially just a pointer to existing memory, in other words, a `const char` pointer pointing to an existing string owned by someone else, along with a *size*.

It works by creating a window into existing memory, providing a small view of it, rather than allocating a new string. This means there is no memory allocation, and passing a `string_view` by value is very lightweight since it is just a pointer and a size.

Let's rewrite the previous `substr` example using `string_view`:

```cpp
void PrintName(std::string_view name) // No need to pass by reference, change the type to string_view
{
	std::cout << name << std::endl;
}

int main()
{
	std::string name = "Yan Chernikov";

#if 0
	std::string firstName = name.substr(0, 3);

	std::string lastName = name.substr(4, 9);
#else
	std::string_view firstName(name.c_str(), 3);
	std::string_view lastName(name.c_str()+4, 9);
#endif

	PrintName(firstName);

	std::cout << s_AllocCount << " allocations" << std::endl;
	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230803233514.png)

Now there is only one allocation, but in fact, we can eliminate all allocations by not using `std::string` at all:
![](./storage%20bag/Pasted%20image%2020230803233742.png)

> Since this is just a static string, there is no need to use `std::string`, so we can do it this way.

If the string comes from a file or is generated in some other way, it might be more realistic to keep it as a `std::string` in that case.