This section begins to delve into some more advanced C++ features, including move semantics, but understanding it requires a lot of prerequisite knowledge, such as lvalues and rvalues. Don't rush to define lvalues and rvalues; take your time to understand them gradually.

## 1. What are Lvalues and Rvalues?

Let's start with simple definitions of lvalues and rvalues:

```cpp
int i = 10;
```
> This expression has two parts: the left side and the right side.
> This is also a good way to think about what lvalues and rvalues are, i.e., lvalues are mostly on the left side of the equals sign, while rvalues are mostly on the right side.
> However, this is not a complete truth and cannot always be understood this way, but in this example, it is correct.

We have a variable ==i==, which is an actual variable with a location in memory, and then we have a value, a numeric literal ==*10*==, which has no storage space, no location, until we assign it to the lvalue ==i==. However, we cannot assign to an rvalue, for example, we cannot say `10 = i`, which would be strange.

![](./storage%20bag/Pasted%20image%2020230807164943.png)

Because `10` has no location, we cannot store data in `10`. On the other hand, ==i== is an lvalue, and obviously, we can make another variable ==a== equal to ==i==.

```cpp
int i = 10;
int a = i;
```
> In this example, we set an lvalue equal to another lvalue, which is why the statement "the right side of the equals sign is an rvalue" is incorrect.

**Rvalues** are not just literals; they can also be the result of a function:

```cpp
int GetValue()
{
	return 10;
}

int main()
{
	int i = GetValue();
	int a = i;
}
```
> We call this function, and it returns a temporary value because the returned `int` has no location, no storage space; it's just a value `10`, so it's also an rvalue. We take this rvalue, this temporary value, and store it in the lvalue `i`.

Since `GetValue()` is an rvalue, assigning to it doesn't work:

![](./storage%20bag/Pasted%20image%2020230807165555.png)

## 2. Lvalue References

But if the function returns an lvalue, things get interesting. We can achieve this by returning an `int&` (**lvalue reference**):

```cpp
// We need to provide some storage for our value, such as using a static int, and then return it
int& GetValue()
{
	static int value = 10;
	return value;
}

int main()
{
	int i = GetValue();
	GetValue() = 5;   // This compiles
}
```
> In this case, the function returns an lvalue reference, so the expression assigning to it is fine. This is what an lvalue reference is.

Additionally, we have a function with a parameter:

```cpp
void SetValue(int value) {}
```

We can call it in various ways, using either an lvalue or an rvalue:

```cpp
int main()
{
	int i = 10;
	SetValue(i);  // Parameter is an lvalue
	SetValue(10);  // Parameter is a temporary rvalue
}
```
> In this case, when the function is called, this rvalue is used to create an lvalue.

We can easily tell which is temporary and which is not because there's a rule: you cannot assign an rvalue to an lvalue reference, so an lvalue reference can only reference an lvalue. Adding an `&` to the function parameter, taking an lvalue reference, immediately results in an error:

![](./storage%20bag/Pasted%20image%2020230807170933.png)
> Non-const reference initializer must be an lvalue.

There's actually a special rule here. Although we cannot use an lvalue to reference an rvalue, meaning `int& a = 10;` is invalid, if we add `const` to the lvalue reference, it works:

```cpp
const int& a = 10;
```
> This is just a special rule, a workaround.

In reality, the compiler might create a temporary variable with your storage and then assign it to that reference:

```cpp
int temp = 10;
const int& a = temp;
```
> So, in reality, it inevitably creates an lvalue, but it supports both lvalues and rvalues.

If we change the function parameter to `const int&`, we can see that it now accepts both types of data:

![](./storage%20bag/Pasted%20image%2020230807171749.png)

Consider another example, try to identify what you think are lvalues and rvalues:

```cpp
int main()
{
	std::string firstName = "Yan";
	std::string lastName = "Chernikov";

	std::string fullName = firstName + lastName;
	std::cout << fullName << "\n";
}
```
> Revealing the answer: In this example, the left sides are lvalues, and the right sides are rvalues.

What needs to be understood is that `firstName + lastName` forms a temporary string, which is then assigned to an lvalue.

```cpp
// Define a function to print the name using an lvalue reference

void PrintName(std::string& name)
{
	std::cout << name << std::endl;
}
```

![](./storage%20bag/Pasted%20image%2020230807172416.png)
> Cannot use a temporary variable as a parameter

This is why you see a lot of constant references (like `const int&`) in C++, as they can accommodate both temporary rvalues and actual lvalue variables:

![](./storage%20bag/Pasted%20image%2020230807172701.png)

Is there a way to write a function that only accepts temporary objects?

## 3. Rvalue References

Of course, this is where **rvalue references** come into play.

Rvalue references are similar to lvalue references, but they use two `&` symbols:

![](./storage%20bag/Pasted%20image%2020230807172833.png)
> Notice that the error positions have swapped; now we cannot use an lvalue as a parameter, but we can pass an rvalue.

With rvalue references, we now have a way to detect temporary values and do something special with them:

```cpp
void PrintName(const std::string& name)
{
	std::cout << "[lvalue]" << name << std::endl;
}

void PrintName(std::string&& name)
{
	std::cout << "[rvalue]" << name << std::endl;
}

/* Here, two versions of the `PrintName` function are defined. One accepts a `const std::string&` parameter (constant lvalue reference), and the other accepts a `std::string&&` parameter (rvalue reference).

When calling `PrintName`, the compiler tries to select the most appropriate overload. Its choice is based on reference collapsing rules and the lvalue/rvalue properties.

1. `PrintName(fullName);`:
    
    - Here, `fullName` is an lvalue because it has a name and can be addressed.
    - The `const std::string&` version is chosen because lvalues prefer to bind to lvalue references (including constant lvalue references) rather than rvalue references. Therefore, `[lvalue]` is output.
2. `PrintName(firstName + lastName);`:
    
    - `firstName + lastName` returns a temporary `std::string` object, which is an rvalue because it does not have a persistent name and cannot be addressed.
    - For temporary objects (i.e., rvalues), they prefer to bind to rvalue references. So, the `std::string&&` version of the overload is chosen. Therefore, `[rvalue]` is output.
*/

int main()
{
	std::string firstName = "Yan";
	std::string lastName = "Chernikov";

	std::string fullName = firstName + lastName;

	PrintName(fullName);
	PrintName(firstName + lastName);
}

/* Although the `const std::string&` version of the function can accept both lvalues and rvalues, if there is a version specifically designed for rvalues (i.e., the `std::string&&` version), when passing an rvalue, the compiler will prefer this version.

The main purpose of this design is to allow developers to provide optimizations specific to rvalues, such as move semantics, thereby improving code performance. */
```

![](./storage%20bag/Pasted%20image%2020230807174334.png)

The main advantage here is optimization. If we know that a temporary object is being passed, we don't need to worry about whether it is alive, intact, or copied. We can simply "steal" its resources and assign them to a specific object or use them elsewhere because we know it is temporary. It won't exist for long; it will only be used in this `PrintName` function.

If you use an lvalue reference in such a function, you cannot "steal" anything from the `name` string because it might be used in many functions.

### A Small Addition

Here, "steal" is used to describe the process of transferring resources from one object to another in move semantics. This is not literal theft but a metaphor to vividly explain this process. ^388d93

To explain in detail:

1. **Traditional Copy Operations**: When you create a copy of an object, all resources (e.g., memory) are copied to the new object. This can be an expensive operation, especially if the object holds a large amount of resources.

2. **Move Semantics and Resource "Stealing"**: Move semantics allows you not to copy resources but to move them from one object to another. In this process, the original object is usually left in a valid but undefined state (e.g., its pointer members may be set to `nullptr`). Since the resources have been "stolen" (i.e., transferred to the new object), the original object no longer owns them.

For example, consider the following code snippet:

```cpp
std::string str1 = "Hello, world!";
std::string str2 = std::move(str1);
```

In the above code, the construction of `str2` does not copy the contents of `str1`. Instead, it "steals" (i.e., moves) the internal pointer of `str1`, and now that pointer points to memory that belongs to `str2`. `str1` is left in a valid but undefined state and should generally not be used anymore.

By avoiding unnecessary copying, move semantics can significantly improve performance. This is especially important when dealing with large objects and containers, such as when you are handling large arrays or matrices, or when constructing and returning temporary objects.

## 4. Summary

In summary, remember:

- Lvalues are **variables with storage support**, while rvalues are **temporary values**;
- Lvalue references only accept lvalues, unless `const` is used, while rvalue references only accept rvalues.

This section is mainly to help those who are confused about this topic, to *clear the air* about what lvalues and rvalues are. As we delve deeper into move semantics later, it will become clear why it is useful. If you are dealing with an rvalue reference, you can "steal" resources from that temporary value (because it is temporary), which can be very helpful for optimization.