Effect can be seen at: [Static in Class](21%20Static%20in%20C++.md#^e0f8b6)

If you create a `static` variable inside a class, there will be only one instance of this variable across all instances of the class. Similarly, if one instance modifies this variable, the change will be reflected in all instances of the class. It's like a *global* instance for the class.

```cpp
struct Entity  // Using struct to default to public
{
	int x, y;

	void Print()
	{
		std::cout << x << "," << y << std::endl;
	}
};

int main()
{
	Entity e;
	e.x = 2;
	e.y = 3;

	Entity e1 = { 5,8 };  // Initializer

	e.Print();   // 2, 3
	e1.Print();  // 5, 8
	std::cin.get();
}
```

```cpp
struct Entity  // Using struct to default to public
{
	static int x, y;

	void Print()
	{
		std::cout << x << "," << y << std::endl;
	}
};

int Entity::x;
int Entity::y;

int main()
{
	Entity e;
	e.x = 2;  // Entity::x;
	e.y = 3;  // Entity::y;
	e.Print();

	Entity e1;
	Entity::x = 5;
	Entity::y = 8;

	e1.Print();
	std::cin.get();
}

	Entity e1;
	Entity::x = 5;
	Entity::y = 8;

	e1.Print();
	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230703002745.png)

A *static method* cannot access non-static variables. Every non-static method you write in a class receives the current class instance as a parameter (the `this` pointer).

```cpp
static void Print(Entity e)  // Pass by reference
{
	std::cout << e.x << "," << e.y << std::endl;
}
```