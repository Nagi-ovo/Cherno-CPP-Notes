## 1. 为什么要使用 namespace

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

这里有两个函数签名一样的函数，这两个的*symbol*（符号)是相同的，如果放在一个文件里的话会产生链接错误、编译错误。那如果我们确实想要两个 print 函数，或者使用另一个已经定义了 print 函数的库，但是我们想有自己的 print 函数。
C 语言没有 namespace，比如使用 GLFW 库（C 语言的 OpenGL 库），调用的每个函数名都是用 GLFW 开头的。
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
![](./storage%20bag/Pasted%20image%2020230723174600.png)

还可以给命名空间起别名：
![](./storage%20bag/Pasted%20image%2020230723175142.png)

尽量将 namepace 限制在一个小的作用域下，一定不要加在头文件里。
