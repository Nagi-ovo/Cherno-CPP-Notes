## 1. Constructors

![](./storage%20bag/Pasted%20image%2020230703113310.png)

Reason: When we instantiate the `Entity` class and allocate memory, the memory is not actually initialized yet.

```cpp
std::cout << e.X << std::endl; // C(compilation error): uninitialized local variable 'e' used
```

### Common Practice:

![](./storage%20bag/Pasted%20image%2020230703115633.png)

### Constructor

A constructor is a special type of method that is primarily used here. It is called whenever you create an object ^0156ab.

```cpp
class Entity
{
public:
    float X, Y;

    Entity()   // Constructor
    {
        X = 0.0f;
        Y = 0.0f;
    }

    void Print()
    {
        std::cout << X << "," << Y << std::endl;
    }
};

int main()
{
    Entity e;
    std::cout << e.X << std::endl;  // 0
    e.Print();  // 0,0
    std::cin.get();
};
```

#### Default Constructor

The *default constructor* is provided by default, which is essentially like an empty function body that does nothing.

```cpp
Entity()  // Default constructor, similar to
{
}
```

No variables are initialized.

In C++, you must manually initialize **all primitive types**, otherwise they will be set to whatever value was previously left in memory.

## 2. Function Overloading

You can write multiple constructors with the same name but provide different parameters.

![](./storage%20bag/Pasted%20image%2020230703121513.png)

When creating an object instance using the *new* keyword, the constructor is also called.
I only want others to use this class like `Log::Write`, and I don't want others to create instances.

### a. Setting the Constructor to Private

```cpp
class Log
{
private:
    Log(){}
public:
    static void Write()
    {
    }
};

int main()
{
    Log::Write();
    Log l;
}
```

![](./storage%20bag/Pasted%20image%2020230703121952.png)

Or use

### b. Delete

```cpp
Log() = delete;
```

Deletes the default constructor.