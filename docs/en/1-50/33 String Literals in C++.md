# String Literals

![](./storage%20bag/Pasted%20image%2020230705140428.png)

Why is the size 7? Because there is an additional [null terminator](<32%20How%20Strings%20Work%20in%20C++%20(and%20how%20to%20use%20them).md#^26e746>) `00`: `"Cherno\0"`

![](./storage%20bag/Pasted%20image%2020230705140940.png)
The two `.` represent the position of `00`

![](./storage%20bag/Pasted%20image%2020230705141715.png)

This string is stored in the const section of the binary file.
Opening it with a hex editor, you can see "Cherno" in the binary file. These characters are embedded in the binary file. When we reference it, it actually points to a constant data block that is not allowed to be edited.
![](./storage%20bag/Pasted%20image%2020230705142330.png)

```cpp
const char* name = "Cherno"
name[2] = 'a';
```

Running the program in Release mode to modify the string will not change it. However, in Debug mode, an exception will be thrown.

### Wide Char

```cpp
const char* name = u8"Cherno";
const wchar_t* name2 = L"Cherno";  // L indicates that the following string literal is composed of wide characters
								   // 2 bytes

// Introduced in C++11
const char16_t* name3 = u"Cherno";   // 16 bits = 2 bytes
const char32_t* name4 = U"Cherno";   // 32 bits = 4 bytes
```

#### Difference between wchar_t and char16_t?

Although we often say that wchar is 2 bytes per character, it is actually determined by the compiler. (Windows: 2 bytes, Linux: 4 bytes).
If you want it to always be 2 bytes, you can use `char16_t`.

### R Method

Adding `R` before a string means ignoring escape characters, where `R` stands for *raw*.

![](./storage%20bag/Pasted%20image%2020230705144029.png)

String literals are always stored in read-only memory.