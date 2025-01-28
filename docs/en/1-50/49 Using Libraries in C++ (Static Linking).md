# Using Libraries in C++ (Static Linking)

If you've used other languages like Python or C#, adding libraries is a straightforward task. You might use a package manager or something similar. However, in C++, it seems like everyone struggles with it. It looks difficult, but in reality, it's quite simple.

This tutorial will focus on linking libraries in the form of binary files, rather than fetching the actual source code of the dependency library and compiling it yourself. Specifically, we'll be using the *GLFW library*.

In your actual project or the library you want to link, binary files might not be available. Therefore, you might be forced to build it yourself, especially for Mac and Linux users. In a more professional, large-scale project, if you have enough time, it's better to compile it yourself as it aids in debugging. If you want to modify the library, you can make slight changes. In such cases, Cherno prefers to compile the source code directly within the Visual Studio project.

## 1. 32-bit or 64-bit?

[Download | GLFW](https://www.glfw.org/download.html)

Do I want 32-bit or 64-bit binaries?  
This has nothing to do with your actual operating system. If you're using Windows 10, a 64-bit OS, it doesn't mean you should get 64-bit binaries. You should choose based on your target application.  
So, if I compile my application as an X86 (win32) program, I need 32-bit binaries; if I compile a 64-bit application, I need 64-bit binaries—they must match, otherwise, they won't link.

Here, I choose to download the 32-bit version. After unzipping, you can see a typical file layout (a typical organizational structure for C++ libraries). Libraries usually consist of two parts: includes and library, which include directories and library directories.
![](./storage%20bag/Pasted%20image%2020230713192127.png)

The _include_ directory contains a bunch of header files we need to use the functions in the pre-built binaries. The *lib* directory contains those pre-built binaries.  
There are usually two parts: dynamic libraries and static libraries (not all libraries provide both, but GLFW does). You can choose between **static linking** and **dynamic linking**.

## 2. Static vs. Dynamic Linking

Here's a brief explanation of the difference:

### Static Linking

Static linking means the library is included within your executable file (it's inside your .exe file, or the executable file on other operating systems).

### Dynamic Linking

Dynamic linking libraries are linked at runtime. You still have some linking, and you can choose to load the dynamic link library during program execution. There's a function called *LoadLibrary* in the Windows API, for example. It loads your dynamic library, allowing you to pull out functions and start calling them. You can also load your DLL file when the application starts—this is your *Dynamic Link Library*.

The main difference is whether the library file is compiled into the .exe file or linked to the .exe file, or if it's a separate file at runtime that you need to place alongside your .exe file or somewhere else, so your .exe file can load it. Because of this dependency, you need to keep the .exe and .dll files together.

So, static linking is generally preferred. Static linking is technically faster because the compiler or linker can perform link-time optimizations. Static linking can produce faster applications because several optimization methods can be applied since we know which functions to link at link time. For dynamic libraries, we don't know what will happen and must keep them intact. When the dynamic link library is loaded by the running program, parts of the program will be completed.

Therefore, **static linking is usually the better choice**.

![](./storage%20bag/Pasted%20image%2020230713194706.png)

## 3. Static Linking Example

We create a Dependencies folder in the directory where the Solution file is located to hold the dependencies. Inside it, we create a GLFW folder and place the unzipped files here.
![](./storage%20bag/Pasted%20image%2020230713194735.png)

This includes many library files compiled with different compilers, such as MinGW, and various versions of Visual Studio. Here, we choose the latest one. The choice doesn't really matter because, ultimately, they are just compiled binary files, and any of them will work. But we want to use the one most compatible with our current *toolchain*.

Here, we include the include directory and the selected version.
![](./storage%20bag/Pasted%20image%2020230713195245.png)

Opening lib-vc2022, we see the following files:
![](./storage%20bag/Pasted%20image%2020230713195344.png)

- `glfw3.dll` is a runtime dynamic link library, used when we dynamically link at runtime.
- `glfw3dll.lib` is actually a static library used in conjunction with glfw3.dll, so we don't have to query the DLL for a bunch of function pointers pointing to all these functions. This means the .lib file contains the locations of all functions and symbols in glfw3.dll, so we can link them at compile time.  
  If we didn't have this .lib file, we could still use the .dll file, but we would need to access the functions inside the .dll by **function name** (e.g., GLFW_INIT). However, this .lib file contains the locations of all these functions, allowing the linker to link directly to them.
- `glfw3.lib` is much larger than the others. If we don't want to link at compile time, we link this .lib file. If we do this, we won't need the .dll file when the .exe runs.

First, in the C/C++ General settings, under Additional Include Directories, we specify the additional include directory. Don't forget to set your configuration and platform; here, we set it to All Configurations.
![](./storage%20bag/屏幕截图%202023-07-13%20200644.jpg)
The include directory is the actual directory of the include folder:
![](./storage%20bag/Pasted%20image%2020230713200941.png)

I could directly copy this directory, but it's clear that it looks something like this:

```text
C:\Dev\HelloWorld\Dependencies\GLFW\include
```

This is specific to the current path on my computer. If someone clones this from GitHub or elsewhere, the code won't compile if the path remains the same.  
What we really want is a path relative to the actual directory, and HelloWorld is the directory of my solution:
![](./storage%20bag/Pasted%20image%2020230713201322.png)

Starting from this solution, we can use a VS *macro*:
![](./storage%20bag/Pasted%20image%2020230713201511.png)

```cpp
$(SolutionDir)Dependencies\GLFW\include // Note that the macro comes with a '\'
```

What we can do now is include the relevant files in this directory (include) relative path. This directory contains the GLFW folder, which has a file called glfw3.h, so we can write:

```cpp
#include "GLFW/glfw3.h" // Compiles fine
```

Since this is a compiler-specified include path, I can also use angle brackets: `#include <GLFW/glfw3.h>`.  
This brings up the question of whether to use quotes or angle brackets. In practice, there's no difference because if you use quotes, it first checks the relative path. If it doesn't find anything relative to this file (i.e., relative to main.cpp), it checks the compiler's include paths.

A reference choice method:

- If the source file is in Visual Studio (somewhere in the solution, maybe in another project, it doesn't matter, as long as it's in this Solution), then use `" "`.
- If it's a completely external dependency or an external library, not compiled with my actual solution in Visual Studio, then use `< >` to indicate that it's actually external.

```cpp
int a = glfwInit();  // Compiles successfully, but build fails
```

It shows *unresolved external symbol*:
![](./storage%20bag/Pasted%20image%2020230713205445.png)  
This means you haven't linked to the actual library; the linker can't find the glfwInit function.

Modify the Linker settings to set the directory of the .lib file, specifying a library directory.
![](./storage%20bag/Pasted%20image%2020230713210033.png)

Then specify the library file name relative to that library directory.
![](./storage%20bag/Pasted%20image%2020230713210216.png)

Now the build succeeds.

We print the result to the console:

```cpp
#include <iostream>
#include <GLFW/glfw3.h>

int main()
{
	int a = glfwInit();
	std::cout << a << std::endl;  // 1, indicating success

	std::cin.get();
}
```

If we remove the `include` and input the actual declaration of glfwInit:

```cpp
#include <iostream>
//#include <GLFW/glfw3.h>

int glfwInit();

int main()
{
	int a = glfwInit();
	std::cout << a << std::endl;

	std::cin.get();
}
```

This idea works, but in this specific example, we get an error. The GLFW library is actually a C library, and we're using C++ here, which causes name mangling.

We need to add `extern "C"` before the function declaration:

```cpp
extern "C" int glfwInit();
```

This means keeping the name as it is because you're linking to a library built in C. Running it successfully also outputs "1," the same result we got when we had the header file.  
So remember, linking libraries or header files isn't some magical process; it's just connecting all the parts of the system together. Header files provide declarations, telling us which functions are available, and library files provide definitions, allowing us to link to those functions and execute them correctly when calling functions in C++.