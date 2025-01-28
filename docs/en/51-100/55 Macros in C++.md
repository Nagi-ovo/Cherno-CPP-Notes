## 1. Preprocessing Stage

[05 How C++ Works](05%20How%20C++%20Works.md)  
Statements with `#` are *preprocessor statements*, also known as preprocessing directives.  
These directives are processed before actual compilation begins. When the compiler receives a source file, the first thing it does is preprocess all the preprocessing directives.

The preprocessing stage is essentially a text-editing phase where we can control what code is passed to the compiler. This is where *macros* come into play.  
What we can do is write some macros that replace text in the code with something else, which is essentially like performing a search-and-replace operation throughout our code.  
(So templates are evaluated later than macros.)

How you use macros depends on your personal preference. If you use too many macros, the code might become harder to understand. Don’t overuse C++ features, especially as we delve into more advanced features. You don’t need to show off that you know every C++ feature to everyone, and using more features isn’t necessarily the way to write good code.  
In a previous section, I defined:

```cpp
#define LOG(x) std::cout << x << std::endl;
```

This is a macro.

## 2. Macros

```cpp
#define WAIT std::cin.get()   // Every time the word WAIT is encountered, the following code is pasted

int main()
{
	WAIT;   // The code sent to the compiler is actually: std::cin.get();
}
```

How our program runs, what the compiler sees, and how the code is compiled are all the same. The compiler doesn’t see any difference because all we’re doing is changing how the text is generated.  
However, this isn’t a good example because it’s not how you should use preprocessing. It’s quite silly; you should just write the actual code. The point here is to understand how preprocessing works.

Think of it as a function during the precompilation stage. The advantage of macro functions is that they don’t have the overhead of saving registers, passing parameters, or returning values like regular functions do. The expanded code is efficient and fast.  
Even the LOG(x) example above might not be used this way. However, in more complex logging systems, such as in game engines, applications, or frameworks, you might use macros in the logging system because the way you log might change based on your settings. For example, you might want logs in the Debug version but remove them in the Release version, and macros can achieve this:

![](./storage%20bag/Pasted%20image%2020230718161725.png)  
Similarly, you can add PR_RELEASE for the Release version.

```cpp
#ifdef PR_DEBUG
#define LOG(x) std::cout << x << std::endl;
#else
#define LOG(x)
#endif
```

Debug mode:  
![](./storage%20bag/Pasted%20image%2020230718162021.png)

Release mode:  
![](./storage%20bag/Pasted%20image%2020230718162056.png)

This is a practical use of macros.

However, there’s an issue here. If it’s just a definition, it might be misunderstood. Generally, you can use `#define` for this purpose, rather than `#ifdef`, which can be worse in many cases.

```cpp
#define PR_DEBUG 0

#if PR_DEBUG == 1
```

This way, you don’t need to delete it; you can just modify it to control PR_DEBUG, making it clearer. You can also add PR_DEBUG=1 in the properties.

```cpp
#if PR_DEBUG == 1
#define LOG(x) std::cout << x << std::endl;
#elif defined(PR_RELEASE)    // You can use elif
#define LOG(x)
#endif
```

## 3. Special Uses of Macros

We can also use the preprocessor and macros to remove specific code:  
![](./storage%20bag/Pasted%20image%2020230718163057.png)

Macros can be written in multiple lines by using `\` to indicate line breaks (the backslash is an escape for the Enter key):  
![](./storage%20bag/Pasted%20image%2020230718163339.png)  
Note that there should be no spaces after the backslash, or it will escape the space instead.

If you want to track when memory is allocated, you can set up a `new` macro that records which line of code it is and how much memory is allocated.