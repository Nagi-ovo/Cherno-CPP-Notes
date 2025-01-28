## 1. Type System

_Type punning_ is just a fancy term for bypassing the type system in C++. C++ is a strongly typed language, meaning it has a type system. Unlike JavaScript, where you don't need to declare the type of a variable when creating it, in C++ you must declare the type of the variable, such as integer, double, struct, etc. However, this type system is not as "enforced" as in Java. In C++, while types are enforced by the compiler, you can directly access memory, making it easy to bypass the type system. Whether or not you should do this depends on your specific needs. In some cases, you absolutely should not circumvent the type system because it exists for a reason. Unless you have a good reason, you wouldn't want to use it excessively. ^4d9dfe

Suppose I have a simple class, and now I want to write it as a byte stream. I can reinterpret its entire structure as a byte array and then output it as a byte stream. This is very useful in many cases. This is a primitive, low-level access, which is why C++ is efficient and applications perform well.

```cpp
#include <iostream>

int main()
{
	int a = 50;
	double value = a;

	std::cout << value << std::endl;


	std::cin.get();
}
```

Viewing `a` in memory:
![](./storage%20bag/Pasted%20image%2020230725135448.png)

Viewing `value` in memory:
![](./storage%20bag/Pasted%20image%2020230725135529.png)

This example shows an implicit conversion. For an explicit conversion, you just need to change it to: ^f3904d

```cpp
double value = (double)a;
```

So, how do we take the memory of `a` and treat this address as a `double`?

```cpp
double value = *(double*)&a; // Primitive method: take the address of a, which becomes an int pointer, then cast it to a double pointer and dereference it.
```

![](./storage%20bag/Pasted%20image%2020230725140104.png)

Viewing the address of `value`, since `double` is 8 bytes, the remaining part is uninitialized memory.
![](./storage%20bag/Pasted%20image%2020230725140241.png)

The reason this happens is that we did a poor job with the type conversion above because they are of different sizes. We took a 4-byte `int` and treated it as a `double`. What we did here was first cast an `int` pointer to a `double` pointer, then dereferenced it. It actually continued for 4 more bytes after our `int` and grabbed that part of memory, which is not the memory we used to store `a`. This is bad and can even cause crashes in some cases. What this means is that we have copied the memory to a new `double` block, and the operation is safe, but reading memory that doesn't belong to us is not good.

If you don't want to create a new variable and just want to access this `int` as a `double`, you just need to add an `&` after `double`, referencing it without copying. This way, you can edit the memory of the `int`, which is dangerous because a `double` requires 8 bytes, and we only have 4 bytes of space, which could cause the program to crash.

## 1. Struct Type Conversion

```cpp
struct Entity
{
	int x, y;
};

int main()
{
	Entity e = { 5,8 };
	std::cin.get();
}
```

In memory, this struct is simply composed of 2 `int`s, which are the integers `x` and `y`.

![](./storage%20bag/Pasted%20image%2020230725142838.png)
The struct itself does not contain any padding or any type of data. If it were an empty struct, it would be at least 1 byte because we need to address this memory. But if the struct contains variables, like these `int x` and `y`, then it only contains these two integers. Therefore, we can treat the `Entity` struct as an `int` array and access these integers without using `e.x` or `e.y`.

```cpp
int* position = (int*)&e;
std::cout << position[0] << "," << position[1] << std::endl;
```

Since we cast it to an array, we can access it like an array.
![](./storage%20bag/Pasted%20image%2020230725143621.png)

Similarly, a more crazy operation:
![](./storage%20bag/Pasted%20image%2020230725144039.png)
You can see that one of the important reasons why C++ is a powerful language is that it can freely manipulate memory.