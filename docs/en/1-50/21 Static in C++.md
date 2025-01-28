# Inside and Outside of Classes (struct, class), Instantiation Refer to [Previous Chapter](18%20CLASSES%20in%20C++.md#^b700f7)

| Outside the Class                                                                 | Inside the Class                                                                                  |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Symbols modified are local during the linking phase, visible only to the compilation unit (.obj) where they are defined | This part of memory is shared by all instances of the class. Multiple instantiations will still result in only one instance of the static variable (see next chapter) |

^e0f8b6

Even if you instantiate this class or struct many times, there will only be one instance of that *static* variable. The same applies to *static methods* inside the class; these methods do not have an instance pointer (_this_).

Static variables are stored in the static storage area, not on the stack or heap. They exist throughout the entire execution of the program and have only one instance.

A static variable or function means that when *linking* to its actual definition, the *linker* will not find its definition outside of this compilation unit (.obj), somewhat similar to the *private* attribute of a class.

```cpp
// Static.cpp
static int s_Variable = 5;  // s stands for static

// Main.cpp
#include <iostream>

int s_Variable = 10;

int main()
{
	std::cout << s_Variable << std::endl;   // 10
	std::cin.get();
}
```

```cpp
// Static.cpp
int s_Variable = 5;  // remove static

// Main.cpp
#include <iostream>

int s_Variable = 10;

int main()
{
	std::cout << s_Variable << std::endl;   // LNK ERROR already defined in Main.obj
	std::cin.get();
}
```

Therefore, two global variables cannot have the same name.

### Solution 1: extern link

*extern* will look for the definition of s_Variable in another compilation unit, known as *external linkage or external linking*.

```cpp
// Static.cpp
int s_Variable = 5;

// Main.cpp
extern int s_Variable;   // It is a reference to the variable

std::cout << s_Variable << std::endl;  // 5
```

This means that the functions and variables you define are only "visible" to the cpp file (compilation unit) where they are declared.
Using *global* is not recommended as it can easily lead to bugs.