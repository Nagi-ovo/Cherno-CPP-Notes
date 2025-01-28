The ternary operator is essentially a `?` and a `:`, which is just syntactic sugar for an *if* statement.

## 1. General Usage
```cpp
if (s_Level > 5)
	s_Speed = 10;
else
	s_Speed = 5;
```
is equivalent to
```cpp
s_Speed = s_Level > 5 ? 10 : 5;
```

Similarly,
```cpp
std::string rank = s_Level > 10 ? "Master" : "Beginner";

/* ------------------------  */ 

std::string otherRank;
if (s_Level > 10)
	otherRank = "Master";
else
	otherRank = "Beginner";
```

The code here is different from the above, and technically, it is slower because you create a temporary string and then immediately destroy it.
The reason why the ternary operator here does not construct an intermediate string is actually related to *return value optimization* (an advanced compiler feature, which is an optimization technique), which will be discussed later.

For now, just know that writing code this way is cleaner, and in my opinion, it will also be faster.

## 2. Nesting
```cpp
s_Speed = s_Level > 5 ? s_Level > 10 ? 15 : 10 : 5;  // Nested ternary operator
```
If greater than 5, and also greater than 10, set to 15, otherwise set to 10, and if not greater than 5, set to 5.
```cpp
s_Speed = s_Level > 5 && s_Level < 100 ? s_Level > 10 ? 15 : 10 : 5;
```
This is getting increasingly crazy, don't overthink it, it doesn't make much sense, try not to write it this way.