前情提要：[69 Casting in C++](69%20Casting%20in%20C++.md)
_Casting_（强制转换）是我们在 C++中使用的类型之间转换的一种方法，而类型系统是 C++提供给我们的一种保护代码的方法，不是我们必须坚持使用的东西，因为我们愿意的话可以在类型之间自由地转换。

## 1. 认识动态类型转换

而*dynamic casting*是当我们想要做特定类型的类型准换时，作为一种安全机制提供给我们的。`dynamic_cast`是 C++风格的类型转换，仅适用于 C++，不能在 C 语言中使用。它做了额外的工作来确保我们实际的类型转换 _is valid_（有效）的。

是否使用`dynamic_cast`完全取决于你自己，这里只给出一些要点，让你知道什么情况下你应该使用它。

认识到这一点很重要：`dynamic_cast`更像一个函数，它不像编译时进行的类型转换，而是在运行时计算，因此它有相关的运行成本。

`dynamic_cast`是专门用于**沿继承层次结构**进行的强制类型转换，比如我的一个游戏里有一个实体类，它派生出了玩家类和敌人类，如果我想将玩家转换为实体是很简单的，因为玩家本身就是实体对象，可以隐式转换。但如果我想将一个实体类型转换为玩家，编译器会相信我们，如果它并不是一个玩家的话我们就相当于在尝试玩家独有的数据，程序可能会崩溃。因为这个原因，`dynamic_cast`常被用来做验证，如果我们尝试使用它将一个敌人转化为玩家，这个转化会失败，`dynamic_cast`会返回一个 NULL 指针，也就是 0。我们可以用它来检查一个对象是否是给定类型，

## 2. 示例

```cpp
class Entity  // 基类
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
	Entity* e = player;             // 这里直接就隐式转换了

	Entity* e1 = new Enemy();
	Player* p = (Player*)e1;        // 报错，我们需要向编译器保证这是一个Player
}
```

但这样强制转换是很危险的，因为 e1 其实是 Enemy，如果强制转换为 Player，除非 Player 和 Entity 都有 Enemy 的所有成员和函数，程序都会出现问题。

`dynamic_cast`只用于多态类型：
![](./storage%20bag/Pasted%20image%2020230729200942.png)
所以我们需要一个虚函数表，来告诉我们这实际上是一个多态类类型：

```cpp
class Entity
{
public:
	virtual void PrintName(){}  // 见 28虚函数
};
```

测试运行：

```cpp
Player* player = new Player();
Entity* actuallyPlayer = player;
Entity* actuallyEnemy = new Enemy();

Player* p0 = dynamic_cast<Player*>(actuallyEnemy);
Player* p1 = dynamic_cast<Player*>(actuallyPlayer);
```

可以看出 p0 转换失败：

![](./storage%20bag/Pasted%20image%2020230729201539.png)

而 p1 是一个有效的 Entity：

![](./storage%20bag/Pasted%20image%2020230729201636.png)

这就是动态类型转换做的事：如果强制转换有效，就返回你想要的指针，如果它不是你声明的给定类型，转换无效就返回 NULL。

## 3. 它是怎么做到判断的

能做到这一点是因为它储存了*runtime type information*（运行时类型信息，RTTI），这存储着我们的所有类型的运行时类型信息，这会增加一些开销，但它可以让你做到动态类型转换之类的事情。

这里有两件事情需要考虑：
1、RTTI 增加了开销，因为类型需要存储更多关于自己的信息；
2、其次，`dynamic_cast`也需要时间，因为我们需要检查类型信息是否匹配，这个实体是敌人还是玩家，是什么类型的？当我们使用它的时候，必须在**运行时**进行验证，它确实增加了开销。

可以在 VS 中关掉 RTTI：

![](./storage%20bag/Pasted%20image%2020230729202545.png)

运行代码：

![](./storage%20bag/Pasted%20image%2020230729202625.png)

Output 报错：

```text
Access violation reading location 0x8AADD718.
```

可以看到有访问冲突，因为它没有得到类型信息，所以没法返回 NULL。

所以一定要了解动态类型转换的实际含义，因为它们会做一些额外的事情，并且大多数情况下需要开启 RTTI（隐式转换就不会程序崩溃）

除此之外，你还可以像 C#或 Java 一样可以做检查之类的事：

```cpp
Player* p0 = dynamic_cast<Player*>(actuallyEnemy);
if(p0)  // 为了防止以后再转换，一般就不在条件里写完整的转换了
{

}
```
