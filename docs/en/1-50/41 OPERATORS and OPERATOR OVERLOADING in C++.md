## 1. Operators

What is an *operator*? Essentially, it is a symbol that we use to perform certain actions in place of functions. So, we're not just talking about mathematical operators here, but also other commonly used operators like the *dereference* operator, the arrow operator, the `+=` operator, the address-of operator, the left-shift operator (`<<`), and so on.

There are also some things that you might not even consider as operators, such as `new` and `delete`, which are actually operators as well.

In addition, the comma can also be an operator, and so can parentheses.

## 2. Operator Overloading

The term *overloading* essentially means giving new meaning to operators, adding parameters, or creating new behaviors for operators within a program.

At the end of the day, operators are just *functions*. Instead of writing a function name like `add`, you can simply use the `+` operator. In many cases, this can really help make your code cleaner and more readable.

Operator overloading should be used sparingly and only when it makes complete sense.

```cpp
#include <iostream>

struct Vector2
{
	float x, y;

	Vector2(float x, float y)
		: x(x), y(y) {}

	Vector2 Add(const Vector2& other) const
	{
		return Vector2(x + other.x, y + other.y);
	}

	Vector2 Multiply(const Vector2& other) const
	{
		return Vector2(x * other.x, y * other.y);
	}
};

int main()
{
	Vector2 position(4.0f, 4.0f);
	Vector2 speed(0.5f, 1.5f);
	Vector2 powerup(1.1f, 1.1f);

	Vector2 result = position.Add(speed.Multiply(powerup));

	std::cin.get();
}
```

Here, the `result` looks a bit hard to read. In a language like Java, this might be the only way to do it. However, in C++, we have operator overloading, which means we can leverage these operators and define our own.

```cpp
	Vector2 Add(const Vector2& other) const
	{
		return Vector2(x + other.x, y + other.y);
	}

	Vector2 operator+(const Vector2& other) const
	{
		return Add(other);
	}

	Vector2 Multiply(const Vector2& other) const
	{
		return Vector2(x * other.x, y * other.y);
	}

	Vector2 operator*(const Vector2& other) const
	{
		return Multiply(other);
	}
};

int main()
{
	Vector2 position(4.0f, 4.0f);
	Vector2 speed(0.5f, 1.5f);
	Vector2 powerup(1.1f, 1.1f);

	Vector2 result = position + speed * powerup;

	std::cin.get();
}
```

## 3. Left-Shift Operator

```cpp
std::cout <<
```

We can't directly output here because this operator hasn't been overloaded.

![](./storage%20bag/Pasted%20image%2020230709144432.png)

```cpp
std::ostream& operator<<(std::ostream& stream, const Vector2& other)
{
	stream << other.x << "," << other.y << std::endl;
	return stream;
}
```

```cpp
struct Vector2
{
	float x, y;

	Vector2(float x, float y)
		: x(x), y(y) {}

	Vector2 Add(const Vector2& other) const
	{
		return Vector2(x + other.x, y + other.y);
	}

	Vector2 operator+(const Vector2& other) const
	{
		return Add(other);
	}

	Vector2 operator*(const Vector2& other) const
	{
		return Multiply(other);
	}

	Vector2 Multiply(const Vector2& other) const
	{
		return Vector2(x * other.x, y * other.y);
	}

	bool operator==(const Vector2& other) const
	{
		return x == other.x && y == other.y;
	}

	bool operator!=(const Vector2& other) const
	{
		return !(*this == other);
	}
};

std::ostream& operator<<(std::ostream& stream, const Vector2& other)
{
	stream << other.x << "," << other.y << std::endl;
	return stream;
}

int main()
{
	Vector2 position(4.0f, 4.0f);
	Vector2 speed(0.5f, 1.5f);
	Vector2 powerup(1.1f, 1.1f);

	Vector2 result1 = position.Add((speed.Multiply(powerup)));
	Vector2 result2 = position + speed * powerup;

	if (result1 == result2)
		std::cout << result2 << std::endl; // Output
	if (result1 != result2)
		std::cout << result2.x << "," << result2.y << std::endl; // No output
	std::cin.get();
}
```