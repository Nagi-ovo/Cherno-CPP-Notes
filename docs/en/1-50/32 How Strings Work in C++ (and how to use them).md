# Notes on Cherno's C++ Tutorial: Strings

Requires prior knowledge of *pointers* and *arrays* because you'll find that strings and arrays are closely related.

First, what is a string? Essentially, a string is a sequence of *characters*. Characters refer to letters, numbers, symbols, and essentially anything that represents text. For us, it’s necessary to represent the shape and format of text on a computer in some way.

A single character, an entire paragraph, a word, a bunch of words... all of these are referred to as strings, or a _string of text_.

In C++, there is a numeric type called *char*, which is short for *character*. It occupies 1 byte of memory. It’s useful because it allows you to convert pointers to `char` pointers, enabling pointer arithmetic based on bytes. It’s also useful for allocating memory buffers. If you want to allocate 1KB of memory, you can simply allocate 1024 `char`s.

It’s also useful for strings and text because the default way C++ handles characters is through *ASCII* characters. Characters can also be larger than one byte (e.g., Chinese, Japanese), and can be 2-4 bytes in size.

If we only use 1 byte to represent a character, 1 byte = 8 bits, which means we have $2^8=256$ possibilities. Clearly, this isn’t enough to accommodate all languages. Therefore, we have *UTF-16*, which is a 16-bit character encoding, giving us $2^{16}=65536$ possibilities.

However, in the base C++ language without any libraries, using only primitive data types, *char* is 1 byte.

## 1. const\* char

Rule of thumb: If you don’t use the *new* keyword, don’t use *delete*.

```cpp
const char* name = "Cherno";  // C-style string definition
name[2] = 'a';  // Won't work. If you know you won’t modify the string, use const; otherwise, remove it.
```

Starting from C++11, assigning string literals directly to non-`const` `char*` pointers is considered unsafe behavior. Therefore, use:

```cpp
char name[] = "Cherno";
```

![](./storage%20bag/Pasted%20image%2020230705122342.png)

The `00` character in the image is called *the null termination character*. This lets us know where the string ends and makes it easier to determine the size of the string ^26e746.

```cpp
char name2[6] = { 'C','h','e','r','n','o' };
std::cout << name2 << std::endl;   // Cherno烫烫烫烫烫......
```

![](./storage%20bag/Pasted%20image%2020230705123511.png)

An *array guard* was allocated, but there’s no null termination character, so `cout` doesn’t know where to stop printing.

```cpp
char name2[7] = { 'C','h','e','r','n','o','\0'}; // You can also write it as 0 directly.
```

![](./storage%20bag/Pasted%20image%2020230705123808.png)
Normal output.

## 2. std::string

`std::string` has a constructor that accepts a `char` pointer or a `const char` pointer.
![](./storage%20bag/Pasted%20image%2020230705124249.png)
It also has many built-in methods.

```cpp
std::string name = "Cherno";
std::cout << name << std::endl;          // Cherno
std::cout << name.size() << std::endl;   // 6
```

### String Concatenation

```cpp
std::string name = "Cherno" + "hello";  // '+': cannot add two pointers
```

As mentioned earlier, these are `const char` arrays, not actual strings.

```cpp
std::string name = "Cherno";
name += "hello";   // Chernohello
```

Or:

```cpp
std::string name = std::string("Cherno") + "hello!";
```

## 3. Passing Strings to Other Functions

```cpp
void PrintString(const std::string& string) // Pass by reference, not by copy, and ensure it’s not modified.
```