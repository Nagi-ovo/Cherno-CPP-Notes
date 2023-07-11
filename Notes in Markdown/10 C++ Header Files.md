## 1. 用途

头文件的用途不仅是声明，以供你在多个cpp文件中使用

C++基础中，头文件传统上是用来声明某些函数类型，以便可以用于整个程序中使用。
可复习：
[06 How the C++ Compiler Works](06%20How%20the%20C++%20Compiler%20Works.md)
[07 How the C++ Linker Works.md^](07%20How%20the%20C++%20Linker%20Works.md^.md)

## 2. pragma

`#pragma`是一个*preprocessor command*([预处理](05%20How%20C++%20Works.md#^bafd29))

```cpp
#pragma once    // only include this file once
```

因此它其实是一个*header guard*(头文件保护符)，防止我们把头文件多次include到一个单一*translation unit*([见AST，翻译单元](06%20How%20the%20C++%20Compiler%20Works.md#^c2b6d2))

即你可能会有很多个头文件，如果没有*header guard*，很有可能在一个.cpp文件同时include这两个头文件时导致重复定义

exp：
```cpp
// #pragma once
struct Player{}    // struct type redefinition
```

## 3. 另一种保护符

```cpp
#ifndef _LOG_H   // if _LOG_H is not defined
#define _LOG_H  

void InitLog();
void Log(const char* messsge);

#endif
```

过去主流，现在还是用`#pragma once`

## 4. include补充

inculde `" "` 为相对路径，若在当前文件上一目录，则可为 `"../"`。
include `< >`则是文件必须在所有include目录中的某一个，不过现在引号也可以了，即`include "iostream"`可以正常工作。


#### 为什么iostream没有拓展名

写标准库的人决定的，为了区分*C Standard Library Header files*和*C++ Standard Library Header files*

| C   | C++ |
| - | -|
| .h拓展名，如stdlib.h  | 无，如iostream   |

