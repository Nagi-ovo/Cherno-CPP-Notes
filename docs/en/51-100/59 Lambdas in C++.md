## 1. What is Lambda Used For?

*Lambda* is essentially a way for us to define something called an anonymous function. This method allows us to create a quick, one-time function without actually defining a formal function. We tend to view it more as a variable rather than a formal function that exists as a symbol in our compiled code.

As long as you have a function pointer, you can use lambda in C++. This is how it works, so lambda is a method for us to define a function without needing to define it through a function declaration.
The usage of lambda is that wherever we would set a function pointer to point to a function, we can set it to a lambda instead.

Lambda is a great way to specify code that we want to run in the future as a function.

What if we want to bring external variables into the instructions inside the lambda function?
Just like when we create our own functions, there are two methods: pass by value and pass by reference. This is where capturing comes into play. The `[]` specifies how we intend to pass variables. (`[=]`, pass all variables by value; `[&]` pass all variables by reference)
You can also pass individual variables, `[a]` passes `a` by value, `[&a]` passes `a` by reference.

```cpp
#include <iostream>
#include <vector>
#include <functional>

void ForEach(const std::vector<int>& values,const std::function<void(int)>& func)
{
	for (int value : values)
		func(value);
}

int main()
{
	std::vector<int> values = { 1,5,4,2,3 };
	int a = 5;
	auto lambda = [=](int value) {std::cout << a << std::endl; };
	ForEach(values,lambda);

	std::cin.get();
}
```

Even though `a` is passed by value and copied in the lambda here, it does not allow us to reassign `a` within it, unlike in a normal function. To fix this, simply add `mutable` in front (all of this can be learned on [cppreference.com](https://en.cppreference.com/w/))
```cpp
auto lambda = [=](int value) mutable { a = 6; std::cout << a << std::endl; };

// 6 6 6 6 6
```


## 2. Why You Might Want to Use Lambda

```cpp
#include <algorithm>

auto it = std::find_if(values.begin(), values.end(), [](int value) {return value > 3; });

std::cout << *it << std::endl;
```

The `std::find_if` function searches within the `values` container for the first element that satisfies the condition specified by the lambda expression. `values.begin()` and `values.end()` represent the start and end iterators of the container, respectively. This function will search within the range of all elements in the container.
`[](int value) {return value > 3; }` is an anonymous lambda expression that specifies the search condition: the element's value is greater than 3. `std::find_if` will return an iterator pointing to the first element that satisfies the condition. If no such element is found, it will return the iterator `values.end()`.

Equivalent to:
```cpp
void ForEach(const std::vector<int>& values,const std::function<void(int)>& func)
{
	for (int value : values)
		if(value > 3)    // Add boolean judgment
			func(value);
}
```
But we can use lambda to quickly implement this by specifying this boolean condition.