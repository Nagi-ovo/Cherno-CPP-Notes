# Raw Pointer vs Smart Pointer

Perhaps the most important aspect in programming is *memory*. Everything we do in our code involves reading from or writing to memory.

## 1. What is a Pointer?

A pointer is an *integer*, a whole number that stores a memory address.

#### Visualization

Think of the computer's memory as a long street with a row of houses, each with a house number and address.

Now, imagine each house with an address as a *byte*, a single byte of data. We need a way to address all these bytes. Suppose someone orders something online and wants it delivered to their house, or someone sends something out from their house. In any case, you need to be able to *read and write* from those bytes in memory, those houses.

The pointer is that address, telling us where the house is—where that specific byte of memory is located.

So, a pointer is an address, an integer that stores a **memory address**.

*Types* are completely meaningless; all types of pointers are integers that store a memory address. The purest pointer, `void`, has no type. We define types for pointers to indicate that the data at that address is of the type we assign, making our lives syntactically easier. However, the type does not change the pointer; it's just an integer.

```cpp
void* ptr = 0;   // Address 0 is meaningless; the pointer is in an invalid state and cannot be accessed.
void* ptr = NULL;  // (#define NULL 0)
void* prt = nullptr; // Introduced in C++11
```

^646396

## 2. Using Pointers

`135fd6c` is the location in memory where this integer variable is stored.

![](./storage%20bag/Pasted%20image%2020230701112242.png)

> You can view this in Visual Studio's memory window: [See how](11%20How%20to%20DEBUG%20C++%20in%20Visual%20Studio.md#^dd3537)

![](./storage%20bag/Pasted%20image%2020230701113120.png)

> You can see that the value `8` is stored at this address.

Changing the pointer type still allows you to find the memory; the type has no effect.

![](./storage%20bag/微信图片_20230701113713.png)

## 3. Accessing and Modifying

I know where the data is; how do I access it?

#### _Dereferencing_:

By adding an *asterisk* (\*) before the pointer, `*ptr` actually dereferences the pointer, meaning you are now accessing the data at that location, and you can read or write to that data.

```cpp
int var = 8;
void* ptr = var; 
*ptr = 10;  // This will cause an error; how can the computer write a value to a void pointer?
```

Because it doesn't know what `10` is—is it a *short* (a 2-byte integer), an *int* (a 4-byte integer), or a *long long* (an 8-byte integer)?

This is where the importance of *type* comes in.

```cpp
int var = 8;
int* ptr = &var;
*ptr = 10;
```

![](./storage%20bag/Pasted%20image%2020230701175252.png)

#### memset

Allocates memory, accepts a pointer, data, and size.
![](./storage%20bag/Pasted%20image%2020230701175816.png)

Since we used the *new* keyword, this data is allocated on the *heap*, so we need to delete it after we're done:

```cpp
	char* buffer = new char[8];
	memset(buffer, 0, 8); // Used to set the value of a block of memory. Here, it sets all bytes in the buffer to 0, effectively clearing it.

	delete[] buffer;  // Delete the data
```

#### Pointer to Pointer

![](./storage%20bag/Pasted%20image%2020230701180553.png)
We know this pointer will be 4 bytes because we're running a 32-bit program (in a 32-bit program, a memory address is 32 bits).
Here, it's important to note the byte order:

##### Little Endian

The computer's *endianness is in reverse order* (the byte order is reversed), meaning the least significant byte matches the lowest address, and the most significant byte matches the highest address.
Thus, the address in the image is actually: ==00963408==
![](./storage%20bag/Pasted%20image%2020230701181043.png)

In conclusion, *pointers* are not mysterious magic, nor are they difficult. Once you understand their *gist*, the path ahead will naturally open up to you.