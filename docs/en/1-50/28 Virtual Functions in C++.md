## 1. Virtual Functions

Virtual functions allow us to override methods in derived classes.  
For example, if `B` is a subclass of `A`, and we define a method in class `A` and mark it as a virtual function, we can override this method in class `B` to make it perform different actions.

```cpp
#include <iostream>
#include  <string>

class Entity
{
public:
	std::string GetName() { return "Entity"; }
};

class Player : public  Entity
{
private:
	std::string m_Name;
public:
	Player(const std::string& name)   // Constructor learned in lesson 25
		: m_Name(name) {}

	std::string GetName() { return m_Name; }
};

int main()
{
	Entity* e = new Entity();
	std::cout << e->GetName()<< std::endl;

	Player* p = new Player("Cherno");
	std::cout << p->GetName() << std::endl;

	Entity* entity = p;
	std::cout << entity->GetName() << std::endl;

	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230704181515.png)  
Here, although we are pointing to an `Entity` _pointer_, it is actually an instance of the `Player` class.

### A Better Example

```cpp
void PrintName(Entity* entity)
{
	std::cout << entity->GetName() << std::endl;
}
int main()
{
	Entity* e = new Entity();
	PrintName(e);                             //Entity
	Player* p = new Player("Cherno");
	PrintName(p);                             //Entity

	std::cin.get();
}
```

The reason is that if we declare a function or method normally in a class, when it calls this method, it will always call the method belonging to that type.

Here, we want the C++ compiler to know that the second argument passed is actually a `Player`, so please call the `GetName` method of `Player`.  
This is where *virtual functions* come into play.

Virtual functions introduce a method of dynamic dispatch, usually implemented through a *vtable* (virtual table) during compilation.  
A vtable is a list containing mappings of all virtual functions in a class. Through the vtable, we can find the correct overridden function at runtime.  
Simply put, if you want to override a function, you must **mark the original function in the base class as virtual**.

```cpp
class Entity
{
public:
	virtual std::string GetName() { return "Entity"; }   // Marked as a virtual function
};
```

Now it will correctly print `Entity` and `Cherno`.  
![](./storage%20bag/Pasted%20image%2020230704182832.png)

The C++11 standard allows marking overridden functions with the `override` keyword.

```cpp
	std::string GetName() override { return m_Name; }
```

It won't cause an error if you don't include it, but adding it improves readability, making it clear that the function is overridden. It also helps prevent bugs, such as typos.  
![](./storage%20bag/Pasted%20image%2020230704183318.png)  
For example, if `N` is written as lowercase `n`, an error will occur because there is no such function in the base class to override.

## 2. Runtime

Virtual functions are not without cost. There are two runtime costs associated with virtual functions.

One is the additional memory required to store the vtable, which allows us to dispatch to the correct function. The base class also contains a pointer member pointing to the vtable.

The other is that every time a virtual function is called, we must traverse the vtable to find the final function to execute, which incurs additional performance overhead.

Unless you're working on an embedded platform with a very weak CPU, you won't be told to avoid using virtual functions due to performance concerns, as the impact is minimal and you might not even notice it.