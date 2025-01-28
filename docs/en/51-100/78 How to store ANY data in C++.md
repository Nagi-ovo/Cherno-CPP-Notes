# Storing Different Types of Data in a Single Variable Series 3/3

This section will discuss how to store any type of data in a single variable. You can use `void*` to handle this, but here we will introduce a better and safer method, which is a new approach brought by the C++17 standard.

## 1. std::any

Its usage is straightforward. The main points to consider are: why does this thing exist, when should it be used, and why use `std::any` instead of `std::variant`. These are the most exciting parts of this section.

```cpp
#include <any>

int main()
{
	std::any data;
	data = 2;   // int
	data = "Cherno";   // const char
	data = std::string("Cherno"); // string

	// If you want to extract the data
	std::string string = std::any_cast<std::string>(data);

	std::cin.get();
}
```

If the type of value contained in the `std::any` object matches the target type of `std::any_cast`, then `std::any_cast` will return the value. Otherwise, if the types do not match, `std::any_cast` will throw a `std::bad_any_cast` exception.

It looks similar to `std::variant`, and they do have some similarities. They can store any type of data. Some might think that `std::variant` is bad because it requires us to list all the types, while with `std::any`, we don't need to worry about types at all. But in fact, it's the opposite. This is why `std::variant` is better than `std::any` in most cases.

In fact, requiring `std::variant` to list all these types is a good thing, as it ensures type safety:

```cpp
data = "Cherno";   // For example, forgetting to explicitly state that this is a string
// The following line of code seems reasonable, but when trying to extract, you encounter a problem: data is a const char*
std::string string = std::any_cast<std::string>(data);

// With std::variant, it works fine because the types are limited

#include <variant>

std::variant<int, std::string> data;
data = 2;
data = "Cherno";
std::string string = std::any_cast<std::string>(data);
```

Apart from `std::variant` requiring the listing of types, what other differences are there between `std::any` and `std::variant`?

## 2. Differences Between std::any and std::variant

Of course, there are differences, and they relate to their storage methods.

`std::variant` is just a type-safe `union`, meaning it stores all data in a [union](67%20Unions%20in%20C++.md).

What about the storage method of `std::any`? Let's dive into its header file:

> The variable named Storage, which seems to be used for storing things, is actually a Union.
> ![](./storage%20bag/Pasted%20image%2020230802013345.png)

> Finally, upon deeper inspection, Small_storage is an aligned_union_t, which is the aligned_union of all types.
> ![](./storage%20bag/Pasted%20image%2020230802013626.png)

So what does `std::any` actually do? It's quite clever. For _small types_, it simply stores them as a `union`, meaning that for small types, it works exactly the same as `std::variant`.

However, if you have a large type, it will take you into the `void*` of large storage space. In this case, it will dynamically allocate memory, which is not good for performance.

If you need more storage space (here you can see it's >32), `std::any` will dynamically allocate, but `std::variant` will not.

![](./storage%20bag/Pasted%20image%2020230802014151.png)

So in other words, besides being more type-safe and slightly more restrictive, `std::variant` also performs faster when handling larger data, or if your data needs to avoid dynamic memory allocation.

Another performance tip is to avoid copying data. In the previous code, there was a copy of the string, which can be replaced by returning via reference:

```cpp
// In std::get(), you can directly add a reference symbol, but in std::any_cast, you need to insert the reference into the template parameter to optimize well
std::string& string = std::any_cast<std::string&>(data); // Note that the reference is also used in the template parameter here
```

Under the current circumstances, we won't get any memory allocation other than that of the string. You can simply test this:

```cpp
void* operator new(size_t size) // This is not a good implementation of the new operator, so do not use it in any production code
{
	return malloc(size); // Set a breakpoint here
}
```

![](./storage%20bag/屏幕截图%202023-08-03%20005450.jpg)

> You can see that we indeed got a memory allocation, which comes from std::string, std::basic_string entering the allocator. any actually just forwards all these parameters with a \_Construct_in_place, and basic_string does another memory allocation, which is the entire memory allocation in this program. In this case, std::any did not allocate anything.

```cpp
struct CustomClass
{
	std::string s0, s1;  // One is 28(x86)
};

int main()
{
	std::any data;
	data = 2;   // int
	data = CustomClass();
//	std::string& string = std::any_cast<std::string&>(data);

	std::cin.get();
}

```

![](./storage%20bag/Pasted%20image%2020230803011322.png)

> During the Emplace process, you will see that this is a large storage process, so it will call new. Therefore, you should know that std::any will allocate when necessary. In this case (>32Bytes), it will call new and dynamically allocate memory. Here, the compiler might have abstracted the process, so the same effect as in the video was not achieved.

## 3. When to Use any and variant?

This is a tricky question.

If you want to store multiple data types in a single variable, use `std::variant`, because it is essentially a type-safe version of `std::any`. This means you cannot arbitrarily set its type. Moreover, it does not dynamically allocate memory, which results in better performance.

If you need to be able to store any data type in a single variable, perhaps you need to reconsider your program design. Cherno means that he really can't think of a valid use case (it shouldn't be used). If you have data like a buffer and you don't know the type of this data, you just want to point to it, then you can use `void*`. As it stands, Cherno does not think it is as useful as `std::optional` and `std::variant`. You should clearly realize that `std::any` might not be something you should use frequently. (Opinion published in 2019 when the video was recorded).