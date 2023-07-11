*Breakpoints* and *reading memory*

设断点来读取内存

## 1. Breakpoints

断点是程序中调试器会*break*(中断)的一个点，当执行到断点所在行时，执行线程会悬停

#### Visual Studio断点快捷键：F9

*Debug*(调试)时，要确保自己==在“Debug”模式下==，配置可见[Configuration](05%20How%20C++%20Works.md#^0b34c7)
“Release”模式下代码会被更改，你的断点可能永远不会执行 ^a1059f

### 调试
##### Step Into : F11
##### Step Over : F10
##### Step Out : Shift + F11


![](Pasted%20image%2020230626144929.png)

现在对main函数的第七行进行*Step into*

![](Pasted%20image%2020230626144858.png)

黄色箭头表明还没执行当前行，按F10箭头到第六行
再次F10后，字符串才被输出
![](Pasted%20image%2020230626145245.png)


看这段程序：
```cpp
int main()
{
·	int a = 8;   //断点
	a++;
	const char* string = "Hello";

	for (int i = 0; i < 5; i++)
	{
		const char c = string[i];
		std::cout << c << std::endl;
	}

	Log("Hello Wolrd");
	std::cin.get();
}
```

此时`int a=8`还没有被执行，还是没初始化的内存
![](Pasted%20image%2020230626145932.png)

### Memory View（内存视图）

^dd3537

Debug过程中，上方导航栏Debug->Windows->Memory->Memory1即可调出内存视图
![](Pasted%20image%2020230626150626.png)

输入`&a`即可访问变量a的内存地址，其中都是16进制数。

#### 为什么都是cc？

说明这是一个未初始化的堆栈内存

按下F10
![](Pasted%20image%2020230626151308.png)

可以看到内存中存储的数据发生改变。其中==*每两个十六进制数字代表一个字节*==。

如果我想跳出循环，按Step Out会跳出整个函数。所以只需要再设一个断点，再按F5即可运行到断点处。
![](Pasted%20image%2020230626152501.png)