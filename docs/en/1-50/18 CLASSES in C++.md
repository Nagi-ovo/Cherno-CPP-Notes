# Learning Notes on Cherno's C++ Tutorial for Game Engine Developers

*Object Oriented Programming* (OOP) is just a programming style you adopt when writing code. Languages like Java and C# are inherently OOP, and it's generally best to stick to this style when using these languages (unless you absolutely have to do otherwise). Overall, these languages are best suited for object-oriented programming.

C++, however, is not limited to just OOP. It supports procedural programming, object-based programming, object-oriented programming, and generic programming. C, on the other hand, does not support OOP because OOP requires concepts like *class* and *object*.

## 1. Class

In simple terms, a class is a way to organize data and functions together.

If you're making a game, a game character might have many attributes, such as position, state, etc. If there are multiple characters, you would have to repeatedly define these attributes. You could use arrays to manage these, but the point is that this would still leave your code cluttered with disorganized variables, which is obviously not a good idea. Moreover, if you want to create a function to move a character, you would need three integers as parameters for the function, like this:

```cpp
void Move(int x, int y, int speed) // coordinates and speed
```

This would result in a lot of code and make maintenance difficult.

Therefore, you can use a *class* to simplify this. You can create a `Player` class that contains all the desired data as a single entity.

A variable of type *class* is called an *object*. The process of creating a new object is called *instantiation*. ^b700f7

## 2. Class Access

```cpp
class Player
{	
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

By default, members of a class have *private* access control, meaning only functions within the class can access these variables. If we want to access these variables in the `main` function, we need to define them as *public*.

```cpp
class Player
{	
public:
	int x, y;
	int speed;
};

	
int main()
{
	Player player;
	player.x = 5;  // Compiles successfully
	std::cin.get();
}
```

## 3. Method

Functions within a *class* are called *methods*.

#### General Definition of Move()

```cpp
class Player
{	
public:
	int x, y;
	int speed;
};


void Move(Player& player, int xa, int ya)
{
	player.x += xa * player.speed;
	player.y += ya * player.speed;

}

int main()
{
	Player player;
	Move(player,1,-1)
	std::cin.get();
}
```

#### Converting Move() to a Method

```cpp
class Player
{	
public:
	int x, y;                  // Variable 1              
	int speed;                 // Variable 2
	void Move(int xa, int ya)  // Variable 3    // Removed player parameter
	{
		x += xa * speed;
		y += ya * speed;
	}
};

int main()
{
	Player player;
	player.Move( 1, -1);  // Removed player parameter
	std::cin.get();
}
```

The code is now much cleaner, more readable, and easier to maintain.

## 4. Summary

Essentially, a *class* allows us to organize variables into a type and also add functions to operate on these variables. We have both the data and the functions that manipulate this data.

You can achieve what you can do with classes without using them, which is why C is still quite useful. It's just *syntax sugar* that makes the programmer's life easier.