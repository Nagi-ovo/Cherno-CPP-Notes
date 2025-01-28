## 1. Definition

To avoid code duplication and other issues, execute specific tasks.

```cpp
    int Multiply(int a,int b)
     |
 return type(void means no return)
	{
		return a * b;
	}
```

## 2. Calling Mechanism

#### Assuming the compiler decides to keep our function as a function rather than *inline*:

Every time we call the function, the compiler generates a [call instruction](06%20How%20the%20C++%20Compiler%20Works.md#^d63649). We need to create an entire *stack frame* for this function, which means pushing **parameters** and the **return address** onto the stack.

The process involves jumping to a different part of the program, executing the commands in our function, and then returning the pushed return value to the location before the function was called. This takes time and slows down the program, so it's not necessary to define a function for every line.

## 3. Return Value

If a return value is defined, it [must be returned](05%20How%20C++%20Works.md#^d4cfc1), except for the `main` function, which defaults to returning 0.

However, errors are only reported in `Debug` mode. When specific *flags* (debugging compilation flags) are activated, errors are reported to help debug the code.

If switched to `Release` mode, the compilation will not report errors, but if called, it will result in *undefined behavior*.