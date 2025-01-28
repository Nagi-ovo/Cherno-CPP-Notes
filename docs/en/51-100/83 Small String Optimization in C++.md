# Small String Optimization (SSO)

Strings are often associated with poor performance, and this section focuses on how the C++ standard library optimizes small strings.

We all know that creating a standard string can lead to memory allocation, so many people try to minimize the use of strings. However, in the standard library, small strings (i.e., strings that are not very long) do not require heap allocation. Instead, we can allocate a small stack-based buffer rather than heap-allocated memory. If you have a string that does not exceed 15 characters (in VS2019), it will not allocate memory on the heap. In other words, for very small strings, you don't need to use `const char*` or micro-manage and optimize your code.

![](./storage%20bag/Pasted%20image%2020230806012752.png)

> The main function of importance is `assign`, which takes a pointer parameter, i.e., `const char*`, representing our string.

![](./storage%20bag/Pasted%20image%2020230806013023.png)

> Here, there is an `if` statement. If the condition is met, the string is simply moved to this memory buffer, and no allocation occurs. If the condition is not met, `Reallocate` is called, which triggers heap allocation via the `new` operator.

Let's check what `Myres` is:

![](./storage%20bag/Pasted%20image%2020230806013328.png)

> As you can see, it is set to the buffer size minus 1.

![](./storage%20bag/Pasted%20image%2020230806013455.png)

> This buffer size `_BUF_SIZE` is equal to `_Scary_val::_BUF_SIZE`.

![](./storage%20bag/Pasted%20image%2020230806013432.png)

> And it is equal to a `constexpr` (constant expression), which in this case is 16. Subtracting 1 gives us 15.

```cpp
#include <iostream>
#include <string>

void* operator new(size_t size)  // Operator overloading
{
	std::cout << "Allocating " << size << " bytes\n";
	return malloc(size);
}

int main()
{
	std::string name = "Cherno";  // Clearly less than 15 characters
	std::cin.get();
}
```

If you run it with F5, you will notice that it still prints an allocation of 8 bytes. This is actually an issue with VS's string class, which mostly occurs in Debug mode. Therefore, switching to Release mode will show the desired result:

![](./storage%20bag/Pasted%20image%2020230806013905.png)

```cpp
std::string name = "Cherno Small St"; // 15 characters, no allocation
std::string name = "Cherno Small St "; // 16 characters, immediately results in a 32-byte heap allocation
```

![](./storage%20bag/Pasted%20image%2020230806014248.png)

This is an optimization that makes the code more efficient and faster.

So what happens in Debug mode that causes the allocation?

![](./storage%20bag/Pasted%20image%2020230806014815.png)

If the debug level is 0, i.e., in Release mode, only `Fake_allocator` is called, which essentially does nothing:

![](./storage%20bag/Pasted%20image%2020230806014947.png)
> In Debug mode, however, the `proxy_ptr` causes the allocation.