## 1. Abstract Syntax Tree

The compiler's job is to transform code into *constant data* and *instructions*. After constructing the abstract syntax tree, it begins generating code.

In C++, there is no concept of a "file"; files are merely a way to provide source code to the compiler.

`.cpp` tells the compiler to compile using C++ -> the compiler treats it as a *translation unit* -> resulting in a `.obj` file.

Common [preprocessor](05%20How%20C++%20Works.md#^bafd29) statements are ==pragma statements==.

```cpp
include
define
if
ifdef
```

## Common Preprocessor Statements

### 2.1 \#include

`#include` simply copies the contents of the desired file into the current file. For example, if you create an `EndBrace.h` file with the following content:

```cpp
}
```

Then, my `Multiply` function can still compile correctly even if written like this:

```cpp
int Multiply(int a, int b)
{
	int result = a * b;
	return result;
	#include "EndBrace.h"
```

To inspect the preprocessed file, you can generate a `.i` file by performing the following operation:

![](https://s2.loli.net/2023/06/24/oAysjHlPzxdfbtR.png)

The contents of the `Math.i` file are as follows:
![](https://s2.loli.net/2023/06/24/rNuXMpy1azP6tZT.png)

### 2.2 \#define

```cpp
#define INTEGER int
```

This searches for the word `INTEGER` and replaces it with what follows.

![](https://s2.loli.net/2023/06/24/b2ivcAC1fh6lpUE.png)

### 2.3 \#if

Allows us to ==include== or ==exclude== code based on specific conditions.

```cpp
// Exclude
#if 0
int Multiply(int a, int b)
{
	int result = a * b;
	return result;
}
#endif
```

![](https://s2.loli.net/2023/06/24/are4fv3RF5w6Djn.png)

You can convert `.obj` files into a readable `.asm` format. To read binary, I used the VSCode plugin [Hex Editor](https://marketplace.visualstudio.com/items?itemName=ms-vscode.hexeditor).

## 3. Compiler Optimizations

### 3.1 Simple Case

```cpp
int result = a * b
return result

====>

return a * b
```

### 3.2 Constant Folding

```cpp
return 5 * 2

====>

return 10
```

![](./storage%20bag/Pasted%20image%2020230624210409.png)

### 3.3 Function Signatures and Calls

A "call" refers to invoking a function. Through symbol decoration, the function is given a unique signature, allowing the [linker](05%20How%20C++%20Works.md#^620dbb) to locate the function based on its signature.

![](./storage%20bag/Pasted%20image%2020230624211102.png)

Modifying the compiler can automatically optimize assembly instructions.

![](./storage%20bag/Pasted%20image%2020230624210044.png)

![](./storage%20bag/屏幕截图%202023-06-24%20210107.jpg)