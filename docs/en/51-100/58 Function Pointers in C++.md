This section will cover raw-style function pointers (from C language).

## 1. What is a Function Pointer?

A **function pointer** is a way to assign a function to a variable. From this, you can also pass functions as parameters to other functions. In fact, functions can be used to do many things, which creates a lot of interesting and complex logic. Without function pointers, this would be very cumbersome.

The `auto` keyword is very useful for things like function pointers:

```cpp
void HelloWorld()
{
    std::cout << "HelloWorld" <<  std::endl;
}

int main()
{
    auto function = HelloWorld;   // Note that there are no parentheses here

    std::cin.get();
}
```

Specifically, this is like using the `&` address-of operator. We get the memory address of this function. Imagine that when you compile your code, each function is compiled into CPU instructions, and they reside in our binary file. What we need to do is retrieve the location of the instructions to be executed when the function is called. We don't need to write `&HelloWorld` because there is an **implicit conversion** here.

![](./storage%20bag/Pasted%20image%2020230721111933.png)

The actual type of `auto`:

```cpp
void(*function)() = HelloWorld;   // Same as auto function = HelloWorld;
```

Or create an *alias*:

```cpp
typedef void(*HelloWorldFunction)();

HelloWorldFunction function = HelloWorld;

function();
```

Function with parameters:

```cpp
void HelloWorld(int a)
{
    std::cout << "HelloWorld:" << a <<  std::endl;
}

int main()
{
    typedef void(*HelloWorldFunction)(int);

    HelloWorldFunction function = HelloWorld;

    function(3);   // HelloWorld:3
}
```

## 2. Why Use Function Pointers?

```cpp
void PrintValue(int value)
{
    std::cout << "Value:" << value << std::endl;
}

void ForEach(const std::vector<int>& values, void(*func)(int))
{
    for (int value : values) // This is a range-based for loop.
        func(value);
}
// In this syntax, `int value` is the defined loop variable, and `values` is the container to be traversed. The meaning of the loop is: for each element in the container `values`, assign its value to the variable `value`, and then execute the relevant operations in the loop body. This syntax simplifies the traditional index or iterator traversal method, making the code more concise and readable.

int main()
{
    std::vector<int> values = { 1,5,4,2,3 };
    ForEach(values, PrintValue);

    std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230721113234.png)

This method can tell the function to do something at a specific time, but this method does a bit too much. So let's use another method:

## 3. Lambda

If we don't want to define the `PrintValue` function this way, because such a small amount of information doesn't need an extra function, especially if we only plan to use it inside the `ForEach` function, we can use something called a **lambda**.

A lambda is essentially a normal function, but unlike a normal function, it is declared inline and is **disposable** after use:

```cpp
void ForEach(const std::vector<int>& values, void(*func)(int))
{
    for (int value : values)
        func(value);
}

int main()
{
    std::vector<int> values = { 1,5,4,2,3 };
    ForEach(values, [](int value) {std::cout << value << std::endl; });

    std::cin.get();
}
```

Here, the `[]` is called the **capture method**, which is how parameters are passed in and out. More on this later.