[85 Lvalues and Rvalues](85%20lvalues%20and%20rvalues%20in%20C++.md) After a few sections, we finally arrive at move semantics.

We already know what rvalues are and what rvalue references are. Now, let's take a look at one of their biggest uses—move semantics.

## 1. Move Semantics

Move semantics essentially allow us to move objects, which was impossible before C++11 because C++11 introduced rvalue references, which are essential for move semantics.

The basic idea is that when writing C++ code, there are many situations where we don't need or want to copy an object from one place to another, but we have to do so because it's the only way to achieve the goal. For example, when passing an object to a function, the function must take ownership of that object, and the only option is to copy it. Similarly, when returning an object from a function, we still need to create that object in the function and then return it (copying the data).

> However, now there is "Return Value Optimization" (RVO) that can optimize the return value part, but in the first example, we still need to construct a temporary object in the current stack frame and then copy it to the function we are calling, which is not ideal.

This is where move semantics come into play: if we can move the object instead of copying it, the performance will be better.

```cpp
#include <iostream>

class String
{
public:
	// Default constructor
	String() = default;

	// Constructor that initializes from a C-string
	String(const char* string)
	{
		printf("Created!\n");
		// Calculate the length of the string
		m_Size = strlen(string);
		// Dynamically allocate memory to store the string content
		m_Data = new char[m_Size];
		// Copy the content from the input string to the newly allocated memory
		memcpy(m_Data, string, m_Size);
	}

	// Copy constructor
	String(const String& other)
	{
		printf("Copied!\n");
		m_Size = other.m_Size;
		m_Data = new char[m_Size];
		memcpy(m_Data, other.m_Data, m_Size);
	}

	// Destructor, releases the dynamically allocated memory
	~String()
	{
		delete[] m_Data;
	}

	// Print the string content
	void Print()
	{
		for (uint32_t i = 0; i < m_Size; i++)
			printf("%c", m_Data[i]);

		printf("\n");
	}

private:
	char* m_Data;      // Pointer to store the string content
	uint32_t m_Size;   // Size (length) of the string
};

class Entity
{
public:
	// Constructor that takes a String parameter to initialize the name
	Entity(const String& name)
		:m_Name(name) {}

	// Print the entity's name
	void PrintName()
	{
		m_Name.Print();
	}

private:
	String m_Name;     // The entity's name
};

int main()
{
	// Create an Entity object named "Cherno"
	Entity entity(String("Cherno"));
	// Print the entity's name
	entity.PrintName();

	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230812215614.png)

> As we can see from the print result, our data was copied.

We first create it in the scope of the main function, then pass it to the Entity's constructor, and then copy it to `m_Name`. Why can't we directly allocate it in the private member `String m_Name` of Entity? We can't do this unless we can access the string and manually manipulate it. But we can allocate it in the main function and then move it into this space, which is where the *move statement* comes into play.

In this example, we need to write a move constructor, which is similar to the copy constructor, except that it takes an rvalue (temporary value) as a parameter.
After using it, when we call it in main, the parameter in `Entity entity(String("Cherno"));` is not an lvalue; it is not assigned to anything, but is just a parameter of the Entity constructor.

```cpp
// Move constructor
String(String&& other) noexcept // Ensure that this constructor does not throw any exceptions
{
    printf("Moved!\n");
    // Copy the size and data pointer from the source object
    m_Size = other.m_Size;
    m_Data = other.m_Data; // Directly assign the source object's data pointer to the current object

    // Put the source object into a valid but indeterminate state
    other.m_Size = 0;      // Set the source object's size to 0
    other.m_Data = nullptr;// Set the source object's data pointer to nullptr, ensuring that the source object will not delete this data block
}

// Entity class constructor that takes an rvalue reference to a String object
Entity(String&& name)
    : m_Name(name) {}  // Directly pass the rvalue-referenced name to m_Name. Since m_Name's constructor also supports rvalue references, it will call String's move constructor.

```

![](./storage%20bag/Pasted%20image%2020230812222425.png)

> Indeed, the newly written Entity constructor was called and the result was printed, but an assignment still occurred, indicating that the String's copy constructor was called instead of the move constructor.

To make it use the move constructor, we must explicitly convert it to a temporary object:

```cpp
Entity(String&& name)
    : m_Name((String&&)name) {}

// In practice, it's better to use the more elegant std::move:

Entity(String&& name)
	:m_Name(std::move(name)) {}  // Essentially the same as above, will be explained in detail in the next section
```

![](./storage%20bag/Pasted%20image%2020230812222924.png)

> Now we have successfully allocated memory only once and managed to move the string into the Entity class's member. We didn't use the copy constructor to allocate a new memory block and then copy; we just moved it. This is awesome.

## 2. "Stealing" Memory

(Mentioned in the [85 Lvalues and Rvalues](85%20lvalues%20and%20rvalues%20in%20C++.md#^388d93) section)

Here, the move constructor indeed "steals" the memory of the `other` object. It directly takes over the memory pointed to by `other.m_Data` instead of allocating new memory and copying the content. This makes the move operation generally faster and more efficient than the copy operation because it avoids additional resource allocation and copying.

Afterward, the members of the original object `other` are set to default values (e.g., `nullptr`), ensuring that its destructor does not release the resources that have already been transferred. This is a typical implementation of move semantics.