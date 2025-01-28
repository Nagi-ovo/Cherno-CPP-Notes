# Comparison of Heap and Stack Memory

When our program starts, it is divided into several different memory regions. Besides the heap and stack, there are many other things, but these two are our primary focus: the stack and the heap.

## 1. What are the Stack and Heap?

After the application starts, what the operating system does is load the entire program into memory and allocate a large amount of physical RAM (_Random Access Memory_) so that our actual application can run.
The stack and the heap are two regions that actually exist in RAM:
The *stack* is usually a predefined size of memory, typically around 2 megabytes (2MB);
The *heap* is also a region with a predefined default size, but it can grow and change as the application progresses.
It is important to know that the actual physical locations of these two memory regions are in RAM. Many people tend to think that the stack is stored in the CPU cache or similar locations. It is indeed active in the cache because we keep accessing it, but not all stack memory is stored there. This is not how it works. Just remember that the actual locations of these two memory regions are in our memory, which is why there are two different regions in memory.

## 2. Differences Between the Stack and the Heap

In our program, memory is used to store the data needed to run the program, whether it is from local variables or things read from files. The stack and the heap are places where we can store data.
They work very differently, but essentially do the same thing: we can ask C++ to give us some memory from the stack or the heap, and if all goes well, it will give us a block of memory of the requested size. The difference lies in **how it allocates memory**.

Define an `int`, `array`, and `struct` on the stack and heap respectively:

```cpp
int value = 5;
int array[5];
Vector3 vector;

// We need the new keyword to allocate on the heap

int* hvalue = new int ;
*hvalue = 5;
int* harray = new int[5];
Vector3* hvector = new Vector3(); // Parentheses are optional
new int[5];

```

The main difference is that we need the `new` keyword to allocate memory on the heap.

Now let's check the memory window:

```cpp
struct Vector3
{
	float x, y, z;

	Vector3()
		: x(10), y(11), z(12) {}
};

int main()
{
	int value = 5;  // Set a breakpoint
	int array[5];
	Vector3 vector;
	array[0] = 1;
	array[1] = 2;
	array[2] = 3;
	array[3] = 4;
	array[4] = 5;

	int* hvalue = new int ;
	*hvalue = 5;
	int* harray = new int[5];
	Vector3* hvector = new Vector3();
	harray[0] = 1;
	harray[1] = 2;
	harray[2] = 3;
	harray[3] = 4;
	harray[4] = 5;

	LOG(value);
	LOG(*hvalue);
	std::cin.get();
}
```

### 2.1 Stack Allocation

In memory, check &value as shown in the figure: cccc in debug mode indicates that we have not initialized this value yet.
![](./storage%20bag/Pasted%20image%2020230715194440.png)

You can find that the memory of value follows the memory of the array. There are some bytes between them because in debug mode, *safety guards* are added around variables to ensure that we do not overflow all variables and access them in the wrong memory, etc.

![](./storage%20bag/屏幕截图%202023-07-15%20194754.jpg)

Check &vector:
![](./storage%20bag/屏幕截图%202023-07-15%20195243.jpg)

So the storage locations of these variables in memory are very close because what actually happens is: when we allocate variables on the stack, the pointer at the top of the stack moves by the size of this variable. Allocating a 4-byte integer moves the stack pointer by 4 bytes.

Memory is actually stored like a stack, one on top of the other. In most stack implementations, the stack grows downward. This is why you will see in the figure: the first int value is stored at a higher memory address, and the subsequent array and vector are stored at lower memory addresses next to it because it grows downward.

The stack's approach is to stack things on top of each other, which is why *stack allocation* is very fast. It is like a single CPU instruction; all we do is move the stack pointer and then return the address of the stack pointer. If I want to allocate an integer, I move the stack pointer backward by 4 bytes and then return that memory address because it is the start of the 4-byte block.

### 2.2 Heap Allocation

^77312c

The visibility here is poor because the allocated memory is not contiguous:
![](./storage%20bag/Pasted%20image%2020230715200619.png)

You can see that the addresses of hvalue and harray are far apart.

![](./storage%20bag/Pasted%20image%2020230715200734.png)

After allocating with `new` in the heap, you need to call the `delete` keyword to free the memory. Using [smart pointers](44%20SMART%20POINTERS%20in%20C++.md) with `make` will also help you call the keyword, so we need to manually free the memory.

```cpp
delete hvalue;
delete[] harray;
delete hvector;
```

When allocating memory on the stack, once the scope ends, all the memory you allocated on the stack is popped, and the memory is freed.
This scope can be any form, such as a function scope like the main function, or just an empty scope, or even for, while loops, or any scope statement:

```cpp
int main()
{
	{
		int value = 5;
		int array[5];
		array[0] = 1;
		array[1] = 2;
		array[2] = 3;
		array[3] = 4;
		array[4] = 5;
		Vector3 vector;
	}
}
```

When this scope ends, everything allocated on the stack within this scope is popped, freed, and recycled because the stack moves back to its original position (the position before we entered this scope).
This is also one of the important differences between the stack and the heap. Freeing memory has no overhead because freeing memory on the stack is the same as allocating it. We don't need to move the stack pointer backward and return the stack pointer address; we just pop things off the stack, and the stack pointer naturally returns to its position before the scope started. (A single CPU delete instruction can free everything.)

## 3. What the `new` Keyword Actually Does

For details, see [39 The NEW Keyword in C++](39%20The%20NEW%20Keyword%20in%20C++.md)

The `new` keyword actually calls a function called `malloc` (short for memory allocate), which usually calls a specific function of the underlying operating system or platform, which will allocate memory for you on the heap. When you start the application, you are allocated a certain amount of physical RAM, and your program maintains something called a *free list*, which keeps track of which memory blocks are free and stores their locations. When you request heap memory using `malloc`, it can browse the free list, find a memory block that meets the size requirements, and then return a pointer to it, recording the allocated size and whether it is now allocated (so you can't use this memory block).

The key point here is that allocating memory on the heap is a big deal, while allocating memory on the stack is like a single CPU instruction. The difference between these two main types of memory is the way they are allocated. You can see from the assembly instructions that declaring a variable on the stack is just one or two lines of instructions, while heap allocation is a large block of instructions, followed by calling `delete`, which is another large block of instructions.

So in fact, if possible, you should **try to allocate memory on the stack**. The only reason to allocate on the heap is if you can't allocate on the stack, such as when you need its lifetime to be longer than the scope you are dealing with, or you specifically need more data, like loading a 50MB texture, which is not suitable for stack allocation, so you have to allocate it on the heap.

The performance difference is due to the allocation method. So theoretically, if you pre-allocate a block of memory on the heap before running your program and then perform heap allocations from this pre-allocated block, stack and heap allocations are basically the same. The only thing you might have to deal with is *CPU cache misses*, but the number of misses may not be enough to cause trouble. So when you call `new`, you need to check the free list, request memory, and record everything, which is where the heap is slower compared to the stack. The actual access (CPU, cache) is usually negligible.