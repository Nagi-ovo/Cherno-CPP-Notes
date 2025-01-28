## 1. Variable Types

In C++, the ==only difference== between different variable types is their ==_size_==, i.e., how much memory the variable occupies.

The actual size of a data type depends on the compiler, and it may vary due to different compilers.

### 1.1 int

The `int` type is designed to store integers within a certain range, as it has a size of 4 bytes.

$1byte=8bits,4bytes=32bits$

Variables are ==signed==, meaning one bit is used to represent the sign ($\pm$), leaving only 31 bits for the actual number representation.
1 bit can be either "0" or "1", $2^{31}=2,147,483,648$ (over 2.1 billion). Since 0 also needs to be represented, the maximum number that can be represented is $2^{31}-1$.

$\therefore$ The range of `int` is $(-2147483648 , 2147483647)$.

#### What if I only want positive numbers?

$\ce { -> }$ Use an unsigned number, which can represent $2^{32}$ ^7a7e3b

```cpp
unsigned int
```

### 1.2 Common Types

| char   | short   | int     | long    | long long | (long int) |
| ------ | ------- | ------- | ------- | --------- | ---------- |
| 1 byte | 2 bytes | 4 bytes | 4 bytes | 8 bytes   | 4 bytes    |

Any type can be prefixed with [`unsigned`](08%20Variables%20in%20C++.md#^7a7e3b).

### 1.3 char

Making assumptions about certain data types.

```cpp
char a = 'A';  // A

char a = 65;   //  A
```

Because when a `char` is passed to `std::cout`, it is treated as a character rather than a number.

```cpp

short a = 65;  // 65

short a = 'A'; // 65
```

### 1.4 Storing Decimal Numbers

#### float & double

`float` occupies 4 bytes and is distinguished from `double` by appending "F/f" to the number.
`double` occupies 8 bytes.
![](./storage%20bag/Pasted%20image%2020230625003726.png)
![](./storage%20bag/Pasted%20image%2020230625003951.png)
![](storage%20bag/Pasted%20image%2020230625003951.png)

### 1.5 bool

0 for false
anything except 0 for true

Occupies 1 byte.

Since memory addressing cannot directly access bits but only bytes, you can cleverly store 8 bools in one byte to save memory.

## 2. sizeof Operator

```cpp
std::cout << sizeof(bool) << std::endl;   // 1
```

## 3. Pointers & References

Pointers: type\* `bool*`

References: type& `bool&`