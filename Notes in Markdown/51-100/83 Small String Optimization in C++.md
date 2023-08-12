小字符串优化，简称SSO。
字符串往往会和性能差联想到一起，本节主要关注C++标准库如何优化小字符串。

我们都知道创建一个标准字符串会导致内存分配，所以很多人会尽量减少字符串的使用。但是标准库中，小字符串（也就是不是很长的字符串），它们不需要堆分配，我们可以只分配一小块基于栈的缓冲区而不是堆分配的。如果你有一个不超过15个字符的字符串（VS2019），它不会在堆上分配内存，换句话说对于很小的字符串你就不要使用`const char*`或视图微观管理、优化你的代码了。

![](Pasted%20image%2020230806012752.png)
> 重要的的主要函数是assign，它接受一个指针参数，也就是const char*，我们的字符串

![](Pasted%20image%2020230806013023.png)
> 这里有一个if语句，如果满足则简单地将我们的字符串移到这个内存缓冲区中，就没有分配了；如果没通过if，则会Reallocate，调用new操作符导致堆分配。

来查一下这个Myres是多少：

![](Pasted%20image%2020230806013328.png)
> 可以看到它被设置为缓冲区大小-1

![](Pasted%20image%2020230806013455.png)
> 这个缓冲区大小_BUF_SIZE等于_Scary_val::\_BUF\_SIZE

![](Pasted%20image%2020230806013432.png)
> 而它又等于一个constexpr（常量表达式），这个例子中它是16，减去1后是15

```cpp
#include <iostream>
#include <string>

void* operator new(size_t size)  // 操作符重载
{
	std::cout << "Allocating " << size << " bytes\n";
	return malloc(size);
}

int main()
{
	std::string name = "Cherno";  // 显然小于15个字符
	std::cin.get();
}
```

如果F5运行，会发现依然打印分配了8字节内存，这其实是VS的string类的问题，基本只在Debug模式下发生，因此切换到Release模式运行就可以看到想要的结果了：

![](Pasted%20image%2020230806013905.png)

```cpp
std::string name = "Cherno Small St"; // 15个字符，没有分配
std::string name = "Cherno Small St "; // 16个字符，立即产生32个字节的堆上内存分配
```

![](Pasted%20image%2020230806014248.png)

这是一种优化，效率更高，更快。

那Debug模式下发生了什么导致了分配呢？

![](Pasted%20image%2020230806014815.png)
> 如果调试等级为0，也就是Release模式下，只会调用Fake_allocator，而它其实什么都不做：
> ![](Pasted%20image%2020230806014947.png)
> 如果是Debug模式就会因这个proxy_ptr造成分配。



