## 1. Linking

一旦编译了文件，我们就需要一个叫*Linking*（链接）的过程，其主要工作是找到每个符号和函数的位置，并将他们链接在一起。由于编译时每个.cpp 都会变成.obj，我们如果要做一个很多.cpp 文件的项目时，每个文件实际没法沟通，因此需要[Linker](05%20How%20C++%20Works.md#^620dbb)链接器。

就算你都写在一个文件里了，找到程序的[entry part](05%20How%20C++%20Works.md#^2224fe)，也就是主函数在哪儿，也需要链接器来链接主函数和其他东西

## 2. 报错相关

### 2.1

语法错误、没找到函数： 报错示例为 C+XXXX，表明是[Compiling](./storage%20bag/06%20How%20the%20C++%20Compiler%20Works.md)期间的问题。

### 2.2

缺乏主函数 entry point： 报错示例为 LNK+XXXX，代表是链接期间发声的问题。

### 2.3

Unresolved external symbol ：函数定义和函数声明有区别，若没有调用则不会报错。或者可通过`static `解决，可使链接只发生在文件内部。

### 2.4

Duplicate symbol： 有函数或者变量名字和签名相同，两个函数名字、返回值、参数相同，Linker 不知道链接哪个。很可能发声，比如.h 中调用，又[#include](06%20How%20the%20C++%20Compiler%20Works.md#^f8f616)到了别的文件中，就会造成此问题。可通过`static`解决，使链接只发生在文件内部。或者`inline`。
推荐的方法是将函数声明都放在.h 头文件中，定义放在.cpp 中
