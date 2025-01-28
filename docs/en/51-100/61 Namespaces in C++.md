## 1. Why Use Namespace

```cpp
void print(const char* text)
{
	std::cout << text << std::endl;
}

void print(const char* text)
{
	std::string temp = text;
	std::reverse(temp.begin(),temp.end());
	std::cout << temp << std::endl;
}
```

Here we have two functions with the same function signature. The *symbols* for these two functions are identical, which would result in linking or compilation errors if placed in the same file. However, if we indeed want two `print` functions, or if we are using a library that already defines a `print` function but we want our own version, we need a way to differentiate them.

C language does not have namespaces. For example, when using the GLFW library (a C-based OpenGL library), every function name is prefixed with `GLFW`.

Thus, the primary purpose of a *namespace* is to avoid naming conflicts.

Namespaces can be nested in a single line, which can improve readability when dealing with multiple layers of nesting:

```cpp
namespace apple { namespace functions {

	void print(const char* text)
	{
		std::cout << text << std::endl;
	}
} }
```

The `::` operator is the namespace resolution operator. Classes are also a form of namespace, which is why you use `::` to access members like nested classes within another class.

You can also selectively introduce functions:
![](./storage%20bag/Pasted%20image%2020230723174600.png)

You can also alias namespaces:
![](./storage%20bag/Pasted%20image%2020230723175142.png)

It is advisable to limit the scope of a namespace to a small area and avoid placing it in header files.