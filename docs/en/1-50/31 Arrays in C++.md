Arrays require prior knowledge of [16 POINTERS in C++](16%20POINTERS%20in%20C++.md).

## 1. What is an Array

An array is a collection of elements, a set of things arranged in a specific order. In our example, an array is essentially used to represent a collection of variables, typically of the same type.

Arrays are very important and useful because there are many scenarios where we want to represent a whole collection of data. Creating a large number of variables doesn't make sense; these data should be placed in a *data set*.

Since variables need to be created manually, we have to set variables in the code and give them a variable name. Suppose we want to store 50 integers representing some kind of data; we definitely don't want to specify fifty manually, which is terrifying and unmaintainable: we would have to write 50 lines of code to set them to 0 manually. In this scenario, we need to use an array to contain all these 50 elements of the same type at the same time, which is much easier.

Remember that an array is like having many variables in one variable.

```cpp
int main()
{
	int example[5];  // Allocates enough memory to store five integers
	example[0] = 2;
	example[4] = 4;

	std::cout << example[0] << std::endl;   // 2
	std::cout << example << std::endl;      // 0064FC30 (memory address), because it is actually a pointer

	std::cin.get();
}
```

### Memory Access Violation

_Memory access violation_

```cpp
	int example[5];  // Allocates enough memory to store five integers

	example[-1] = 5;
	example[5] = 2;
```

In *Debug* mode, you will get a program crash error to help you debug these issues. In *Release* mode, you might not receive an error, meaning you have modified memory that does not belong to you. Be very careful with this issue and always ensure that you operate within the bounds of the array. If not, it will produce hard-to-debug problems because you are modifying memory that does not belong to this array, but this memory is part of other variables in the code, meaning you are unconsciously modifying other variables in the code.

## 2. For Loops

*Array* is always accompanied by [For loops](<14%20Loops%20in%20C++(for,while%20loops).md#^ebdf13>), because for loops can traverse using indices within a specific range. So if we want to set each value in the array, a good way is to implement it through a for loop.

```cpp
	for( int i=0;i<5;i++)  // i<=4 has performance issues because you are doing less than and equal comparisons
	{
		example[i] = 2;
		std::cout << example[i] << std::endl;
	}
```

An important point about arrays is that the data in the array is contiguous, meaning the data is placed in a row. Memory allocation: each *integer* is 4 bytes, so here we get a row of 20 bytes of memory divided into several 4 bytes (not literally divided).

![](./storage%20bag/Pasted%20image%2020230704230608.png)

*index* index is actually an address offset, offset = index x size of each element. For example, the address offset of example\[2] is 2 x _sizeof_(int) = 8 bytes.

Here it is an integer pointer pointing to a memory block containing 5 integers.

```cpp
int example[5];  // Allocates enough memory to store five integers
	int* ptr = example;

	for (int i = 0; i < 5; i++)
	{
		example[i] = 2;
		std::cout << example[i] << std::endl;
	}

	example[2] = 5;  // Can be rewritten with pointers, as in the next line
	*(ptr + 2) = 6;

```

![](./storage%20bag/Pasted%20image%2020230704231247.png)

> The above says the offset is 8 bytes, but when dealing with pointers, just adding a value like 2 to the pointer, it will calculate the actual number of bytes based on the data type, as calculated above.

```cpp
int main()
{
	int example[5];   // Created on the stack, destroyed when out of scope
	for (int i=0;i<5;i++)
	{
		example[i] = 2;
	}
	int* another = new int[5]; // Created on the heap, will survive until we actively destroy it or the program ends
	for (int i=0;i<5;i++)
	{
		another[i] = 2;
	}
	delete[] another;

	std::cin.get();
}
```

If you have a function that returns a newly created array, then you must use *new* to allocate, unless the parameter you pass in is a memory address.

Another thing to consider is *memory indirection*, meaning we have a pointer, and the pointer points to another memory block that holds our actual array, which can cause some memory fragmentation and cache loss.

#### On the Stack

```cpp
class Entity
{
public:
	int example[5];   // Created on the stack, destroyed when out of scope

	Entity()
	{
		for (int i = 0; i < 5; i++)
			example[i] = 2;
	}
};
```

![](./storage%20bag/Pasted%20image%2020230704232816.png)

#### On the Heap

```cpp
class Entity
{
public:
	int* example = new int[5];   // Created on the heap

	Entity()
	{
		for (int i = 0; i < 5; i++)
			example[i] = 2;
	}
};
```

![](./storage%20bag/Pasted%20image%2020230704233052.png)

Here, in the memory view, enter `&e`, we see another memory address, which is actually a pointer. Due to *endian* (byte order), we need to reverse.

![](./storage%20bag/Pasted%20image%2020230704233253.png)

> That is, `p -> p -> array`

## 3. C++ 11 std::array

This is a built-in data structure defined in the C++11 standard library, which many people use to replace native arrays because of its many advantages. For example, boundary checking, recording the size of the array.

### 1. Native Arrays

We actually cannot calculate the size of a native array, but when deleting this array, the compiler needs to know how much memory we need to release. However, it is troublesome and cannot be trusted; never access the size of the array in array memory.

```cpp
int a[5];
std::cout << sizeof(a) << std::endl;  // 20: size of the array
int count = sizeof(a) / sizeof(int);
std::cout << count << std::endl;      // 5: number of elements
```

If you do `sizeof(example)`, it will return the size of the integer pointer (4), so you can only use this trick on stack-allocated arrays.

![](./storage%20bag/Pasted%20image%2020230704234722.png)

Changing back to `int example[5];` can also work, but you really can't trust this method.

#### A Key Point

When you apply for memory for an array on the stack, it must be a constant that needs to be known at compile time (there will be other methods to solve this later).

![](./storage%20bag/Pasted%20image%2020230704234937.png)

```cpp
static const int size = 5;
int example[size];

// Or constant expression constexpr
// The constant expression in the class must be static
```

Like below, you can get the size of the array.

```cpp
	static const int exampleSize = 5;
	int example[exampleSize];

	Entity()
	{
		for (int i = 0; i < exampleSize; i++)
			example[i] = 2;
	}

int main()
{
	std::cout << sizeof(Entity) << std::endl;  // 20
}

```

### 2. std::array

```cpp
class Entity
{
public:
	static const int exampleSize = 5;
	int example[exampleSize];

	std::array<int, 5> another;  // std::array

	Entity()
	{
		for (int i = 0; i < another.size(); i++)
			example[i] = 2;
			}
};

```

There will be additional overhead because if you want, it will do boundary checking, and it actually maintains an integer size. These additional overheads are usually worth it. Usually, native arrays are used, which are faster. If you want to be very safe, you can use std::array.