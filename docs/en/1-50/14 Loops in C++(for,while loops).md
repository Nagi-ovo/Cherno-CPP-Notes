## 1. for loops

^ebdf13

The parentheses following a *for loop* contain three parts, separated by semicolons.

- Variable declaration, defined before the loop starts
- Loop condition, which is a boolean; if true, the loop body is executed
- Operation to be performed before the next iteration of the loop, executed after the loop body, followed by the evaluation of the loop condition

```cpp
for (int i = 0;i < 5;i++)
{

}

\\Equivalent to

int i = 0;
bool condition = true;
for (;condition;)
{
	i++;
	if (!(i < 5))
		condition = false;
}
```

## 2. while loops

```cpp
while (i < 5)
{
	i++;
}
```

## 3. Choosing between for and while

- **while**: Use when the condition is already defined and does not need to be modified with each iteration. No need to define a variable before the loop since the boolean condition is already declared.
- **for**: Use for iterating over arrays, when the size is known, and when you need to access indices. The variable `i` can be conveniently used for this purpose.

## 4\* do while loops

Executes the loop body at least once, as shown in the image below:
![](./storage%20bag/Pasted%20image%2020230627210926.png)