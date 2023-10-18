## 1. 前言

调好了.vssettings,VsVim,但是 Ob 的`imap jj <Esc>`死活搞不定，事已至此，学习吧。
(第二天发现重启后映射就能用了......)
从 25 课回来的补充，视频中 Cherno 用的是 Visual Assist，正版价格对国内不友好。而 VS 可以装一个 JetBrains ReSharper C++插件，教育邮箱可白嫖，爽飞了。

## 2. 基本概念

### 2.1 头文件

带有`#`的为*preprocessor statement*，即预处理指令
该类指令发生在真正的编译之前
当编译器收到一个源文件时，做的第一件事情就是预处理所有预处理指令

```cpp
#include <iostream>
```

即找到`iostream`文件，将该文件中的所有内容复制粘贴到目前的文件里
这些被 include 的文件一般被称为*header file*,即头文件

每个 cpp 程序都有一个类似`main`函数的东西，被称作*entry point*

## 2. 基本概念

### 2.1 头文件

带有`#`的为*preprocessor statement*，即预处理指令
该类指令发生在真正的编译之前
当编译器收到一个源文件时，做的第一件事情就是预处理所有预处理指令

```cpp
#include <iostream>
```

即找到`iostream`文件，将该文件中的所有内容复制粘贴到目前的文件里
这些被 include 的文件一般被称为*header file*,即头文件

每个 cpp 程序都有一个类似`main`函数的东西，被称作*entry point*
后面了解到这个必须的原因在于.exe 可执行文件必须需要一个入口，可在设置中自定义入口点（不一定必须是 main function）

只有主函数可以不返回任何值，默认返回 0

*preprocessor statement*被评估后，我们的文件会被编译，这个阶段，编译器把我们的 cpp 代码转化为实际的机器码

### 2.2 Visual Studio 相关

![](./storage%20bag/Pasted%20image%2020230621232703.png)

> 配置*Configuration*是如何 build 一个项目的一系列规则

![](./storage%20bag/Pasted%20image%2020230621232713.png)

> *Solution platform*使我们目前编译的目标平台，x86 就是生成一个用于 windows 的 32 位程序，你要求弄安卓程序就改成安卓相关的

若要修改我们的配置，右键项目点击*Properties*,得到下面界面
![](./storage%20bag/Pasted%20image%2020230621233202.png)

> _==注意==_:确保*Active*的是你想修改的，有可能会不是

### 2.3 Linker 链接器

所有.cpp 文件都会被编译，.h 头文件不会被编译，它会通过 include 到 cpp 中，然后被编译
每个.cpp 文件都被编译成一个*Object*文件（.obj)，将所有.obj 文件连在一起，成为一个.exe 文件

*Compile*编译单个.cpp 文件，快捷键==Ctrl+F7==

_==注意==_:error list 不好用，工作原理是*parse*(解析)output 窗口，找 error 关键字，然后从那里找信息再放入 list,仅当做概述看。
要具体的、所有的错误信息，只能通过 output 窗口

双击 output 窗口的 error 信息即可跳转到错误行

### 2.4 Declaration 声明

编译器识别不出另一个.cpp 文件中的函数，所以报告编译错误吗，可以通过提供一个声明*declaration*来解决

| Declaration  | Defination                 |
| ------------ | -------------------------- |
| 声明函数存在 | 这个函数是什么，函数的主体 |
| void Log(x)  | void Log(x){ code...}      |

文件被编译后，linker 会去找函数的定义，然后跟 main 中调用的联系起来。如果找不到会得到 linker error
只有主函数可以不返回任何值，默认返回 0

*preprocessor statement*被评估后，我们的文件会被编译，这个阶段，编译器把我们的 cpp 代码转化为实际的机器码
