This section discusses a **design pattern** in C++, namely the _Singleton_ pattern.

## 1. What is a Singleton

A Singleton is a single instance of a class. If we don't intend to instantiate multiple instances of a particular class, why bother creating a class for it in the first place?

Singletons are very useful when we want to have functionality that applies to some global dataset and we just want to reuse it.

For example, a random number generator class: we only want to query it and get a random number, without needing to instantiate it multiple times. Another example is a renderer, which is typically a very **global** thing. Usually, there won't be multiple instances of a renderer; instead, all rendering commands are submitted to a single renderer.

What we might want is to be able to call certain functions by using the class as a namespace, which is where the Singleton pattern can get a bit messy. Essentially, a Singleton class can function like a namespace, but there's no requirement for it to behave like a regular class.

So, in C++, a Singleton is just a way to organize a bunch of global variables and static functions.

## 2. Using a Singleton

```cpp
class Singleton
{
public:
	// Delete the copy constructor
	Singleton(const Singleton&) = delete;

	// Public static method to get the Singleton instance
	static Singleton& Get()
	{
		return  s_Instance;
	}

	// An example method
	void Function() {};

private:
	// Private constructor
	Singleton() {};

	// Static member for the Singleton instance
	static Singleton s_Instance;
};

// Initialize the Singleton instance
Singleton Singleton::s_Instance;

int main()
{
	Singleton::Get(); // Get the Singleton instance
	Singleton::Get().Function(); // Call a method through the Singleton instance
}

```

This is just a lazy Singleton pattern, which is not suitable for multi-threaded use. Let's look at a more practical example, implementing a Singleton for a random number generator:

```cpp
class Random
{
public:
	Random(const Random&) = delete;
	static Random& Get()
	{
		return  s_Instance;
	}
	float Float() { return m_RandomGenerator; };
private:
	Random() {};
	float m_RandomGenerator = 0.5f;  // Just for demonstration, not actually generating random numbers
	static Random s_Instance;
};

Random Random::s_Instance;

int main()
{
	float number = Random::Get().Float();
	std::cout << number << "\n";  // 0.5
}
```

Finally, to call this Singleton, we need to access it like a namespace. How can we remove the "Get()" in the middle?

![](./storage%20bag/Pasted%20image%2020230805161556.png)

> You can use this indirect approach. Once all of this is inlined by the compiler, there won't be any performance loss from all these function calls.

Lastly, the Get function in the current code. The way we've written it means we need to have a static instance in the class members, and then define it in some translation unit, which is a bit cumbersome. A better approach is to move the static declaration into the static function:

```cpp
class Random
{
public:
	Random(const Random&) = delete;
	static Random& Get()
	{
		static Random s_Instance; // Static variable in static memory
		return  s_Instance;
	}
	static float Float() { return Get().IFloat(); }
private:
	float IFloat() { return m_RandomGenerator; };
	Random() {};
	float m_RandomGenerator = 0.5f;
	// static Random s_Instance;
};
// Random Random::s_Instance;
int main()
{
	float number = Random::Float();
	std::cout << number << "\n";
}
```

> The effect of this is that once the Get function is called for the first time, it will instantiate the Singleton, and for the rest of the time, it will just reference the static memory. The code is cleaner.

You might also want to delete the copy operator and perform further cleanup:

```cpp
Random& operator=(const Random&) = delete; // Delete the assignment operator
```

> For related knowledge, you can refer to [41 OPERATORS and OPERATOR OVERLOADING in C++](41%20OPERATORS%20and%20OPERATOR%20OVERLOADING%20in%20C++.md)

But the course simplifies the operation for better understanding.

## 3. Why Not Use a Namespace

```cpp
namespace RandomClass
{
	static float s_RandomGenerator = 0.5f;
	static float Float() { return s_RandomGenerator; }
}
```

> This achieves essentially the same effect, but you can't directly use class-specific features like public and private. Although you can effectively hide the implementation by only including the declaration of the Float function in the header file and then implementing the function and static variable in another cpp file.

So, there's no real downside to using a class to implement a Singleton. It makes your code more organized, not to mention that using a `namespace` loses the ability to assign it to a variable, whereas a class can.