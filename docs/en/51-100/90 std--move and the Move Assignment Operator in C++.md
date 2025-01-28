After the previous section [89 Move Semantics in C++](89%20Move%20Semantics%20in%20C++.md), I have a basic understanding of the key points and all the fundamental knowledge of move semantics. Move semantics allow an object to be moved to another object, but it hasn't yet covered two crucial parts: `std::move` and the _move assignment operator_, which is an assignment operator used when we want to move an object into an existing object (not constructing a new object).

## 1. std::move

In the code from the previous section, using `std::move` allows us to transfer the temporary variable `name` to `m_Name`, a permanent storage location (class member):

```cpp
	Entity(String&& name)
	//	:m_Name(name) {}
		:m_Name(std::move(name)) {}
```

Creating a new `String`:

```cpp
String string = "Hello";
String dest = string; // Copying the string to a new variable, not moving
```

To move, we clearly need the move constructor of `Entity`. To use it, we need to ensure that the passed string becomes **temporary**:

```cpp
String string = "Hello";
// 	String dest = (String&&)string;
// 	String dest((String&&)string);
// This is not the most elegant and universally applicable method. Therefore, a more flexible function can be used, which can determine the type of input at compile time using auto
String dest(std::move (string));
```

![](./storage%20bag/Pasted%20image%2020230812225450.png)

> It can be seen that it returns an rvalue reference type, implemented in a well-templated manner, correctly handling all types, including constants, etc.

Here, any method creates a new object, thus invoking the move constructor, which leads to the **move assignment operator**.

## 2. Move Assignment Operator

The assignment operator is only called when we assign a variable to an existing variable, for example:

```cpp
String dest(std::move (string));
dest = std::move(string);
```

> The operator actually works like a function, so calling the = operator here is like having an assign function dest.assgin(std::move(string)).

The move assignment operator looks very similar to the move constructor:

```cpp
// Move assignment operator
String& operator=(String&& other) noexcept
{
    printf("Moved!\n");

    // Check for self-assignment, ensuring not assigning the object to itself
    if (this != &other)
    {
        // Delete the resources currently held by the object
        delete[] m_Data; // **Key point** Because we are overwriting the original object, delete memory to prevent memory leaks

        // "Steal" resources from the "other" object to the current object
        m_Size = other.m_Size;
        m_Data = other.m_Data;

        // Leave the "other" object in a valid but undefined state
        other.m_Size = 0;
        other.m_Data = nullptr;
    }

    // Return *this to support chain assignment
    return *this;
}

```

Testing the call:

```cpp
int main()
{
	String apple = "Apple";
	String dest;

	std::cout << "Apple: ";
	apple.Print();
	std::cout << "Dest: ";
	dest.Print();

	dest = std::move(apple);

	std::cout << "Apple: ";
	apple.Print();
	std::cout << "Dest: ";
	dest.Print();

	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230812233014.png)

> It can be seen that the resources of `apple` are "stolen" by `dest`. We essentially transferred the ownership of the entire character array without doing any copying or deallocation.

In summary, the move assignment operator is something you want to include in your class when you include a move constructor, because you might want to move an object into an existing variable. It is basically part of the **Rule of Five**, which includes the new move semantics.

> C++ Rule of Three: If you need a destructor, you must need a copy constructor and copy assignment operator;
> C++ Rule of Five: To support move semantics, it adds the move constructor and move assignment operator.

And `std::move` is what you do when you want to convert an object into a temporary object, in other words, if you need to turn an existing variable into a temporary variable, you can mark it, indicating that you can steal resources from this specific variable, allowing us to perform moves on existing variables through operations.

It's important to note that `std::move` itself does not perform any moving; it merely reinterprets the object to make it usable as an rvalue. The actual moving behavior is performed by specific move constructors or move assignment operators, which are called when they receive an object marked as an rvalue.