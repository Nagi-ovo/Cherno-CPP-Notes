# C++ Object Lifetime (Stack Scope Lifetime)
Review [38 How to CREATE_INSTANTIATE OBJECTS in C++](38%20How%20to%20CREATE_INSTANTIATE%20OBJECTS%20in%20C++.md)

## 1. Scope
Think of the stack as placing a book on a bookshelf. The variables (what's written in the book) declared within this scope (the book) will be discarded once the scope ends. Every stack-based variable declared in the book, all objects created on the stack, will disappear.

```cpp
class Entity
{
private: 
	int x;
};
```
Here is a variable initialized on the stack, not allocated on the heap. This variable is also within the scope of the class, meaning that when the class goes out of scope, the variable will also disappear.

```cpp
class Entity
{
public:
	Entity()
	{
		std::cout << "Created Entity" << std::endl;
	}

	~Entity()
	{
		std::cout << "Destroyed Entity" << std::endl;
	}

};

int main()
{
	{
		Entity e;   // Written like this, it is not created on the heap, but on the stack
	}               // The default constructor will be called

	std::cin.get();
}

// Output
// Created Entity
// Destroyed Entity
```
Changed to heap allocation:
```cpp
int main()
{
	{
		Entity* e = new Entity();
	}   // Skips this scope

	std::cin.get();
}

// Output
// Created Entity
```

Remember, if you create a variable on the stack, it will disappear when it goes out of scope.

Let's look at another example:
```cpp
int* CreateArray()
{
	int array[50];
	return array;
}
```
Is this legal?
No, because we did not allocate it on the heap, as we did not use `new`. We only declared it on the stack. When we return a pointer to it, it will return a pointer to stack memory, which will be cleared when we leave the scope.

So if you write it like this, it will fail.
```cpp
int main()
{
	int* a = CreateArray();
}
```
If you want to write a function like this, you basically have two options.
You can allocate the array on the heap, ensuring its lifetime will persist.
```cpp
int* CreateArray()
{
	int* array = new int[50];
	return array;
}

int main()
{
	int* a = CreateArray();
}
```
Or you can copy the data created here to a variable that exists outside the stack scope.
```cpp
void CreateArray(int* array)
{
	// fill our array
}

int main()
{
	int array[50];
	CreateArray(array);
}
```
Here we are just passing a pointer, so no allocation is done.

Therefore, creating an array locally is a typical mistake.

So how can we make this automatic destruction of stack variables useful?

## 2. Scope Pointer
It is essentially a class, a wrapper for a pointer, which allocates the pointer upon construction and deletes the pointer upon destruction. So we can automate this `new` and `delete`.

This is a basic *scoped pointer* (class) ^58d90d
```cpp
class ScopedPtr
{
private:
	Entity* m_Ptr;
public:
	ScopedPtr(Entity* ptr)
		: m_Ptr((ptr))
	{
	}

	~ScopedPtr()
	{
		delete m_Ptr;  
	}
};

int main()
{
	{
		ScopedPtr e = new Entity(); 
	}
}


// Output
// Created Entity
// Destroyed Entity
```
This ScopedPtr class is allocated on the stack, meaning that if e is deleted, in the destructor, it will `delete` the wrapped Entity pointer. Even though we used `new` for heap allocation, the destruction is completed.

This is the most basic thing that a *smart pointer*: *unique_ptr* does.

Automatic construction and destruction, these stack-based variables are very useful as they are destroyed when they go out of scope.

### Timer
Suppose you want to calculate the time within your benchmark scope, you can write a timer class that starts the timer when the object is constructed, and stops the timer when the result is printed, i.e., when the timer object is destroyed. This way, you only need to write one line of code at the beginning of the function, and the entire scope will be timed. And you never need to manually call the timer to stop, because once it goes out of scope, it will automatically call and stop.

### Mutex Locking
If you want to lock a function so that multiple threads can access it simultaneously without crashing, you can have an automatic scope lock that locks it at the beginning of the function and unlocks it at the end of the function.