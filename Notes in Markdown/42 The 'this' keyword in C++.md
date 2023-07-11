C++中有这样一个关键字*this*，通过它可以访问成员函数。
`this`是一个指向当前对象实例的指针，该*method*(方法)属于这个对象实例。

```cpp
class Entity
{
public:
	int x, y;

	Entity(int x,int y)
	// : x(x),y(y)
	{
		x = x;
	}
};

```
如果不用[Member Initializer Lists](36%20%20Member%20Initializer%20Lists%20in%20C++%20(Constructor%20Initializer%20List).md)（像注释中一样），我想在方法内部写，由于传入参数的x和成员x名字一样，`x=x`只会让传入的x赋值给它自己，也就是什么都不做。

而我真正想做的是引用属于这个类的x和y，`this`关键字可以让我们做到这一点。
```cpp
Entity* e = this;
e->x = x;
// 或者直接用箭头运算符
this->x = x;
```

```cpp
#include <iostream>

class Entity;
void PrintEntity(Entity* e);

class Entity
{
public:
	int x, y;

	Entity(int x,int y)
	{
		this->x = x;
		this->y = y;
		PrintEntity(this);
	}

	int GetX() const
	{
		// this->x = 5;
		const Entity* e = this;
		return this->x;
	}
};


void PrintEntity(Entity* e)
{
	// Print
}

```