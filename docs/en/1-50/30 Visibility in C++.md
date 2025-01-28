It is a concept in OOP that refers to whether the members or methods of a class are visible. Visibility means who can access them, who can call them, and who can use them.

Visibility does not affect the actual running state of your program, nor does it affect aspects like program performance. It is purely a language-level concept that helps you write better code and organize your code more effectively.

## 1. Three Basic Visibility Modifiers
### 1. private
The difference between *struct and public*: struct defaults to public, while class defaults to private. See [Lesson 19](19%20CLASSES%20vs%20STRUCTS%20in%20C++.md#^d8987b)
```cpp
class Entity
{
private:    // Only *this Entity class can access these variables
	int X, Y;
};
```

Only *: Actually, in C++, there is also a keyword called *friend* that can mark other classes or functions as friends of the current class, allowing you to access the **private** members of this class.

```cpp
class Entity
{
private:
	int X, Y;
	void Print() {}
public:
	Entity()
	{
		X = 0;
		Print();  
	}
};

class Player : public Entity
{
public:
	Player()
	{
		X = 2;
		Print();  // Cannot access
	}
};

int main()
{
	Entity e;
	e.Print();    // Cannot access
	e.X = 2;      // Cannot access
	
	std::cin.get();
}
```
### 2. protected

The visibility of *protected* is higher than *private* but lower than *public*.
It means that this class and all its derived classes can access these members.
```cpp
protected:  // Derived classes can access
	int X, Y;

	void Print() {}
......

class Player : public Entity
{
public:
	Player()
	{
		X = 2;
		Print();   // Can access
	}
};

int main()   
{
	Entity e;
	e.Print();    // Not a subclass, cannot access
	e.X = 2;      // Cannot access
	
	std::cin.get();
}
```

### 3. public

```cpp
class Entity
{
public:
	int X, Y;

	void Print() {}
public:
	Entity()
	{
		X = 0;
		Print();
	}
};

class Player : public Entity
{
public:
	Player()
	{
		X = 2;
		Print();   // Can access
	}
};

int main()
{
	Entity e;
	e.Print();     // Can access
	e.X = 2;       // Can access
	
	std::cin.get();
}
```

## 2. Why Set Visibility

First, setting everything to *public* is definitely a bad idea for developers.

Specifying visibility ensures that others do not call code they should not touch, causing some damage.

It also provides better readability, so you don't forget.