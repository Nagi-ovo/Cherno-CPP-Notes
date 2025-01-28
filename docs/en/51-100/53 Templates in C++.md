## 1. What Are Templates

*Templates* in C++ are more powerful than generics in other languages. Templates are somewhat like *macros* and can be used to do almost anything, whereas generics are heavily constrained by the type system and other factors.

Templates allow you to define a blueprint that the compiler will use to generate code based on your needs. For example, when writing a function, you can use templates to create a *blueprint*. When you decide to call this function, you can specify particular parameters that determine the actual code to be inserted into the template.

```cpp
#include <iostream>
#include <string>

void Print(int value)
{
	std::cout << value << std::endl;
}

void Print(std::string value)  // Function overloading
{
	std::cout << value << std::endl;
}

int main()
{
	Print(5);
	Print("Hello");
	Print(4.3f);   // If we want to print a float, we need to overload the function again
	std::cin.get();
}
```

We end up manually defining three overloaded Print functions. What if we only need to define this function once?

## 2. Creating Templates

```cpp
template<typename T>  // Typically called T
void Print(T value)
{
	std::cout << value << std::endl;
}
```

![](./storage%20bag/Pasted%20image%2020230714153728.png)

`template` indicates that a template is being defined, which will be evaluated at compile time. Therefore, this is not an actual function; it only gets created when we actually call it.

`<typename T>` is the template parameter. In this example, we use `typename` as the type of the template parameter, and `T` as the name, which is essentially the parameter name for the template and can be replaced by the type that appears in the example.

```cpp
Print<int>(5.5f); // You can specify the type; the result here will be 5
```

To reiterate, a template is only created when it is called; otherwise, it doesn't exist at all. You can even have syntax errors inside it, and as long as it's not called, it won't affect compilation. (This is how it was in the video, but currently, errors in templates will affect compilation even if they are not called.)

In reality, the compiler fills in the blanks for the template:

```cpp
template<typename T>
void Print(T value)
{
	std::cout << value << std::endl;
}

void Print(int value)  // Equivalent to copying and pasting this function, then replacing T with int to get an actual function
{
	std::cout << value << std::endl;
}
```

Templates are not limited to classes or functions; you can create an entire class based on a template. In fact, a large part of the C++ Standard Template Library (STL) is built entirely using templates.

Here's an example where we can't use a type as a template parameter:

```cpp
class Array // I want an array whose size is determined at compile time
{
private:
	int m_Array[];
};
```

You can't directly input a variable like `size` here because this is a stack-allocated array, so its size must be known at compile time. Templates are evaluated at compile time.

```cpp
template<int N>
class Array
{
private:
	int m_Array[N];
public:
	int GetSize() const { return N; }
};

int main()
{
	Array<5> array;
	std::cout << array.GetSize() << std::endl; // 5

	std::cin.get();
}
```

As you can see, we're not limited to using types; we can use integers or other data types to specify how we want to generate a class or an entire class.

Let's go further. I want the type of the array to be variable as well, so I can specify the type that the array actually contains at compile time. I can add another template parameter.

```cpp
template<typename T,int N>
class Array
{
private:
	T m_Array[N];
public:
	int GetSize() const { return N; }
};

// Usage
Array<int,5> array0;
Array<std::string,50> array1;
```

You can see that we've created a class that can be automatically generated. This is actually very similar to how the standard array class in the C++ Standard Template Library works (it has two template parameters: type and size). This is somewhat like *meta programming* in C++, where instead of programming at runtime, we're programming at compile time.

## 3. Where to Use Templates? Where Not to?

This section is entirely subjective and for reference only.

Many game studios or software companies actually prohibit the use of templates. However, templates are very useful, such as in logging systems or other scenarios where you want to log every possible type. Do you really want to overload the function for each type? You can use templates to automate this, meaning you can let the compiler write code for you based on some rules.

This is to say, you can delve into using templates to do some great things, but if your templates become very complex and you start generating an entire meta-language, you might be going too far. There's a balance here. When templates become too complex, no one can understand what they're doing, and you'll spend a lot of time figuring out which code has been compiled and why your template isn't working. This indicates that you've gone too far.

Cherno's opinion is: doing some things manually, writing code yourself, will actually benefit you and your team more than trying to create massive templates that magically do everything for you. So templates should not be completely banned, but they should not be overused either. For example, logging systems and material systems in game engines will definitely use templates. When you have a uniform buffer that can contain various types, templates are very useful to some extent.