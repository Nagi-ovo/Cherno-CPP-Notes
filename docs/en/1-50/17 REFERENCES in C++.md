## 1. Relationship with Pointers

In fact, a _reference_ is just an extension of a pointer, a kind of *syntax sugar* based on pointers, designed to make code easier to read and write. As the name suggests, a reference is a way to refer to an existing variable. There is nothing that a *reference* can do that a *pointer* cannot.

[Unlike pointers](16%20POINTERS%20in%20C++.md#^646396) (where you first create a pointer variable and then assign it nullptr, etc.), a *reference* must refer to an existing variable. The reference itself is not a new variable and does not actually occupy memory.

## 2. Defining References

This is achieved through `type&`, where the `&` is part of the type. Therefore, the presence of `&` does not necessarily mean taking an address or being a reference; it depends on the *context*.

![](./storage%20bag/Pasted%20image%2020230701182509.png)

In any case, `ref` is `a`. We are simply creating an *alias* for `a` to make the code easier to write.

## 3. Example

```cpp
void Increment(int value)
{
	// int value = 5;
	value++;
}

int main()
{
	int a =5;
	Increment(a);
	LOG(a); // 5
}
```

Here, we are using *passing by value*, not `int&` or `int*`. Therefore, a new variable is copied with the value `5`, and `a` is not changed.

What we need is *passing by reference* to increment the variable.

![](./storage%20bag/Pasted%20image%2020230701183658.png)
As shown in the image above, first dereference, then increment the value at that address. However, this looks cumbersome, so we can use the following approach:

#### Using References

![](./storage%20bag/Pasted%20image%2020230701183849.png)
The code is clearer and more concise, enhancing readability.

## 4. Other Notes

Once you declare a reference, you cannot change the object it refers to.

```cpp
int a = 5;
int b = 8;

int& ref = a;
ref = b;  // a=8,b=8
```

Additionally, once declared, it must be immediately assigned because it is a reference to a variable, not an actual variable.

If you want to modify the reference, you can do so through pointers (pointers can change the object they point to, while references cannot).
![](./storage%20bag/Pasted%20image%2020230701185029.png)