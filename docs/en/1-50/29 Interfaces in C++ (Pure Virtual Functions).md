# Pure Virtual Functions and Interfaces in C++

Pure virtual functions allow us to define a function in a base class without providing an implementation, thereby forcing derived classes to implement that function.

In Object-Oriented Programming (OOP), it is very common to create a class that contains only unimplemented methods, which are then implemented by derived classes. This is often referred to as an *interface*. An interface is essentially a class that contains only unimplemented methods and serves as a template. Since the interface class does not contain any method implementations, we cannot instantiate it.

```cpp
class Entity
{
public:
	virtual std::string GetName() = 0;   // Still defined as a virtual function, but the =0 makes it a pure virtual function
};
```

This means that if you want to instantiate this class, the function must be implemented in a derived class.

![](./storage%20bag/Pasted%20image%2020230704194349.png)

```cpp
class Player : public Entity
{
private:
	std::string m_Name;
public:
	Player(const std::string& name)
		: m_Name(name) {}

	std::string GetName() override { return m_Name; } // If commented out, the class cannot be instantiated
};

void PrintName(Entity* entity)
{
	std::cout << entity->GetName() << std::endl;
}

int main()
{
	Entity* e = new Player("");  // Now it can be instantiated
	PrintName(e);
	Player* p = new Player("Cherno");
	PrintName(p);
```

After modifying it to `Player`, the class can now be instantiated simply because the `Player` subclass has implemented the `GetName` function. Therefore, it is clear that you can only instantiate a class that has implemented all pure virtual functions.

An *Interface* is just a class in C++.

```cpp
#include <iostream>
#include  <string>

class Printable
{
public:
	virtual  std::string GetClassName() = 0;
};

class Entity : public Printable
{
public:
	virtual std::string GetName() { return "Entity"; }
	std::string GetClassName() override { return "Entity"; }
};

class Player : public Entity
{
private:
	std::string m_Name;
public:
	Player(const std::string& name)
		: m_Name(name) {}

	std::string GetName() override { return m_Name; }
	std::string GetClassName() override { return "Player"; }
};

void PrintName(Entity* entity)
{
	std::cout << entity->GetName() << std::endl;
}


class A : public Printable
{
public:
	std::string GetClassName() override { return "A"; }
};

void Print(Printable* obj)
{
	std::cout << obj->GetClassName() << std::endl;
}

int main()
{
	Entity* e = new Entity();
	Player* p = new Player("Cherno");

	Print(e);
	Print(p);
	Print(new A());

	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230704200052.png)

By ensuring that a class has a specific method, we can pass an instance of that class as a parameter to a generic function, allowing us to call that function or perform other operations.