Today's topic is multi-dimensional arrays. It is essential to understand [31 Arrays in C++](31%20Arrays%20in%20C++.md) and [16 POINTERS in C++](16%20POINTERS%20in%20C++.md) because pointers are crucial when dealing with any type of array (since arrays are memory blocks, and the straightforward way to handle memory is by using pointers).

## 1. Differences Between Multi-dimensional Arrays and Regular Arrays

Starting with a two-dimensional array as an example, it is essentially an **array of arrays** (a three-dimensional array would be an array of arrays of arrays, and so on), which is a collection of arrays.

One strategy we consider when dealing with arrays is using pointers. We have a pointer that points to the beginning of the array in memory. Imagine having an array of pointers; eventually, you get a memory block containing contiguous pointers, each pointing to some array in memory. Thus, what you get is a collection of pointers to arrays, which is an array of arrays.

```cpp
#include <iostream>

int main()
{
	int* array = new int[50];

	int** a2d = new int*[50]; // Here we allocate a buffer of pointer objects

	std::cin.get();
}
```
Here, we have only allocated a memory block that can store 200 bytes of pointers, but it is not initialized yet.
We can then iterate and set each pointer to point to an array, resulting in an array containing memory locations of 50 arrays.
```cpp
for (int i = 0; i < 50; i++)
		a2d[i] = new int[50];
```

Three-dimensional array (just for understanding):
```cpp
int*** a3d = new int**[50]; 

for (int i = 0; i < 50; i++)
{
	a3d[i] = new int*[50];
	for (int j = 0; j < 50; j++)
		a3d[i][j] = new int[50];  // Two levels of dereferencing
	//	int** ptr = a3d[i];
	//	ptr[j] = new int[50];
}
a3d[0][0][0] = 0;
```

Back to the two-dimensional array:
```cpp
int** a2d = new int*[50]; // Here we allocate a buffer of pointer objects

for (int i = 0; i < 50; i++)
	a2d[i] = new int[50];

a2d[0][0] = 0;
a2d[0][1] = 0;
a2d[0][2] = 0;
```
It's important to note that the first column is an index of pointers, not integers. What we are actually dealing with is:
```cpp
int** a2d = new int*[50]; // Here we allocate a buffer of pointer objects
```
The second column on the right is where we handle the internal data.

Since this is [heap allocated](54%20Stack%20vs%20Heap%20Memory%20in%20C++.md#^77312c), we need `delete[]` to free the memory. However, be aware that `delete[] a2d` only deletes the array of pointers that store the actual integer arrays. If you delete it, you will cause a memory leak of the 200 bytes of memory space that stores the actual 50 arrays because we can no longer access them. Therefore, we need:
```cpp
for(int i = 0;i < 50;i++)
	delete[] a2d[i];
delete[] a2d;
```

## 2. Cache Misses
```cpp
int** a2d = new int*[5]; // Create a 5x5 two-dimensional array

for (int i = 0; i < 5; i++)
	a2d[i] = new int[5];
```
Handling arrays of arrays in the above manner can lead to *memory fragmentation* issues. We are not storing these 25 integers in a contiguous memory buffer, i.e., in a single row. Instead, we are creating 5 separate buffers, each containing 5 integers. Unless you use some custom allocation method or memory pool allocation, they will be allocated to completely random locations in memory. Therefore, when we finish reading one row and jump to the next row to read the array contents, it will cause a *cache miss*, meaning we waste time fetching data from RAM. In fact, traversing these 25 integers in this way is much slower than if we had allocated a single one-dimensional array (where memory allocation is in a single row). One of the most important things you can optimize when programming and optimizing is your memory access. If you can store the memory you need to access contiguously, you will have more *cache hits* and fewer *cache misses*, making your program faster.

Can you think of a better way to store 25 integers?

You can store them in a one-dimensional array:

```cpp
int* array = new int[5 * 5];
for(int y=0;y<5;y++)
	for(int x=0;x<5;x++)
	{
		array[x + y * 5] = 2;  // Each time y increases by 1, we jump forward by 5 numbers, equivalent to jumping a row in a grid.
	}
```