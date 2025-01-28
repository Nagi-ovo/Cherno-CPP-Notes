_Breakpoints_ and _reading memory_

Setting breakpoints to read memory

## 1. Breakpoints

A breakpoint is a point in the program where the debugger will *break* (interrupt). When execution reaches the line with the breakpoint, the execution thread will pause.

#### Visual Studio Breakpoint Shortcut: F9

When _Debugging_, make sure you are ==in "Debug" mode==. The configuration can be seen in [Configuration](05%20How%20C++%20Works.md#^0b34c7).
In "Release" mode, the code may be altered, and your breakpoints might never be executed. ^a1059f

### Debugging

##### Step Into: F11

##### Step Over: F10

##### Step Out: Shift + F11

![](./storage%20bag/Pasted%20image%2020230626144929.png)

Now, perform a *Step into* on the seventh line of the main function.

![](./storage%20bag/Pasted%20image%2020230626144858.png)

The yellow arrow indicates that the current line has not been executed yet. Press F10 to move the arrow to the sixth line.
After pressing F10 again, the string is output.
![](./storage%20bag/Pasted%20image%2020230626145245.png)

Look at this program:

```cpp
int main()
{
·	int a = 8;   //breakpoint
	a++;
	const char* string = "Hello";

	for (int i = 0; i < 5; i++)
	{
		const char c = string[i];
		std::cout << c << std::endl;
	}

	Log("Hello Wolrd");
	std::cin.get();
}
```

At this point, `int a=8` has not been executed yet, and it is still uninitialized memory.
![](./storage%20bag/Pasted%20image%2020230626145932.png)

### Memory View

^dd3537

During debugging, you can bring up the memory view by navigating to Debug->Windows->Memory->Memory1 in the top navigation bar.
![](./storage%20bag/Pasted%20image%2020230626150626.png)

Enter `&a` to access the memory address of variable a, which is displayed in hexadecimal.

#### Why is it all cc?

This indicates that it is uninitialized stack memory.

Press F10.
![](./storage%20bag/Pasted%20image%2020230626151308.png)

You can see that the data stored in memory has changed. ==_Every two hexadecimal digits represent one byte_==.

If I want to exit the loop, pressing Step Out will exit the entire function. So, I just need to set another breakpoint and press F5 to run to the breakpoint.
![](./storage%20bag/Pasted%20image%2020230626152501.png)