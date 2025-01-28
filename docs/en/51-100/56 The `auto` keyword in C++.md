There is a way to allow C++ to automatically deduce the type of data, whether it is when creating and initializing variable data, or when assigning one variable to another.

## 1. The `auto` Keyword

It can automatically deduce that `b` is also of type `int`.
![](./storage%20bag/Pasted%20image%2020230718191950.png)

Even the type of `a` can be deduced using `auto`:
![](./storage%20bag/Pasted%20image%2020230718192644.png)

So the question arises, with `auto`, do I still need to write the type? Can I use it everywhere?

This also comes down to a matter of programming style. At the same time, you need to consider the advantages and disadvantages of this programming style.

## 2. Usage Example

```cpp
std::string GetName()
{
	return "Cherno";
}

int main()
{
	std::string name = GetName();

	char a = 'a';                   // If it's just a simple assignment, writing the type makes it clearer

	std::cin.get();
}
```

Here, I can set the type of `name` to `auto`:

```cpp
auto name = GetName();
```

This way, if the *API* changes, for example, if the return type of `GetName` is changed to `char*`, the client side does not need any changes. However, the downside is that I won't know that the API has changed, and it might break code that depends on a specific type.

## 3. When is it appropriate to use `auto`?

```cpp
int main()
{
	std::vector<std::string> strings;
	strings.push_back("Apple");
	strings.push_back("Orange");

	for (std::vector<std::string>::iterator it = strings.begin();
		it != strings.end();it++)
	{
		std::cout << *it << std::endl;
	}

	std::cin.get();
}
```

The type of the *iterator* in the code is too long, and it can be directly replaced with `auto` for better readability:
![](./storage%20bag/Pasted%20image%2020230718194607.png)

Another example:

```cpp
class Device{};

class DeviceManager
{
private:
	std::unordered_map<std::string, std::vector<Device*>> m_Devices;
public:
	const std::unordered_map<std::string, std::vector<Device*>>& GetDevices() const
	{
		return m_Devices;
	}
};

int main()
{
	DeviceManager dm;
	const std::unordered_map<std::string, std::vector<Device*>>& devices = dm.GetDevices();
}
```

The type here is quite large, and what can be done is to use an *alias*:

```cpp
using DeviceMap = std::unordered_map<std::string, std::vector<Device*>>;
	DeviceManager dm;

// or

typedef std::unordered_map<std::string, std::vector<Device*>> DeviceMap;
```

Then it can be called directly, and even the `using` part can be moved into the `DeviceManager` class:

```cpp
const DeviceMap& devices = dm.GetDevices();
```

This way, I get a concise and more meaningful type.

But if I don't want to use these methods, I can use `auto` to help myself:
![](./storage%20bag/Pasted%20image%2020230718195835.png)

However, it should be noted that `auto` does not handle references, so don't omit the `&` and cause a copy.

These are two scenarios in the real world where it might be more appropriate to use `auto`, such as when your variable type is very long. If the variable type is just an `int` and you still use `auto`, it will only reduce the readability of the code, and in my opinion, there is no benefit.

When entering more complex code sets, including templates, the situation is quite complicated, and you have to use `auto` because you don't know what the type is.