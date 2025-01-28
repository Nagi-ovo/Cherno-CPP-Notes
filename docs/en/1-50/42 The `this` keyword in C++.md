In C++, there is a keyword called `this`, which allows access to member functions.  
`this` is a pointer to the current object instance, and the *method* belongs to this object instance.

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

If we don't use [Member Initializer Lists](36%20%20Member%20Initializer%20Lists%20in%20C++%20(Constructor%20Initializer%20List).md) (as shown in the comment), and instead write inside the method, since the parameter `x` and the member `x` have the same name, `x = x` will only assign the passed `x` to itself, effectively doing nothing.

What I really want to do is reference the `x` and `y` that belong to this class. The `this` keyword allows us to achieve this.
```cpp
Entity* e = this;
e->x = x;
// Or directly use the arrow operator
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