# How to Handle Multiple Return Values in C++

This lesson discusses what a *tuple* is, what a *pair* is, and how to handle multiple return types in C++.

## 1. How to Return Different Types?

We have a function that needs to return two strings, or an *integer* plus a *string*. By default, a C++ function can only return one type, a specific variable, which can cause issues in such cases. If a function needs to return two or more variables of the same type, you can return a `vector` or an array, but for various reasons, this is not always the best approach.

Cherno's favorite solution is to create a struct that contains only the elements to be returned.

C++ provides several methods to handle this.

### 1. Pointers and References
```cpp
#include <iostream>

void returnWithReference(std::string& str, int& num)
{
    str = "Hello";
    num = 42;
}

int main()
{
    std::string str;
    int num;
    returnWithReference(str, num);
    std::cout << str << ", " << num << std::endl;
    return 0;
}
```

### 2. Arrays and Vectors
The difference between an array and a vector: an array is created on the stack, while a vector stores its underlying data on the heap. Therefore, technically, returning a `std::array` is faster.
```cpp
#include <iostream>
#include <array>
#include <vector>

std::array<int, 2> returnWithArray()
{
    std::array<int, 2> result;
    result[0] = 42;
    result[1] = 56;
    return result;
}

std::vector<int> returnWithVector()
{
    std::vector<int> result;
    result.push_back(42);
    result.push_back(56);
    return result;
}

int main()
{
    std::array<int, 2> arrResult = returnWithArray();
    std::cout << arrResult[0] << ", " << arrResult[1] << std::endl;

    std::vector<int> vecResult = returnWithVector();
    std::cout << vecResult[0] << ", " << vecResult[1] << std::endl;

    return 0;
}
```
However, these methods obviously only work when the types are the same.

### 3. Tuples and Pairs
A tuple is essentially a class that can contain x number of variables, regardless of their types.
```cpp
#include <iostream>
#include <tuple>
#include <utility>

std::tuple<std::string, int> returnWithTuple()
{
    return std::make_tuple("Hello", 42);
}

std::pair<std::string, int> returnWithPair()
{
    return std::make_pair("Hello", 42);
}

int main()
{
    std::tuple<std::string, int> tupleResult = returnWithTuple();
    std::cout << std::get<0>(tupleResult) << ", " << std::get<1>(tupleResult) << std::endl;

    std::pair<std::string, int> pairResult = returnWithPair();
    std::cout << pairResult.first << ", " << pairResult.second << std::endl;

    return 0;
}
```
However, the syntax does not allow us to know what the variables are when returning, so Cherno always uses a *struct* instead.

### 4. Struct
```cpp
#include <iostream>

struct Result
{
    std::string str;
    int num;
};

Result returnWithStruct()
{
    Result result;
    result.str = "Hello";
    result.num = 42;
    return result;
}

int main()
{
    Result structResult = returnWithStruct();
    std::cout << structResult.str << ", " << structResult.num << std::endl;

    return 0;
}
```