# Copying and the C++ Copy Constructor

## 1. Copying

**Copying** refers to the act of duplicating data or memory. When we want to copy an object, a *primitive*, or a piece of data from one location to another, we end up with two copies. It's important to avoid unnecessary copying because it can waste performance.

Understanding how copying works in C++, how to prevent it, or how to avoid it when you don't want it, is crucial for mastering the language and writing efficient and correct C++ code.

```cpp
int a = 2;
int b = a;
```

Here, a copy of `a` is created. `a` and `b` are two independent variables with different memory addresses. So if we change `b` to 3, `a` remains 2.

The same logic applies to classes.

Copying pointers is different because they point to the same content. Modifying `b` will also affect `a`.

```cpp
struct Vector2
{
	float x, y;
};

int main()
{
	Vector2* a = new Vector2();
	Vector2* b = a;
	b->x = 5;
	std::cout << "x:" << a->x << "y:" << a->y << std::endl;  // x:5,y:0
}
```

So, except for references, whenever you write code where one variable is assigned to another, you are always copying.

```cpp
#include <iostream>
#include <string>

class String
{
private:
	char* m_Buffer;  // Pointer to the character buffer
	unsigned int m_Size;  // Holds the size of the string
public:
	String(const char* string)
	{
		m_Size = strlen(string);
		m_Buffer = new char[m_Size];  // Need to leave space for the null terminator, intentionally omitted here
		/*for (int i = 0; i < m_Size; i++)
			m_Buffer[i] = string[i];*/
		// You could use a simple for loop to fill it, but here we use a more concise method
		memcpy(m_Buffer, string, m_Size);
	}
	friend std::ostream& operator<<(std::ostream& stream, const String& string); // Friend function to allow access to private members
};


std::ostream& operator<<(std::ostream& stream,const String& string )
{
	stream << string.m_Buffer;
	return stream;
} // Overload the output operator to output the `String` object to the `std::ostream` stream.

int main()
{
	String string = "Cherno";
	std::cout << string << std::endl;

	std::cin.get();
}
```

You can see that the output contains many random characters because the null terminator is missing.
![](./storage%20bag/Pasted%20image%2020230711210743.png)

```cpp
m_Buffer = new char[m_Size + 1 ]; // Add space for the null terminator, or use strcpy which we'll learn later
m_Buffer[m_Size] = 0; // Add the null terminator
```

Now it can correctly output "Cherno".
Let's go back and look at the `String` class code. Is there still a problem?

The answer is that there is a memory leak.

```cpp
m_Buffer = new char[m_Size + 1 ];
```

When we allocate this `new char`, there is no corresponding `delete`. Of course, if you use smart pointers or `vector`, you don't need to `delete`.
So we modify the destructor of the `String` class:

```cpp
~String()
{
	delete[] m_Buffer;
}
```

Next, we copy this string and try to print it:

```cpp
int main()
{
	String string = "Cherno";
	String second = string;

	std::cout << string << std::endl;
	std::cout << second << std::endl;

	std::cin.get();
}
```

Oops, the program crashes after outputting the string and pressing enter at `cin.get()`. The callstack is also unclear, so what caused the program to crash?
![](./storage%20bag/Pasted%20image%2020230711212436.png)

When we copy this `String`, what C++ automatically does for us is that it copies all the class member variables, which make up the class (the memory space of the instance). It consists of a `char*` and an `unsigned int`, and it copies these values to a new memory address, which contains this `second` string.

## 2. Shallow Copy

Now the problem arises. There are two `String` objects in memory because they were directly copied. This type of copying is called a *shallow copy*. What it does is copy the `char*`. The two `String` objects in memory have the same `char*` value, meaning they share the same memory address. This `m_Buffer` memory address is the same for both `String` objects, so the program crashes because when we reach the end of the scope, both `String` objects are destroyed, the destructor is called, and `delete[] m_Buffer` is executed twice. The program tries to free the same memory block twice. This is why the program crashes—because the memory has already been freed, it's no longer ours, and we can't free it again.
![](./storage%20bag/Pasted%20image%2020230711213515.png)

Now suppose we want to modify the `second` string, not completely, but just change the letter 'e' to 'a', making it "Charno".

```cpp
second[2] = 'a'; // We also need to overload the operator

class String
{
.......
char& operator[](unsigned int index)
{
	return m_Buffer[index];
}
......
}
```

Why do we end up with two "Charno"s?
![](./storage%20bag/Pasted%20image%2020230711214022.png)

What we really need to do is allocate a new `char` array to store the copied string. What we're doing now is copying the pointer, so both string objects point to the exact same memory buffer. Changing one affects the other because they point to the same memory block. Or when we delete, it deletes both because they point to the same memory block.

## 3. Deep Copy (Using the Copy Constructor)

We want the second string to have its own pointer, to have its own unique memory block.
The way we can achieve this is by performing something called a *deep copy*, which means we actually copy the entire object, not just the shallow copy we mentioned earlier: what the object is made of. A shallow copy doesn't go into the content of the pointer or where the pointer is pointing, nor does it copy it.

A deep copy, by definition, copies the entire object. Here, we use the *copy constructor*.

The copy constructor is a constructor that gets called when you copy a second string. When you assign one string to another object that is also a string (when you try to create a new variable and assign it another variable of the same type), you copy this variable, which is what the copy constructor does.

C++ automatically provides a copy constructor for you:

```cpp
class String
{
......
String(const String& other);
......
}
```

What it does is a memory copy, shallow copying the memory of the `other` object into these member variables.
So if we were to write it ourselves, it might look like this:

```cpp
String(const String& other)
	: m_Buffer((other.m_Buffer)), m_Size(other.m_Size){};

// More intense way
String(const String& other)
{
	memcpy(this, &other, sizeof(String));
}
```

This is the default copy constructor provided by C++.

If we decide we don't need a copy constructor and want to disallow copying, we can declare the copy constructor as `delete`:

```cpp
String(const String& other) = delete;
```

This is what [unique_ptr](44%20SMART%20POINTERS%20in%20C++.md#^f2eddc) does.

But here, we want to define our own copy constructor:

```cpp
String(const String& other)
	: m_Size((other.m_Size))
{
	m_Buffer = new char[m_Size+1];
	memcpy(m_Buffer, other.m_Buffer, m_Size + 1);
}
```

We get the desired result, and the program terminates successfully.
![](./storage%20bag/Pasted%20image%2020230711220047.png)

Add a function to print, and the result is normal, but actually, we don't need to perform this copy.
Add an indicator (output a string) in the copy constructor:
![](./storage%20bag/Pasted%20image%2020230711220355.png)
It seems like we only did one copy, but when we pass it to this function, we actually did 2 additional copy operations. Each time the destructor is called to delete the memory, it's completely unnecessary.
What we really want to do is to pass the existing string directly into this `PrintString` function. We know we don't need to get another copy, we can directly reference the existing string.

We can achieve this through *reference*.
![](./storage%20bag/Pasted%20image%2020230711220922.png)
Only when we assign the second object to the string do we have one copy.

If we suddenly decide that we still want to copy in the `PrintString` function, we just need:

```cpp
void PrintString(const String& string )
{
	String copy = string;
	std::cout << string << std::endl;
}
```

What I want to tell you is that you should always pass objects by const reference. We'll delve deeper into its optimization later (because in some cases copying might be faster). But in any case, using const references is better for basic usage.
Always pass objects by const reference because you can decide inside your function whether you want to copy, but there's no reason to copy everywhere, as it will slow down your program.
Important things to say three times: when you pass a string, whether it's your own `String` class or the standard library's `String` (`std::string`), always pass it by const reference. Besides reducing copies, there are other benefits, which we'll discuss later.