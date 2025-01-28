# Storing Different Types of Data in a Single Variable Series 2/3

This section discusses how to store multiple types of data in a single variable, which is a feature provided by the C++17 standard library.

## 1. std::variant

This is similar to `std::optional`, and its purpose is to allow us not to worry about the exact data type being processed. A single variable is placed there, and we can consider its specific type later. It allows you to list all possible types, and then you can decide what it will be. If you want, you can reassign it to any type, which is also a way to create a variable that may have multiple types.

```cpp
#include <variant>

int main()
{
	std::variant<std::string, int> data;
	data = "Cherno";
	std::cout << std::get<std::string>(data) << "\n";
	data = 2;
	std::cout << std::get<int>(data) << "\n";

	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230731191350.png)

What happens if we access it with the wrong type?

![](./storage%20bag/Pasted%20image%2020230731191534.png)

The `std::get` function will throw a `bad_variant_access` exception, which can be handled using `try-catch`. However, there are other methods to determine if the data type is what we expect without using exceptions.

First, the `index` function:

```cpp
if(data.index() == 0) // Is the index 0, i.e., is it the first type, std::string?
```

A better method is to use the `get_if` function:

```cpp
if (auto value = std::get_if<std::string>(&data))
{
	std::string& v = *value;
}
else // Or use else if to handle another type
{

}
```

In this code, `std::get_if` is a function used to access the members of `std::variant`. It attempts to access the value of `data` as a `std::string`. If the current type of `data` is `std::string`, then `get_if` will return a pointer to that value; otherwise, it will return `nullptr`. The `if` statement then checks if `value` is `nullptr`. If `value` is `nullptr`, the condition of the `if` statement evaluates to `false`, so the code inside the `if` block will not execute, and it will jump to the `else` block instead.

## 2. Comparison with Union

Refer to [67 Unions in C++](67%20Unions%20in%20C++.md)

There is a lot of discussion about `variant` being essentially a type-safe *union*, but they are quite different.

```cpp
std::variant<std::string, int> data;
std::cout << sizeof(data) << std::endl;
```

If `data` were a `union`, its size would be the size of the largest type it contains. However, `variant` stores all possible data types as separate variables within a structure or class:

![](./storage%20bag/Pasted%20image%2020230731193322.png)

It essentially creates a structure or class for you, storing these data types as members within that structure or class. Therefore, technically, `union` is still a more efficient and better choice. `variant` is more type-safe and does not cause undefined behavior. Unless you are doing low-level optimization where memory size needs to be kept to a minimum, such as CPU processing, you should use it. For example, if you are developing on a desktop platform where you can freely use more memory and processing power, `std::variant` is technically safer.

## 3. Other Uses

For enums, refer to [24 Enumerations](24%20ENUMS%20in%20C++.md)

As mentioned in the previous lesson, `optional` is generally used to indicate that data may or may not exist, while `variant` can allow a function to return values of different types. This way, when reading a file, we can not only return an empty optional value but also discover where the problem lies and handle it accordingly:

```cpp
enum class ErrorCode
{
	None = 0, NotFound = 1, NoAccess = 2
};

std::variant<std::string,ErrorCode> ReadFileAsString()
{
	if (error_occurred)
	{
		return ErrorCode::NotFound; // Return ErrorCode...
	}
	else
	{
		return "File contents"; // Return file contents
	}
}
```

This is another good example of using `variant`, providing more detailed information than returning a boolean value, and giving us more insights.