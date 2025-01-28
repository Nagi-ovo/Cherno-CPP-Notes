# Preface: [69 Casting in C++](69%20Casting%20in%20C++.md)

_Casting_ is a method we use in C++ to convert between types, and the type system is a way C++ provides to protect our code. It's not something we must strictly adhere to, as we can freely convert between types if we wish.

## 1. Understanding Dynamic Casting

_Dynamic casting_ is a safety mechanism provided when we want to perform type conversions of specific types. `dynamic_cast` is a C++-style type conversion and is only applicable in C++; it cannot be used in C. It performs additional work to ensure that our actual type conversion _is valid_.

Whether to use `dynamic_cast` is entirely up to you. Here are some key points to help you understand when you should use it.

It's important to recognize that `dynamic_cast` is more like a function. Unlike type conversions performed at compile time, it is computed at runtime, thus incurring associated runtime costs.

`dynamic_cast` is specifically used for **casting along the inheritance hierarchy**. For example, in one of my games, there is an `Entity` class, from which `Player` and `Enemy` classes are derived. If I want to convert a `Player` to an `Entity`, it's straightforward because a `Player` is inherently an `Entity` object and can be implicitly converted. However, if I want to convert an `Entity` type to a `Player`, the compiler will trust us. If it's not actually a `Player`, we would be attempting to access `Player`-specific data, which could cause the program to crash. For this reason, `dynamic_cast` is often used for validation. If we try to use it to convert an `Enemy` to a `Player`, the conversion will fail, and `dynamic_cast` will return a `NULL` pointer, i.e., `0`. We can use it to check if an object is of a given type.

## 2. Example

```cpp
class Entity  // Base class
{
public:
};

class Player : public Entity
{
public:
};

class Enemy : public Entity
{
public:
};

int main()
{
	Player* player = new Player();
	Entity* e = player;             // Implicit conversion here

	Entity* e1 = new Enemy();
	Player* p = (Player*)e1;        // Error, we need to assure the compiler this is a Player
}
```

However, such a forceful cast is dangerous because `e1` is actually an `Enemy`. If we forcefully cast it to a `Player`, unless `Player` and `Entity` have all the members and functions of `Enemy`, the program will encounter issues.

`dynamic_cast` is only used for polymorphic types:
![](./storage%20bag/Pasted%20image%2020230729200942.png)
So we need a virtual function table to indicate that this is actually a polymorphic class type:

```cpp
class Entity
{
public:
	virtual void PrintName(){}  // See 28 Virtual Functions
};
```

Test run:

```cpp
Player* player = new Player();
Entity* actuallyPlayer = player;
Entity* actuallyEnemy = new Enemy();

Player* p0 = dynamic_cast<Player*>(actuallyEnemy);
Player* p1 = dynamic_cast<Player*>(actuallyPlayer);
```

We can see that `p0` conversion fails:

![](./storage%20bag/Pasted%20image%2020230729201539.png)

While `p1` is a valid `Entity`:

![](./storage%20bag/Pasted%20image%2020230729201636.png)

This is what dynamic casting does: if the cast is valid, it returns the desired pointer; if it's not of the declared type, the conversion is invalid and it returns `NULL`.

## 3. How It Determines Validity

It achieves this by storing _runtime type information_ (RTTI), which holds runtime type information for all our types. This adds some overhead, but it allows you to perform tasks like dynamic casting.

There are two things to consider here:
1. RTTI adds overhead because types need to store more information about themselves.
2. Additionally, `dynamic_cast` also takes time because we need to check if the type information matches. Is this entity an `Enemy` or a `Player`? What type is it? When we use it, we must perform validation at **runtime**, which indeed adds overhead.

You can disable RTTI in VS:

![](./storage%20bag/Pasted%20image%2020230729202545.png)

Run the code:

![](./storage%20bag/Pasted%20image%2020230729202625.png)

Output error:

```text
Access violation reading location 0x8AADD718.
```

You can see there's an access violation because it didn't get the type information, so it couldn't return `NULL`.

Therefore, it's essential to understand the actual implications of dynamic casting because they do some extra things, and in most cases, RTTI needs to be enabled (implicit conversion won't crash the program).

Additionally, you can perform checks similar to C# or Java:

```cpp
Player* p0 = dynamic_cast<Player*>(actuallyEnemy);
if(p0)  // To prevent future conversions, generally avoid writing the full conversion in the condition
{

}
```