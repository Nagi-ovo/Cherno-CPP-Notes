## 1. const

I like to call `const` a "fake keyword" because it doesn't actually do much when generating code.  
It's somewhat like the visibility of classes and structs—a mandatory rule for developers to keep the code clean.  
Essentially, `const` is a promise you make that certain things are immutable and won't change. However, it's just a promise, and you can bypass or break it, just like in real life.

![](./storage%20bag/Pasted%20image%2020230705145201.png)  
`*a = 2` refers to the dereferencing mentioned earlier.

```cpp
const int* a = new int;
// Equivalent to int const* a = new int;
*a = 2;                           // Error: const prevents you from modifying the content pointed to by a
a = (int*)&MAX_AGE;
```

```cpp
int* const a = new int;
*a = 2;
a = (int*)&MAX_AGE;               // Error: You can change the content pointed to by a, but you cannot reassign the pointer itself to point to something else
```

```cpp
const int* const a = new int;      // Neither the content pointed to by a nor the pointer itself can be changed
*a = 2;
a = (int*)&MAX_AGE;
```

Key point: Pay attention to whether `const` is on the left or right side of `*`.

## 2. Using const in Classes and Methods

```cpp
class Entity
{
private:
	int m_X, m_Y;
public:
	int GetX() const { // Promises that this method will not modify the class; it's a read-only method
		m_X = 2;       // Cannot modify
		return m_X;
	}
};
```

`int* m_X, m_Y` means `m_Y` is still an `int` type. To make both pointers, you need to write `int* m_X, *m_Y`.

A `const` object cannot call non-`const` member functions because the latter might modify the object.

You can mark a variable as `mutable int var`, allowing it to be modified even within a `const` method.