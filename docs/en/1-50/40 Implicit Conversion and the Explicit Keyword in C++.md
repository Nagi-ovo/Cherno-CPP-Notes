## 1. Implicit Constructors / Implicit Conversion

The term _implicit_ means that it doesn't explicitly tell you what it's going to do; it kind of works automatically under certain circumstances. In fact, C++ allows the compiler to perform an implicit conversion on the code.

If I start using one data type as if it were another, there will be a type conversion between these two types. C++ allows this conversion to happen implicitly, without the need for a *cast* or other explicit conversion. ^cde452

```cpp
class Entity
{
private:
	std::string m_Name;
	int m_Age;
public:
	Entity(const std::string& name)
		: m_Name(name), m_Age(-1){}
	Entity(int age)
		: m_Name("Unknown"), m_Age(age) {}

	const int& GetName() const { return m_Age; }
};

int main()
{
	Entity a("Cherno");
	// Entity a = "Cherno";  Not recommended, the above is clearer
	Entity b = Entity(22);
	// Entity b = 22;
	std::cout << a.GetName() << std::endl;
	std::cin.get();
}
```

Here, why can an integer be assigned to a class that also has a string member `name`?
This is due to implicit conversion or implicit constructors.
It implicitly converts `22` into an `Entity` object, constructing an `Entity` because `Entity` has a constructor that takes an integer parameter `age`, and another that takes a string parameter.

```cpp
void PrintEntity(const Entity& entity)
{
	// Printing
}

int main()
{
	PrintEntity(22);
	PrintEntity("Cherno");
```

![](./storage%20bag/Pasted%20image%2020230708165018.png)

Here, the parameter is a *char array\[7]*, not a `std::string`. See [32 How Strings Work in C++ (and how to use them)](<32%20How%20Strings%20Work%20in%20C++%20(and%20how%20to%20use%20them).md>)
For this to work, C++ needs to perform two conversions: one from `const char` array to `string`, and another from `string` to `Entity`. However, only one implicit conversion is allowed.

```cpp
PrintEntity(std::string("Cherno"));
PrintEntity(Entity("Cherno"));
```

This can help simplify your code, but personally, I would try to avoid using it unless it's necessary to simplify the code, rather than wrapping it through constructors.

## 2. The `explicit` Keyword

The *explicit* keyword disables implicit conversion. Placing it before a constructor means that this constructor will not perform implicit conversions. If you want to construct an `Entity` object using an integer, you must explicitly call the constructor.

```cpp
explicit Entity(int age)
		: m_Name("Unknown"), m_Age(age) {}
```

![](./storage%20bag/Pasted%20image%2020230708165751.png)

```cpp
Entity b(22);
Entity b = (Entity)22;
Entity b = Entity(22);
```

The `explicit` keyword is sometimes used in mathematical libraries because you don't want to compare numbers with vectors, ensuring code safety. However, it's not frequently used. It might be used in low-level encapsulation to prevent accidental conversions, performance issues, or bugs.