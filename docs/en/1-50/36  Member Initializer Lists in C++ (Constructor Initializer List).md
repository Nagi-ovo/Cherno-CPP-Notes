# Constructor Initialization List

The constructor initialization list is a way to initialize class members within the constructor. When we write a class and add members to it, we usually need to initialize these members in some way, which typically happens in the constructor. There are two methods to initialize class members within the constructor.

## 1. Constructor Initialization

### 1. General Method

```cpp
#include <iostream>
#include <string>
#define LOG(x) std::cout << x << std::endl;

class Entity
{
private:
	std::string m_Name;
public:
	Entity()    // Entity entity1; calls the default constructor, using "Unknown" as the name by default
	{
		m_Name = "Unknown";
	}

	Entity(const std::string& name)    // Entity entity2("Alice"); calls the parameterized constructor, using "Alice" as the name
	{
		m_Name = name;
	}

	const std::string& GetName() const { return m_Name; };
};

int main()
{
	Entity e;
	LOG(e.GetName())           // "Unknown"
	Entity e1("Cherno");
	LOG(e1.GetName())          // "Cherno"
	std::cin.get();
}
```

### 2. Constructor Initialization List

```cpp
class Entity
{
private:
	std::string m_Name;
	int m_Score;
public:
	Entity()
		: m_Name("Unknown"), m_Score(0)  // Initialize in the order of class member definitions, otherwise the compiler may issue a warning
	{
	}

	Entity(const std::string& name)
		: m_Name(name)    // Equivalent to replacing the equals sign with parentheses and moving it into the list
	{
	   // m_Name = name;
	}


	const std::string& GetName() const { return m_Name; };
};

int main()
{
	Entity e;
	LOG(e.GetName())
	Entity e1("Cherno");
	LOG(e1.GetName())
	std::cin.get();
}
```

No matter how you write the initialization list, it will always initialize members in the order they are defined in the class. Breaking this order can lead to various dependency issues. Therefore, ensure that the member initialization list follows the same order as the member variable declarations.

#### Why Use This?

For code style reasons, if there are many variables, writing them in the initialization list keeps our constructor code clean and easy to read.

There is also a functional difference, particularly when it comes to classes.

```cpp
Entity()
	:  x(0),y(0),z(0)
{
	m_Name = "Unknown";    // m_Name will be constructed twice
	// Equivalent to std::string("Unknown");
}
```

You create two strings, one of which is immediately discarded, resulting in a performance waste.

```cpp
class Example
{
public:
	Example()
	{
		LOG("Created Entity!");
	}

	Example(int x)
	{
		std::cout << "Created Entity with " << x << "!" << std::endl;
	}
};

class Entity
{
private:
	std::string m_Name;
	Example m_Example;
public:
	Entity()
	{
		m_Name = std::string("Unknown");
		m_Example = Example(8);
	}

	Entity(const std::string& name)
		: m_Name(name)
	{
	}

	const std::string& GetName() const { return m_Name; };
};

int main()
{
	Entity e;                // "Created Entity!"
                             // "Created Entity with 8"

	std::cin.get();
}
```

Here, two `Entity` objects are created: one is created in `private: Example m_Example;` and the other is created in `m_Example = Example(8);`. In this case, a new `Example` object is created and assigned to `m_Example` (the old one), resulting in a performance waste due to overwriting.

However, if we move this to the initialization list:

```cpp
Entity()
	: m_Example(8)
	// : m_Example(Example(8))
{
	m_Name = std::string("Unknown");
}
```

This way, only one object is created. Therefore, you should always use member initialization lists; there is absolutely no reason not to use them.