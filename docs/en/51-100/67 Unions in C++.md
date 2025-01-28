## 1. Union

A _union_ is somewhat similar to a class or a struct, except that it can only occupy the memory of one member at a time. 
Typically, if we have a struct with 4 floats declared inside it, it would occupy 4x4 bytes, totaling 16 bytes in the struct. 
However, a union can only have one member, so if I declare 4 floats, say a, b, c, d, the size of the union remains 4 bytes. When I try to manipulate them, such as setting a to 5, their memory is the same, and the value of d will also be 5. This is how a union works.

You can use them just like structs or classes, and you can also add static functions or regular functions/methods to them. However, you cannot use virtual methods, and there are some other limitations. But usually, what people use unions for is closely related to [type punning](66%20Type%20Punning%20in%20C++.md). It's really useful when you want to give the same variable two different names.

Typically, `union` is used anonymously, but an anonymous union cannot contain member functions.

## 1. Use Cases

Here we have two different methods to handle the same memory:

### a. Dereferencing Pointers

```cpp
struct Union
{
	union
	{
		float a;
		int b;
	};
};

Union u;
u.a = 2.0f;
std::cout << u.a << "," << u.b << std::endl;

```

This will output 2 and a string of numbers. Actually, 107... is the byte representation of the float 2. It's as if we took the memory that makes up the float and interpreted it as an integer, which is type punning.

![](./storage%20bag/Pasted%20image%2020230725173306.png)

Let's look at a more useful example:

```cpp
struct Vector2
{
	float x, y;
};

struct Vector4
{
	float x, y, z, w;
};

void PrintVector(const Vector2& vector)
{
	std::cout << vector.x << "," << vector.y << std::endl;
}
```

We can see that Vector4 is essentially two Vector2s. We can cast the memory address of x to Vector2 and then dereference it:

```cpp
struct Vector4
{
	float x, y, z, w;

	Vector2& GetA()
	{
		return *(Vector2*)&x;
	}
};

int main()
{
	Vector4 e={1,2,3,4};
	std::cout << e.GetA().y << std::endl;  // 2
	std::cin.get();
}
```

### b. Union

Another method is to use `union`:

```cpp
struct Vector4
{
	union
	{
		struct
		{
			float x, y, z, w;
		};
	};
};
// Here we can still access Vector4.x normally because we didn't name the struct; it's anonymous, just a data structure.
```

Let's add another struct member:

```cpp
struct Vector4
{
	union
	{
		struct
		{
			float x, y, z, w;
		};

		struct
		{
			Vector2 a, b;
		};
	};
};
```

Here, a and x, y share the same memory, and b and z, w share the same memory. There are two ways to read this:

```cpp
int main()
{
	Vector4 vector = { 1.0f,2.0f,3.0f,4.0f };
	PrintVector(vector.a);

	PrintVector(vector.b);
	vector.z = 500.f;
	PrintVector(vector.b);

	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230725201340.png)
Here, we didn't set b.x=500, but rather vector.z. This z variable corresponds to b.x because it occupies the same memory, so z corresponds to the x of Vector2.

## 3. Summary

`Union` is really useful when you want to do something like this: when you want to handle the same data in multiple ways.
You can also use type punning or other methods, but usually `union` is more readable.