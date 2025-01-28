## 1. Purpose

The purpose of header files is not only for declarations, allowing you to use them across multiple `.cpp` files.

In the basics of C++, header files are traditionally used to declare certain function types so that they can be used throughout the program.
For review:
[06 How the C++ Compiler Works](06%20How%20the%20C++%20Compiler%20Works.md)
[07 How the C++ Linker Works.md^](07%20How%20the%20C++%20Linker%20Works.md^.md)

## 2. pragma

`#pragma` is a *preprocessor command* ([preprocessing](05%20How%20C++%20Works.md#^bafd29))

```cpp
#pragma once    // only include this file once
```

Therefore, it is essentially a *header guard*, preventing us from including the header file multiple times into a single *translation unit* ([see AST, translation unit](06%20How%20the%20C++%20Compiler%20Works.md#^c2b6d2))

That is, you might have many header files, and without a *header guard*, it is very likely that including both header files in a `.cpp` file could lead to redefinition.

Example:
```cpp
// #pragma once
struct Player{}    // struct type redefinition
```

## 3. Another Type of Guard

```cpp
#ifndef _LOG_H   // if _LOG_H is not defined
#define _LOG_H  

void InitLog();
void Log(const char* messsge);

#endif
```

This was mainstream in the past, but now `#pragma once` is preferred.

## 4. Include Supplement

Including with `" "` is a relative path. If it is in the directory above the current file, you can use `"../"`.
Including with `< >` means the file must be in one of the include directories, but now quotes can also be used, meaning `#include "iostream"` works fine.

#### Why iostream has no extension

It was decided by the people who wrote the standard library, to distinguish between *C Standard Library Header files* and *C++ Standard Library Header files*.

| C   | C++ |
| - | -|
| .h extension, e.g., stdlib.h  | None, e.g., iostream   |