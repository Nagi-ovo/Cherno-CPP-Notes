if statements

`==`是*equality*运算符,标准库中实现的，将两个整数的四个字节抓出来逐位比较。

## 1. Disassembly

在[Debug 模式](11%20How%20to%20DEBUG%20C++%20in%20Visual%20Studio.md#^a1059f)下调试时，右键或 Ctrl+K，G 即可调出 Go to disaseembly
![](Pasted%20image%2020230627161844.png)

`jne`(jump not equal)，如果不相等就跳转

```assembly
00C8601E  mov         dword ptr [ebp-0DCh],0  ; boolean被赋值0（false）
```

如果`00C86035  test   eax,eax `成功，即 test 操作是 true，则会执行`je`(jump equal)，则会跳转到 cin.get()那句

![](./storage%20bag/Pasted%20image%2020230627162803.png)

## 2. Constant folding （常数折叠）

编译器最佳化技术。会把这些都转到一个常变量中，因为这些常量都会在编译时被知晓。然后编译时直接去掉 if 等部分，直接跳到 cin.get()

所以要在 Debug 模式下操作。

可以写成

```c++
if (x==5)
	Log("Hello World")   //如果在同一行不方便打断点
```

## 3. if else

```cpp
const char* ptr = "Hello";
if (ptr)
	Log(ptr);
else if (ptr == "Hello")
	Log("ptr is Hello");
```

只有在 if 失败的情况下，才执行 else 后的代码，即只有 ptr 为 false，才执行 else if.....
![](./storage%20bag/Pasted%20image%2020230627170041.png)
原因如下

#### else if 就是一个 else 和 if

```cpp
else if (ptr == "Hello")
	Log("ptr is Hello");

//等价于

else
{
	if (ptr == "Hello")
		Log("ptr is Hello");
}

```

编程=数学部分+逻辑部分 ^2780f2

可能会用某些运算来代替比较和分支，让代码更快更实用。
