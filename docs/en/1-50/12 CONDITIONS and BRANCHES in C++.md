# if statements

The `==` operator is an *equality* operator, implemented in the standard library, which extracts the four bytes of two integers and compares them bit by bit.

## 1. Disassembly

When debugging in [Debug mode](11%20How%20to%20DEBUG%20C++%20in%20Visual%20Studio.md#^a1059f), right-click or press Ctrl+K, G to bring up the Go to disassembly window.
![](./storage%20bag/Pasted%20image%2020230627161844.png)

`jne` (jump not equal), jumps if the values are not equal.

```assembly
00C8601E  mov         dword ptr [ebp-0DCh],0  ; boolean is assigned 0 (false)
```

If `00C86035  test   eax,eax` succeeds, meaning the test operation is true, then `je` (jump equal) will be executed, jumping to the line with cin.get().

![](./storage%20bag/Pasted%20image%2020230627162803.png)

## 2. Constant Folding

A compiler optimization technique. It converts all these into a constant variable, as these constants are known at compile time. Then, during compilation, it directly removes the if statements and jumps to cin.get().

Therefore, you need to operate in Debug mode.

You can write it as:

```c++
if (x == 5)
    Log("Hello World")   // If it's inconvenient to set a breakpoint on the same line
```

## 3. if else

```cpp
const char* ptr = "Hello";
if (ptr)
    Log(ptr);
else if (ptr == "Hello")
    Log("ptr is Hello");
```

The code after else is executed only if the if condition fails, meaning only if ptr is false, then else if... is executed.
![](./storage%20bag/Pasted%20image%2020230627170041.png)
The reason is as follows:

#### else if is just an else followed by an if

```cpp
else if (ptr == "Hello")
    Log("ptr is Hello");

// Equivalent to

else
{
    if (ptr == "Hello")
        Log("ptr is Hello");
}
```

Programming = Mathematical part + Logical part ^2780f2

Some operations might be used to replace comparisons and branches, making the code faster and more practical.