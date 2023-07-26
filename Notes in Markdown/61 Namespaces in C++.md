
## 1. 为什么要使用namespace

```cpp
void print(const char* text)
{
	std::cout << text << std::endl;
}
	
void print(const char* text)
{
	std::string temp = text;
	std::reverse(temp.begin(),temp.end());
	std::cout << temp << std::endl;
}
```
这里有两个函数签名一样的函数，这两个的*symbol*（符号)是相同的，如果放在一个文件里的话会产生链接错误、编译错误。那如果我们确实想要两个print函数，或者使用另一个已经定义了print函数的库，但是我们想有自己的print函数。
C语言没有namespace，比如使用GLFW库（C语言的OpenGL库），调用的每个函数名都是用GLFW开头的。
所以*namespace*（名称空间）的主要目的就是避免命名冲突。

可以把命名空间放在一行，这样多层嵌套时观感会好些：
```cpp
namespace apple { namespace functions {

	void print(const char* text)
	{
		std::cout << text << std::endl;
	}
} }
```

`::`是命名空间的操作符，类也是一种命名空间，这就是为什么访问另一个类内部的类等成员时也用`::`来调用

还可以单独引入函数：
![](Pasted%20image%2020230723174600.png)
还可以给命名空间起别名：
![](Pasted%20image%2020230723175142.png)

尽量将namepace限制在一个小的作用域下，一定不要加在头文件里。