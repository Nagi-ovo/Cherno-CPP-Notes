## 1. Abstract syntax tree

编译器的工作是把代码转化为*constant data*(常数资料)和*instructions*(指令)，构建抽象语法树后开始生产代码

cpp 中没有文件的概念，文件只是给编译器提供源码的一个方式

.cpp 告诉编译器用 c++编译->编译器当成一个*translation unit*->得到一个.obj

常见的[preprocessor](05%20How%20C++%20Works.md#^bafd29)语句==pragma statement==

```c++
include
define
if
ifdef
```

## 常见的 Preprocessor statement

### 2. 1 \#include

`#include`就是把想要的文件中的内容复制进来.比如创建了一个 EndBrace.h,2 其中的内容是：

```cpp
}
```

则我的 Multiple 函数这么写仍可以正常编译

```cpp
int Multiply(int a, int b)
{
	int result = a * b;
	return result;
	#include "EndBrace.h"
```

检查 Preprocess 的文件，可通过如下操作生成.i 文件

![](https://s2.loli.net/2023/06/24/oAysjHlPzxdfbtR.png)

Math.i 文件内容如下
![](https://s2.loli.net/2023/06/24/rNuXMpy1azP6tZT.png)

### 2.2 \#define

```cpp
#define INTEGER int
```

搜索 INTEGER 这个词，然后替换成后面的东西

![](https://s2.loli.net/2023/06/24/b2ivcAC1fh6lpUE.png)

### 2.3 \#if

可以让我们依据特定条件==包含==或==剔除==代码

```cpp
//剔除
#if 0
int Multiply(int a, int b)
{
	int result = a * b;
	return result;
}
#endif

```

![](https://s2.loli.net/2023/06/24/are4fv3RF5w6Djn.png)

可将.obj 转化为可读版本的.asm 文件，阅读二进制用了 vscode 插件[Hex Editor](https://marketplace.visualstudio.com/items?itemName=ms-vscode.hexeditor)

## 3. 编译器优化

### 3.1 简单案例

```cpp
int result = a * b
return result

====>

return a * b
```

### 3.2 constant folding

```cpp
return 5 * 2

====>

return 10
```

![](./storage%20bag/Pasted%20image%2020230624210409.png)

### 3.3 函数签名和 call

call 即调用函数，通过图中的符号修饰对函数做唯一签名认真，让[linker](05%20How%20C++%20Works.md#^620dbb)按函数签名寻找函数

![](./storage%20bag/Pasted%20image%2020230624211102.png) 

修改编译器，可以自动优化汇编指令

![](./storage%20bag/Pasted%20image%2020230624210044.png)

![](./storage%20bag/屏幕截图%202023-06-24%20210107.jpg)
