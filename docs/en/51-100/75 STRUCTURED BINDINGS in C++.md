## 1. Structured Bindings (C++17 Only)

_Structured binding_ is a new feature that allows us to handle multiple return values more effectively (for multiple return values, refer to [52 Handling Multiple Return Values in C++](52%20How%20to%20Deal%20with%20Multiple%20Return%20Values%20in%20C++.md)). This is an extension of the method discussed in Lesson 52, particularly focusing on how to handle _tuples_, _pairs_, and similar return types. Structured binding simplifies our code, making it more concise than previous approaches.

In Lesson 52, Cherno mentioned that he prefers using a struct instance to handle multiple return values. With the introduction of structured bindings, this approach might change.

### Previous Approach

```cpp
#include <tuple>

std::tuple<std::string, int> CreatePerson() // Since there are only two parameters, std::pair could also be used, but tuples are more extensible
{
	return { "Cherno", 24 };
}

int main()
{
	auto person = CreatePerson();
	std::string& Name = std::get<0>(person);
	int age = std::get<1>(person);
}
```

Alternatively, the `std::tie` method can be used, which doesn't require creating an instance and looks cleaner, but using a struct is still preferable:

```cpp
std::string Name;
int age;
std::tie(Name, age) = CreatePerson();
```

Structured bindings solve these issues, making the code look much cleaner (Note: VS defaults to C++14, so you need to set the C++ language standard to 17 in the project properties):

```cpp
auto [name, age] = CreatePerson();
std::cout << name << ":" << age << "\n";
```

![](./storage%20bag/Pasted%20image%2020230731170455.png)