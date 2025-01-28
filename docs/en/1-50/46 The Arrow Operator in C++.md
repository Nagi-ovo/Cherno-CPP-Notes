## 1. Using the Arrow Operator
If we have a pointer `ptr` of type `Entity`, we cannot directly call a method using `ptr.Print()`, because `ptr` is just a pointer, i.e., a numerical value (not an object, so we can't call methods on it).

What we can do is use the *arrow operator* instead of the more cumbersome method of dereferencing the pointer and then calling the method.
```cpp
class Entity
{
public:
	void Print() const { std::cout << "Hello!" << std::endl; }
};


int main()
{
	Entity e;
	e.Print();
	Entity* ptr = &e;
	ptr->Print();

	std::cin.get();
}
```

This arrow essentially dereferences the `Entity` pointer into a regular `Entity` class and then calls `Print`:
```cpp
Entity* ptr = &e;
//Entity& entity = *ptr;
(*ptr).Print();   //*ptr.Print(); won't work due to operator precedence; Print would be called first, then the entire result would be dereferenced
```

This is essentially a shortcut. Normally, we would need to manually dereference the pointer and then wrap it in parentheses. Now, we can just use an arrow. The same can be done with variables within the class.
```cpp
ptr->x = 2;  // There is a public int x member variable in the class
```

This is basically the default usage of the arrow operator, and you'll use it this way more than 90% of the time.
However, as an *Operator*, C++ actually allows you to overload it and use it in your own custom classes.

## 2. Overloading the Arrow Operator

Let's create a new scope pointer class:
```cpp
class ScopedPtr
{
private:
	Entity* m_Obj;
public:
	ScopedPtr(Entity* entity)
		: m_Obj(entity)
	{
		
	}

	~ScopedPtr()
	{
		delete m_Obj;
	}

};

// I can use it like this
int main()
{
	ScopedPtr entity = new Entity();
	
	std::cin.get();
}
```
If I want to call the `Print` function in the `Entity` class, how can I do that? I can't use `.`, but I could make `m_Obj` public or find some way to return `m_Obj`, but these methods are too messy. I want to be able to use it as if it were a heap-allocated `Entity`.
This is where overloading the arrow operator comes in:
```cpp
class ScopedPtr
{
......
public:
    ......
	Entity* operator->()
	{
		return m_Obj;
	}
};

int main()
{
	ScopedPtr entity = new Entity();
	entity->Print();  // Now it compiles and runs correctly

	std::cin.get();
}
```

## 3. Bonus
Finally, a little bonus.
```cpp
struct Vector3
{
	float x, y, z;
};
```
I have a struct `Vector3`, and I want to get the offsets of `x`, `y`, and `z` (`x` is the first item in the struct, so its offset is 0; `y` is the second item, and since a `float` is 4 bytes, its offset is 4 bytes; `z`'s offset is 8 bytes).

We can use the arrow operator to achieve this. I want to access these variables, but not through a valid memory address—instead, starting from address 0.
```cpp
int offset =(int) & ((Vector3*)0)->x; // x,y,z
std::cout << offset << std::endl;  // 0,4,8
```
1. `(Vector3*)0` converts the integer `0` into a pointer of type `Vector3`. This operation is typically used to get the offset of a member of a struct or class that a null pointer points to. `((Vector3*)nullptr)`
2. `&((Vector3*)0)->x` gets the address of the `x` member of the `Vector3` type object that the null pointer points to. Since a null pointer cannot access member variables, this is only used to get the offset of the member variable.
3. `(int)` converts the obtained member variable address into an integer type so that it can be output to the stream.