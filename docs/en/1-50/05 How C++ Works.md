## 1. Preface

I configured `.vssettings` and `VsVim`, but I couldn't get the `imap jj <Esc>` mapping to work in Ob. At this point, I decided to just start learning.  
(The next day, I found that the mapping worked after a restart...)  
A follow-up after coming back from Lesson 25: Cherno uses Visual Assist in the video, but the official price isn't friendly for domestic users. However, you can install the JetBrains ReSharper C++ plugin in VS, and you can get it for free with an educational email. It's amazing!

## 2. Basic Concepts

### 2.1 Header Files

Lines starting with `#` are called *preprocessor statements*, or preprocessor directives.  
These directives are processed before the actual compilation.  
When the compiler receives a source file, the first thing it does is preprocess all the preprocessor directives.

```cpp
#include <iostream>
```

This means finding the `iostream` file and copying all its contents into the current file.  
These included files are generally called *header files*.

Every C++ program has something like a `main` function, which is called the *entry point*.  
Later, I learned that this is necessary because an `.exe` executable file must have an entry point, which can be customized in the settings (it doesn't necessarily have to be the `main` function).

Only the main function can return no value, and by default, it returns 0.

After the *preprocessor statements* are evaluated, our file is compiled. During this phase, the compiler converts our C++ code into actual machine code.

### 2.2 Visual Studio Related

![](./storage%20bag/Pasted%20image%2020230621232703.png)

> *Configuration* is a set of rules for how to build a project.

![](./storage%20bag/Pasted%20image%2020230621232713.png)

> *Solution platform* is the target platform for our current compilation. For example, `x86` means generating a 32-bit program for Windows. If you need to compile for Android, you would change it to the relevant Android settings.

To modify our configuration, right-click on the project and select *Properties*, which will bring up the following interface:  
![](./storage%20bag/Pasted%20image%2020230621233202.png)

> _==Note==_: Make sure the *Active* configuration is the one you want to modify, as it might not be by default.

### 2.3 Linker

All `.cpp` files are compiled, while `.h` header files are not compiled directly. Instead, they are included in `.cpp` files and then compiled.  
Each `.cpp` file is compiled into an *Object* file (`.obj`). All `.obj` files are then linked together to form an `.exe` file.

*Compile* compiles a single `.cpp` file. The shortcut is ==Ctrl+F7==.

_==Note==_: The error list isn't very useful. It works by *parsing* the output window, looking for the keyword `error`, and then extracting information from there to populate the list. It should only be used as an overview.  
For detailed and complete error information, you must rely on the output window.

Double-clicking on an error in the output window will jump to the corresponding line in the code.

### 2.4 Declaration

The compiler cannot recognize functions defined in another `.cpp` file, so it reports compilation errors. This can be resolved by providing a *declaration*.

| Declaration  | Definition                 |
| ------------ | -------------------------- |
| Declares the existence of a function | Defines what the function is, including its body |
| `void Log(x)`  | `void Log(x){ code... }`      |

After the files are compiled, the linker will look for the function definitions and link them to the calls in `main`. If it can't find a definition, you'll get a linker error.  
Only the main function can return no value, and by default, it returns 0.

After the *preprocessor statements* are evaluated, our file is compiled. During this phase, the compiler converts our C++ code into actual machine code.