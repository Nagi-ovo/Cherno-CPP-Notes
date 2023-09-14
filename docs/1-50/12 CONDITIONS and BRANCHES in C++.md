if statements

`==`是*equality*运算符,标准库中实现的，将两个整数的四个字节抓出来逐位比较。

## 1. Disassembly

在[Debug模式](11%20How%20to%20DEBUG%20C++%20in%20Visual%20Studio.md#^a1059f)下调试时，右键或Ctrl+K，G即可调出Go to disaseembly
![](Pasted%20image%2020230627161844.png)

`jne`(jump not equal)，如果不相等就跳转

```assembly
00C8601E  mov         dword ptr [ebp-0DCh],0  ; boolean被赋值0（false）
```

如果`00C86035  test   eax,eax `成功，即test操作是true，则会执行`je`(jump equal)，则会跳转到cin.get()那句

![](Pasted%20image%2020230627162803.png)

## 2. Constant  folding （常数折叠）

编译器最佳化技术。会把这些都转到一个常变量中，因为这些常量都会在编译时被知晓。然后编译时直接去掉if等部分，直接跳到cin.get()

所以要在Debug模式下操作。


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

只有在if失败的情况下，才执行else后的代码，即只有ptr为false，才执行else if.....
![](Pasted%20image%2020230627170041.png)
原因如下

#### else if 就是一个else和if
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