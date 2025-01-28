Why **I personally** don't use `using namespace std`, this is just an opinion.

## 1. What is `using namespace`

As in the code above, which uses a lot of standard library content, if you add the following at the beginning of the code:

```cpp
using namespace std;
```

You can directly write `vector`, `find_if`, etc., making the code look cleaner.  
You can also limit it to a scope, for example, writing it at the beginning of the `main` function, so that calls to the standard library within the `main` function don't need to be prefixed with `std::`.

So `using namespace` can be very useful, especially if you are dealing with long namespaces, or if you have your own namespace where all the symbols in your project files are within this namespace, you can use this.

But **I personally** don't like `using namespace std`.

## 2. Why I don't like it

At first glance, the code looks cleaner, but if you look at the original code, you can easily identify the use of the C++ Standard Template Library (with the `std` prefix). If `using namespace std` is used, it becomes relatively harder to distinguish. If you also use the *snake case* naming convention (like `find_if`) that the standard library prefers, it becomes difficult to tell whether it's from `std` or not.

Let me show you a real-life example. Cherno used to work in the Frostbite Engine department at EA, where they used EASTL (a replacement for C++ STL), which uses the `eastl` namespace. If you just write `vector`, how do I know if it's `eastl::vector` or `std::vector`?

```cpp
namespace apple{

	void print(const std::string& text)
	{
		std::cout << text << std::endl;
	}
}

using namespace apple;
int main()
{
	// apple::print("Hello");
	print("Hello");

```

Now there's a new namespace `orange`, which also has a `print` function, but it prints the reversed content.

```cpp
namespace orange{
	void print(const char* text)
	{
		std::string temp = text;
		std::reverse(temp.begin(),temp.end());
		std::cout << temp << std::endl;
	}
}

using namespace apple;
using namespace orange;

int main()
{
	print("Hello");
```

So which one will be called here?

![](./storage%20bag/Pasted%20image%2020230721134655.png)

This is not because `orange` is after `apple`, but for another reason. "Hello" is actually a `const char[]` array, not a `string`. If only the `apple` namespace is used, an [implicit conversion](40%20Implicit%20Conversion%20and%20the%20Explicit%20Keyword%20in%20C++.md#^cde452) will occur in `apple::print()`, converting the `const char` array to a `string` object. But after introducing the `orange` namespace, `orange::print()` has a better match because its parameter is exactly a `const char*`, requiring no implicit conversion.

If we don't use `using namespace`, but simply include another library `apple::print()`, such runtime errors can be avoided.

Another thing to absolutely avoid is using `using namespace` in header files. Never do this, as it applies these namespaces to places you didn't intend to use them. Who knows what it might include? It's very difficult to track in any large project, so **never use `using namespace` in header files!**