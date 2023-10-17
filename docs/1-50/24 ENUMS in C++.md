_enumeration_(枚举)

定义枚举类型的主要目的：增加程序可读性

枚举值就是一个*integer*

```cpp
enum Example
{
	A,B,C
};

int a = 0;
int b = 1;
int c = 2;

int main()
{
	Example value = B; // 类型为一个enum，因此赋值只能在A,B,C中

	if (value == B)
	{
		// Do something here
	}
	std::cin.get();
}
```

默认情况下，第一个变量的值为 0，依次递增

![](./storage%20bag/Pasted%20image%2020230703095443.png)

![](./storage%20bag/Pasted%20image%2020230703095529.png)

可以声明类型，节省内存空间

```cpp
enum Example : char
{
	A=5,B,C
};
```
