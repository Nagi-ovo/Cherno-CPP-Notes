Data structures determine how data is stored, and data is crucial in C++ programming.

Suppose I have a vector of integers or an array of integers, and I want to sort them by value or some predicate. How can I get C++ to do this for me?

Obviously, you can write your own algorithms, such as bubble sort, quicksort, or any other algorithm that traverses a list and sorts its elements according to your desired sorting method. However, in some cases, such as when dealing with C++'s built-in collection types like `std::vector`, you don't need to write an algorithm yourself. You can let the C++ library handle the sorting for you. Therefore, here we are concerned with `std::sort`.

## 1. std::sort

This is C++'s built-in sorting function, which can sort any type of iterator you provide to it.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main()
{
	std::vector<int> values = { 3,5,1,4,2 };
	std::sort(values.begin(), values.end());  // If we don't provide any type of predicate, i.e., we don't give it a function to sort with, it will sort integers in ascending order by default.

	for (int value : values)
		std::cout << value << std::endl;
	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230724173418.png)

## 2. Using Lambda

If you want to sort in a specific way, you can pass in a function. This can be a function you create within a structure, a [Lambda](59%20Lambdas%20in%20C++.md), or a built-in function.

```cpp
#include <functional>

int main()
{
	std::vector<int> values = { 3,5,1,4,2 };
	std::sort(values.begin(), values.end(),std::greater<int>()); // Sort in descending order

	for (int value : values)
		std::cout << value << std::endl;
	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230724173622.png)

The comparison function (`Compare`) of the `std::sort` function needs to return a `bool` value, indicating the size relationship between two elements. If the first element should come first, it returns true.

```cpp
std::sort(values.begin(), values.end(),[](int a,int b)
{
	return a < b;  // Small elements come first, sorting in ascending order
});
```

![](./storage%20bag/Pasted%20image%2020230724174233.png)

Changing it to `return a > b` will reverse the order, sorting in descending order.

If you want to place 1 at the end, you can do:

```cpp
std::sort(values.begin(), values.end(),[](int a,int b)
{
	if (a == 1)
		return false;
	if (b == 1)
		return true;
	return a < b;
});
```

![](./storage%20bag/Pasted%20image%2020230724174738.png)

Sorting is very useful. You can sort all types of data, not necessarily just integers. You can sort strings, custom classes, and more. Therefore, the *Predicate* (lambda) is very useful because it means we can set rules and not rely solely on built-in types or similar things.