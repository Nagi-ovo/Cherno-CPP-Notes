## 1. Inheritance

Object-oriented programming is a very large programming paradigm, and class inheritance is one of its most fundamental concepts, as well as one of the most powerful features we can utilize. Inheritance establishes a hierarchical relationship between classes, in other words, it allows us to have a base class that contains common functionalities, from which many derived classes can be created.

This is why inheritance is incredibly useful—it helps us avoid writing a lot of duplicate code. *Code duplication* refers to the situation where we have to write the same code multiple times, or code that is slightly different but essentially performs the same task.

To avoid repeating ourselves over and over, we can place all common *functions* in a parent class, and then easily create derived classes from the base class, making slight modifications or introducing entirely new functionalities.

—— Inheritance provides us with a way to place all the common code (functionalities) of a series of classes into a base class, so we don’t have to repeat ourselves as if we were writing templates.

### Example
```cpp
class Entity
{
public:
	float X, Y;

	void Move(float xa,float ya)
	{
		X += xa;
		Y += ya;
	}
};

class Player // Similar to the Entity class, but with an additional Name and functionality
{
public:
	const char* Name;
	float X, Y;

	void Move(float xa, float ya)
	{
		X += xa;
		Y += ya;
	}
	
void PrintName()
	{
		std::cout << Name << std::endl;
	}
};
```
Now, the question arises:

## 2. How to Inherit?
```cpp
class Entity   // sizeof(Entity) = 8 (2 floats)
{
public:
	float X, Y;

	void Move(float xa,float ya)
	{
		X += xa;
		Y += ya;
	}
};

class Player : public Entity // Now this Player class is both an Entity and a Player
{                            // sizeof(Player) = 12 (2 floats, 1 char)
public:
	const char* Name;

	void PrintName()
	{
		std::cout << Name << std::endl;
	}
};

int main()
{
	Player player;
	player.PrintName();
	player.Move(5,5);
	std::cin.get();
}
```

## 3. Polymorphism
Polymorphism, in essence, is the ability to use a single symbol to represent multiple different types.