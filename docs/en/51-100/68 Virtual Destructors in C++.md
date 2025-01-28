Context Recap: [26 Destructors in C++](26%20Destructors%20in%20C++.md), [27 Inheritance in C++](27%20Inheritance%20in%20C++.md), [28 Virtual Functions in C++](28%20Virtual%20Functions%20in%20C++.md)

A virtual destructor can be thought of as a combination of a virtual function and a destructor. Virtual destructors are crucial for handling polymorphism. In other words, if you have a series of subclasses and all inherit from a base class: there is a class A, and then a class B derived from A. If you want to reference class B as class A, but it is actually class B, and you decide to delete A or it gets deleted in some way, you still want to run B's destructor instead of A's destructor. This is what a virtual destructor is and what it does.

To understand it simply, let's look at the code:

```cpp
#include <iostream>

class Base
{
public:
	Base() { std::cout << "Base Constructor\n"; }
	~Base() { std::cout << "Base Destructor\n"; }
};


class Derived : public Base
{
public:
	Derived() { std::cout << "Derived Constructor\n"; }
	~Derived() { std::cout << "Derived Destructor\n"; }
};

int main()
{
	Base* base = new Base();
	delete base;
	std::cout << "---------------------\n";
	Derived* derived = new Derived();
	delete derived;

	std::cin.get();
}
```

You can probably guess the result:
When creating and deleting an instance of the Base class, only the Base class's constructor and destructor are called.
For the Derived class, the base class's constructor is called first, followed by the Derived class's constructor. When deleting, the Derived class's destructor is called first, followed by the base class's destructor.

![](./storage%20bag/Pasted%20image%2020230726214116.png)

Now let's introduce a polymorphic type:

```cpp
std::cout << "---------------------\n";
Base* poly = new Derived(); // Create a Derived instance but assign it to a Base pointer
delete poly;
```

![](./storage%20bag/Pasted%20image%2020230726214720.png)

Here, only the base class's destructor is called, and the derived class's destructor is not called. This is important because it can lead to memory leaks. When `delete` is called on `poly`, it doesn't know that the destructor being called might have another destructor to call, because `~Base` is not marked as virtual.

Marking a function as `virtual` means that C++ knows there might be some overridden method in the hierarchy, and this method can be overridden. A `virtual destructor` doesn't mean overriding the destructor, but **adding** a destructor. In other words, if I make the base class's destructor virtual, it will first call the derived class's destructor, and then move up the hierarchy to call the base class's destructor.

Let's illustrate why this can cause memory leaks:

```cpp
// Add an array member to the derived class
class Derived : public Base
{
public:
	Derived() { m_Array = new int[5]; std::cout << "Derived Constructor\n"; }
	~Derived() { delete[] m_Array; std::cout << "Derived Destructor\n"; }
private:
	int* m_Array;
};
```

Recalling the results from the previous program, it's clear that the derived class's destructor was not called, so the 20 bytes of memory allocated for the array were not freed, causing a memory leak.

So how do we fix this?
Simply make the base class's destructor `virtual`:

```cpp
class Base
{
public:
	Base() { std::cout << "Base Constructor\n"; }
	virtual ~Base() { std::cout << "Base Destructor\n"; }
};
```

This means that the class might be extended with subclasses, and there might be another destructor that needs to be called:

![](./storage%20bag/Pasted%20image%2020230726215832.png)

Great, now we have the exact same result as the second example, meaning that even if we treat it as a polymorphic type (or as a base class type), both the base and derived class's destructors are called, and the array is properly cleaned up.

So when you're writing a class that might be extended or subclassed, as long as you allow a class to have subclasses, you 100% need to declare your destructor as virtual; otherwise, you cannot safely extend the class.