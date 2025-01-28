When you write C++ code, you need to be concerned with memory, performance, and optimization issues, otherwise, it might be better to use another language.

The size of memory allocated is determined by the type you write, in bytes.

For example, `new int` will request the allocation of 4 bytes of memory.
Now, we need to find a contiguous block of memory that contains 4 bytes. Although it is easy to find and can be allocated quickly, it still needs to find a 4-byte memory address in a row of memory. Once found, it will return a pointer to that memory address, allowing you to start using your data, whether for storage, access, reading, or writing.

When allocating memory, it doesn't scan memory continuously like a laser; instead, there is something called a *free list* that maintains addresses with free bytes.

```cpp
int a = 2;
int* b = new int;
```

In addition to creating an integer as usual, we can also choose *dynamic memory allocation* by using the *new* keyword on the *heap*.

```cpp
int* b = new int[50]; // 200 bytes
Entity* e = new Entity();
```

This is the basic usage of the *new* keyword.
Here, it not only allocates space but also calls the constructor.

To see the definition of `new`:
```C
void* __CRTDECL operator new(
    size_t _Size
);
```
It is actually just a function, where `_Size` is the size of memory it allocates, and it returns a void pointer.
You can review [16 POINTERS in C++](16%20POINTERS%20in%20C++.md).

Typically, calling the *new* keyword invokes the underlying C function *malloc*, which is used to allocate memory.
The actual function of `malloc()` is to take a `size`, which is the number of bytes we need, and then return a `void pointer`.
```cpp
malloc(50);
```
This is what the function does, so our code here is equivalent to:
```cpp
// (1) Entity* e = new Entity();
Entity* e = (Entity*)malloc(sizeof(Entity)); // (2)
```
The only difference between these two lines of code is that (1) calls the constructor of Entity. While (2) merely allocates memory and returns a pointer to that memory without calling the constructor. In C++, you shouldn't allocate memory like (2), although in some cases you might want to do so, but we'll discuss that later.

`delete` is also known as a *destructor*, see [26 Destructors in C++](26%20Destructors%20in%20C++.md).

`delete` is also an operator, which is just a regular function that calls the C function `free()`. *free* can release the memory requested by *malloc*.
```cpp
delete e;
free(e);
```

This is important because when we use the *new* keyword, the memory is not released, not marked as *free*, and it will not be returned to the *free list*. Therefore, when we call *new* again, this memory cannot be allocated again until we call `delete`. We must manually release it.

#### Notes

1. If we use `new[]`, we should also use `delete[]`, because that's how the operator is defined.
```cpp
int* b = new int[50];

delete[] b;
```

2. new supports a usage called *placement new*, which determines where its memory comes from.
```cpp
int* b = new int[50];
Entity* e = new(b) Entity();
```
We'll discuss the details later, but here we just show its syntax.

This constructs the `Entity` object on the already allocated memory address `b`, instead of using the default memory allocator. This allows creating an object at a specified memory location. This line of code constructs an `Entity` object at the memory location pointed to by the `b` pointer and returns a pointer to that object, assigning it to the `e` pointer.