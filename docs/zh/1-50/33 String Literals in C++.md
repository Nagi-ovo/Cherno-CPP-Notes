字符串字面量

![](./storage%20bag/Pasted%20image%2020230705140428.png)

为什么大小是 7？因为还有一个`00`的额外的[空终止符](<32%20How%20Strings%20Work%20in%20C++%20(and%20how%20to%20use%20them).md#^26e746>)：`"Cherno\0"`

![](./storage%20bag/Pasted%20image%2020230705140940.png)
两个`.`代表`00`的位置

![](./storage%20bag/Pasted%20image%2020230705141715.png)

这个字符串是存储在二进制文件的 const 部分
用 16 进制编辑器打开，可以看到二进制文件中有"Cherno",这些字符被嵌入到二进制文件中了。当我们引用时，它实际指向一个不允许编辑的常量数据块。
![](./storage%20bag/Pasted%20image%2020230705142330.png)

```cpp
const char* name = "Cherno"
name[2] = 'a';
```

在 Release 模式下运行修改字符串，也不会发生改变。而 Debug 模式下会得到一个异常。

### wide char

```cpp
const char* name = u8"Cherno";
const wchar_t* name2 = L"Cherno";  // L表明后面的字符串字面量是由宽字符组成的
								   // 2 bytes

//C++11引入
const char16_t* name3 = u"Cherno";   // 16 bits = 2 bytes
const char32_t* name4 = U"Cherno";   // 32 bits = 4 bytes
```

#### wchar_t 和 char16_t 的区别？

虽然我们一直说 wchar 每个字符都是 2 字节，但实际上是由编译器决定的。（Windows：2 bytes，Linux：4 bytes）。
如果你希望它一直是 2 bytes，你可以用`char16_t`

### R 方法

字符串前面加上`R`代表忽略转义符，`R`代表*raw*

![](./storage%20bag/Pasted%20image%2020230705144029.png)

字符串字面量总是存储在只读内存中。
