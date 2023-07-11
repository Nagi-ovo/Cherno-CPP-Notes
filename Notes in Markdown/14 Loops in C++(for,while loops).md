## 1. for loops

^ebdf13

*for loops*后面的括号里有三部分，用分号隔开。
- 变量声明，循环开始前定义
- 循环条件，会是一个boolean，若为true则进入循环部分
- 下次for循环前会执行的操作，循环部分结束后执行，接着判断循环条件
```cpp
for (int i = 0;i < 5;i++)
{
	
}

\\等价于

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


## 3. 用for还是while

- while：只要条件而且不用每次循环都改变条件，循环前不需要定义变量，因为条件的boolean已经声明好了
- for : 遍历数组，大小确定，需要访问的索引，i正好可以用

## 4*  do while loops

至少执行循环部分一次，如图
![](Pasted%20image%2020230627210926.png)