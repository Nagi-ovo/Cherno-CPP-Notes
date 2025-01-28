_enumeration_

The primary purpose of defining an enumeration type: to enhance program readability.

Enumeration values are essentially *integers*.

```cpp
enum Example
{
	A,B,C
};

int a = 0;
int b = 1;
int c = 2;

int main()
{
	Example value = B; // The type is an enum, so the assignment can only be among A, B, C

	if (value == B)
	{
		// Do something here
	}
	std::cin.get();
}
```

By default, the value of the first variable is 0, incrementing sequentially.

![](./storage%20bag/Pasted%20image%2020230703095443.png)

![](./storage%20bag/Pasted%20image%2020230703095529.png)

You can declare the type to save memory space.

```cpp
enum Example : char
{
	A=5,B,C
};
```