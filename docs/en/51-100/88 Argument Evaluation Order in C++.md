This section covers some C++ tips and tricks, and the next section will be about **Move Semantics**!

## 1. Parameter Evaluation Order

```cpp
void Function(int a, int b, int c) {}
int a = 2;
Function(GetResult(), ++a, a--);
```

> In a function with multiple parameters, what is the order of parameter evaluation?

Cherno believes that it is normal and reasonable if you don't know the answer to this question, as it involves a deep understanding of how the compiler compiles code, and you wouldn't typically consider this "common" issue in everyday programming.

Let's consider this problem with an example. What will be the output of the `PrintSum` function in the following example?

```cpp
void PrintSum(int a, int b)
{
	std::cout << a << " + " << b << " = " << (a + b) << std::endl;
}

int main()
{
	int value = 0;
	PrintSum(value++, value++);

	std::cin.get();
}
```

> `value++` is a post-increment operator, meaning the initial value should be passed first and then incremented. So, I think the answer is 1, 0.

However, the correct answer to this question is "undefined behavior" (_undefined behavior_). The C++ standard does not truly define what should happen in this case. Here, "undefined behavior" means that it can vary depending on the compiler, entirely relying on the actual implementation of how the C++ compiler converts code into machine code.

![](./storage%20bag/Pasted%20image%2020230811172357.png)

> Debug mode

![](./storage%20bag/Pasted%20image%2020230811172459.png)

> Release mode

Changing to pre-increment:

```cpp
PrintSum(++value, ++value);

// Release: 2 + 2 = 4
// Debug  : 2 + 2 = 4
```

So, what exactly happens with post-increment operations in Release mode?

The reason is that in such cases, the compiler is actually allowed to compute these in parallel, without having to evaluate these parameters in the specified order first and then see what they are (somewhat like *constant folding*, which precomputes the results of constant expressions, e.g., `int a = 1 * 2`, which is not computed at runtime but optimized to `int a = 2` at *compile-time*).

This was possible before the C++17 standard because the C++17 standard introduced a new rule: postfix expressions must be evaluated before other expressions. As a result, the output changes:

```cpp
PrintSum(value++, value++);

// C++ 14 :
// Release: 0 + 0 = 0
// Debug  : 1 + 0 = 1

// C++ 17 :
// Release: 1 + 0 = 1
// Debug  : 1 + 0 = 1
```

> However, the order here is still undefined.

Running it with gcc and the C++20 standard:
![](./storage%20bag/Pasted%20image%2020230811180844.png)

> The screenshot shows that, compared to the MSVC compiler in VS, gcc at least tells us that this `value` operation might be undefined, and we also get the result.

And the compilation result with clang is the opposite:
![](./storage%20bag/Pasted%20image%2020230811181151.png)

So, if you encounter this question in a job interview or programming test, the correct answer is "undefined," because C++ does not actually provide a specification or definition of what should happen in this case, or the order in which parameters or arguments should be evaluated. But if you mention that C++17 disallows simultaneous computation, it will be a plus. However, since the order is not defined in the specification, it means that technically, you cannot know what the evaluation order will be.