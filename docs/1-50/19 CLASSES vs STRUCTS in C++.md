*structure*(结构体)和*class*(类)，二者基本没区别。

## 1. 唯一区别

^d8987b

*struct*默认是*public*的

```cpp
struct Player
{	
	int x, y;
	int speed;
};

	
int main()
{
	Player player;
	player.x = 5;   // 编译不报错
	std::cin.get();
}
```

```cpp
struct Player  // 设置私有属性
{	
private:
	int x, y;
	int speed;
};

int main()
{
	Player player;
	player.x = 5;   // 编译报错
	std::cin.get();
}
```

## 2. 使用区别

作用上确实区别不大，但是代码实际使用时确实有所不同。

C++中结构体存在的唯一原因是因为它想要维持与C之间的兼容性，因为C中没有*class*

二者的使用选择每人有自己的理解，是个人的编程风格。比如想默认public就用struct


### Cherno‘s idea

- struct: 只用来表示一些数据，绝对不继承
```cpp
struct Vec2
{
	float x, y;

	void Add(const Vec2& other)
	{
		x += other.x;
		y += other.y;
	}
};

```

- class：很多功能的类，可能继承的东西