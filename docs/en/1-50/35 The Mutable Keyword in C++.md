## 1. const

When discussing `mutable` in the context of `const`, it is clear that we are talking about something immutable, but in reality, it can be changed. It's as if `mutable` reverses the meaning of `const`.

```cpp
class Entity
{
private:
	std::string m_Name;
public:
	const std::string& GetName() const  // Promise read-only
	{
		return m_Name;
	}
};

int main()
{
	const Entity e;   // const objects cannot call non-const member functions, as the latter may modify the object
	e.GetName();
	std::cin.get();
}
```

We want to modify a variable within the object but do not want to change the object itself.
```cpp
class Entity
{
private:
	std::string m_Name;
	int m_DebugCount = 0;
public:
	const std::string& GetName() // Remove const to allow modification of m_DebugCount
	{
		m_DebugCount++;
		return m_Name;
	}
};

int main()
{
	const Entity e;
	e.GetName();                 // This won't compile
	std::cin.get();
}
```
This is where `mutable` comes into play:
```cpp
mutable int m_DebugCount = 0;
```

Now, the `const` method in the class can modify this member.

## 2. lambda
Lambdas are mostly used in `const` methods, but they can also be encountered in `lambda` expressions.
A `lambda` is like a disposable small function that you can write and assign to a variable, as done here.
```cpp
auto f = []() 
{
	std::cout << "Hello" << std::endl;
};
f();
```

If you want to pass parameters, you'll find that you can't modify variables captured by value.
```cpp
auto f = [=]() 
	{
		x++;        // Cannot modify
		std::cout << x << std::endl;
	};
```

You can achieve the result by using a local variable.
```cpp
int x = 8;
auto f = [=]() 
{
	int y = x;    // Create a local variable
	y++;
	std::cout << y << std::endl;
};
f();
```

### Using the `mutable` keyword
```cpp
int x = 8;
// Use the mutable keyword to allow modification of variables captured by value in the Lambda expression
auto f = [=]() mutable 
{
	x++;
	std::cout << x << std::endl;
};
f();
```

In the capture list of a Lambda expression, different capture modes can be used to specify how external variables are accessed. The following are the roles of different capture modes:

1. `[=]`: Capture by value
    
    - Using `[=]` means that the Lambda expression will capture all external variables by copying their values.
    - Inside the Lambda expression, you can access copies of these variables, but modifications to the copies will not affect the original variables.
    - Using capture by value ensures that the values of external variables remain unchanged during the execution of the Lambda expression.

2. `[&]`: Capture by reference
    
    - Using `[&]` means that the Lambda expression will capture all external variables by reference.
    - Inside the Lambda expression, you can directly access and modify these variables, and the modifications will directly affect the original variables.
    - Using capture by reference avoids creating copies of variables inside the Lambda expression, saving memory and copy overhead.

3. `[x]`: Capture specific variable
    
    - Using `[x]` means that only the specified variable `x` will be captured.
    - Inside the Lambda expression, you can access and modify the specified variable `x`, and the modifications will directly affect the original variable.
    - Using specific variable capture allows you to control the scope of external variable access within the Lambda expression.