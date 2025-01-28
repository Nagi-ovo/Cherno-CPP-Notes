*structure* (struct) and *class* are essentially the same with minimal differences.

## 1. The Only Difference

*struct* defaults to *public* access.

```cpp
struct Player
{	
	int x, y;
	int speed;
};

	
int main()
{
	Player player;
	player.x = 5;   // No compilation error
	std::cin.get();
}
```

```cpp
struct Player  // Setting private attributes
{	
private:
	int x, y;
	int speed;
};

int main()
{
	Player player;
	player.x = 5;   // Compilation error
	std::cin.get();
}
```

## 2. Usage Differences

Functionally, there is not much difference, but there are distinctions in actual code usage.

The only reason *struct* exists in C++ is to maintain compatibility with C, as C does not have *class*.

The choice between using *struct* or *class* is subjective and depends on individual programming style. For example, use *struct* if you want default public access.

### Cherno's Idea

- *struct*: Used only to represent some data, absolutely no inheritance.
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

- *class*: Classes with many functionalities, possibly involving inheritance.