Even though type casting has been used before, it hasn't been discussed yet. It's something that needs to be connected and learned through experience, rather than just being told how it works. Having only theory without practice on this topic won't help much.

## 1. What is casting

Here, *casting* refers to type conversion, or more precisely, type conversions that must be performed within C++'s available type system.

C++ is a strongly-typed language, meaning there is a type system, and types are enforced. (See [Lesson 66: Type Punning in C++](66%20Type%20Punning%20in%20C++.md#^4d9dfe))
If I set something as an `int`, I can't suddenly treat it as a `double` or `float`, and vice versa. I must stick to the original type, unless there is a simple **implicit conversion** (See [Lesson 40: Implicit Conversion and the Explicit Keyword in C++](40%20Implicit%20Conversion%20and%20the%20Explicit%20Keyword%20in%20C++.md#^cde452)), meaning C++ knows how to convert between these two types without data loss - that's implicit conversion; or there is an **explicit conversion** (See [Lesson 66: Type Punning in C++](66%20Type%20Punning%20in%20C++.md#^f3904d)), telling C++ you need to convert this type to the target type. This chapter will formally introduce the meaning of **casting** and explain how to use it.

## 2. Type Casting

The methods we use to perform type casting, especially explicit type casting, can be divided into two styles (personal understanding): C-style and C++-style.

### C-Style Type Casting

```cpp
int a = 5;
double value = a; // This is an implicit conversion, easy to do and no data loss

double value = 5.25;
int a = value;  // This is also considered an implicit conversion because it's not necessary to specify the target type

// To perform an explicit conversion, you can write it like the line below

int a = (int)value; // Of course, it could be done implicitly in this case, but we are discussing casting, so let's write it this way for now.
```

A better example:

```cpp
int main()
{
	double value = 5.25;
	double a = value + 5.3;
	std::cout << a << std::endl;   // Obviously, this outputs 10.55

	std::cin.get();
}
```

If we cast `value` to an `int` type, the fractional part will be discarded, resulting in $5 + 5.3 = 10.3$:

```cpp
double a = int(value) + 5.3;  // 10.3 instead of 10.55
```

The technique used here is called **C-style type casting**, because it specifies the type to cast to in parentheses, followed by the variable we want to cast.
You can also enclose the entire expression to truncate the whole result to an integer:

```cpp
double a = int(value + 5.3);  // 10
```

### C++-Style Type Casting

#### 1. static_cast

To do this the C++ way, use C++ `cast` operators:

```cpp
double s = static_cast<int>(value) + 5.3;
```

There are several C++-style casts: `static_cast`, `reinterpret_cast`, `dynamic_cast`, and `const_cast`. These are the four main casts. They don't do anything that C-style casts can't do; it's not about adding new functionality, but rather adding some *syntax sugar*.

For example, `dynamic_cast` actually performs a check and returns NULL if the conversion fails, so it does extra work and can slow down execution. But in most cases, C++-style casts don't do anything extra; they are just English words in your code.
For instance, `static_cast` means static type conversion, and in the case of static casting, it also performs other compile-time checks to see if such a conversion is possible.
`reinterpret_cast` is similar; it's like expressing **type punning** in English, meaning "I want to reinterpret this memory as something else."
`const_cast` removes or adds the const qualifier to a variable.

##### So why have so many casts?

Besides potentially receiving the compile-time checks mentioned above, it also makes it easier to search for them in your codebase. If I want to see where all my type casts are, perhaps I have performance issues and don't want to use `dynamic_cast`, I can simply search for that term. If C-style casts were used, it would be much harder to search for them. So it helps both in reading and writing code for the programmer.
It also helps us reduce the chance of accidentally making mistakes when attempting casts, such as with incompatible types.

```cpp
class AnotherClass
{
public:
	AnotherClass(){}
	~AnotherClass(){}
};

int main()
{
	double value = 5.25;
	double a = int(value) + 5.3;

	double s = static_cast<AnotherClass*>(value);
	std::cout << a << std::endl;
	std::cin.get();
}
```

You can see this is an invalid type conversion.
![](./storage%20bag/Pasted%20image%2020230727161515.png)

For type punning, you can use `reinterpret_cast`. Here we reinterpret the data at the `value` pointer as data for an `AnotherClass` instance:

```cpp
double s = reinterpret_cast<AnotherClass*>(&value);
```

But the key point is that `static_cast` adds compile-time checks. If you use a C-style cast, it would default to doing what `reinterpret_cast` does.

The best way to actually learn these is through practice, trying to build examples that use these casts.

#### 2. dynamic_cast

```cpp
class Base
{
public:
	Base() {}
	virtual ~Base(){}
};

class Derived : public Base
{
public:
	Derived() {}
	~Derived() {}
};

class AnotherClass : public Base
{
public:
	AnotherClass(){}
	~AnotherClass(){}
};

int main()
{
	Derived* derived = new Derived();
	Base* base = derived;   // Convert derived to Base type

	std::cin.get();
}
```

There's a question: Here I have a Base pointer. Is it an instance of the Derived class or the AnotherClass class? Both of them extend from the Base class.

```cpp
AnotherClass* ac = dynamic_cast<AnotherClass*>(base);
```

If I use `dynamic_cast`, it not only asks this question but also attempts the conversion and does something if the conversion fails.

![](./storage%20bag/Pasted%20image%2020230727163407.png)

Here, `dynamic_cast` is trying to convert the base class pointer `base` to an `AnotherClass` pointer. However, the original `base` pointer actually points to a `Derived` object, not an `AnotherClass` object. These two classes (`Derived` and `AnotherClass`) are both derived from the `Base` class, but they are completely different classes and cannot be converted to each other.

`dynamic_cast` performs a type check at runtime. If the type conversion is safe, it performs the conversion; otherwise, it returns null. In this example, because the `base` pointer actually points to a `Derived` object, not an `AnotherClass` object, `dynamic_cast` judges this conversion to be unsafe and thus returns null.

This ability for type checking is an important feature of `dynamic_cast`; it protects us from performing unsafe type conversions at runtime. This is why `ac` is null.

If we change it to the Derived class, the pointer becomes valid because the conversion is successful.

![](./storage%20bag/Pasted%20image%2020230727163921.png)

This is closely related to *RTTI* (Runtime Type Information).

You need to know that these casting operators are a way to simplify type conversions for you, potentially making conversions more reliable because they perform compile-time checks, and `dynamic_cast` performs runtime checks. By using such casting operators, you get more robust code.