三元运算符，其实就是一个`?`和一个`:` , 只是*if*语句的语法糖而已

## 1. 一般使用
```cpp
if (s_Level > 5)
		s_Speed = 10;
else
	s_Speed = 5;
```
等同于
```cpp
s_Speed = s_Level > 5 ? 10 : 5;
```

同样
```cpp
std::string rank = s_Level > 10 ? "Master" : "Beginner";

/* ------------------------  */ 

std::string otherRank;
if (s_Level > 10)
	otherRank = "Master";
else
	otherRank = "Beginner";
```

这里的代码和上面不同，而且技术上来说会更慢，因为你创建了一个临时字符串然后又立即销毁它。
而这里的三元运算符没有构造中间字符串的原因实际上与*return value optimization*返回值优化有关(一种高级编译器特性，是一种优化方式),后续会提到。

现在只需要知道这样写代码更整洁了，个人看法这么写速度也会更快

## 2. 嵌套
```cpp
s_Speed = s_Level > 5 ? s_Level > 10 ? 15 : 10 : 5;  // 三元运算嵌套
```
如果大于5，又大于10，设为15，否则设为10，再否则设为5
```cpp
s_Speed = s_Level > 5 && s_Level < 100 ? s_Level > 10 ? 15 : 10 : 5;
```
越来越疯狂了，不用多想，没太多意义，尽量不要这么写。