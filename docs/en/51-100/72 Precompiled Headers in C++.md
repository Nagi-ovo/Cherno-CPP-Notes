This section will cover C++'s *precompiled headers* (PCH), discussing what they are, why you should use them, and then diving into how to set them up in Visual Studio and gcc/g++, followed by a simple example to see the practical benefits.

## 1. What is a Precompiled Header?

A precompiled header essentially allows you to take a bunch of header files and convert them into a format that the compiler can use without having to read through these headers repeatedly.  
For example, every time you `#include <vector>` in a C++ file, it needs to read the entire Vector header file and compile it. Moreover, Vector includes a bunch of other header files, which also need to be read. The preprocessor has to copy all of this into the Vector file, resulting in over 100,000 lines of code that need to be parsed, marked, and compiled before you can even start compiling your main file. If your main file includes Vector, then Vector must be copied and pasted into the main file, and all of this code needs to be parsed and compiled every single time. The key point is that every time you modify a C++ file, even if it's just adding a space, the entire file has to be recompiled. So, the Vector file must be copied and pasted into your C++ file, and everything has to be parsed and compiled from scratch. Not only that, but if you have multiple files in your project that all include Vector, you end up parsing the same code over and over again, which takes a lot of time.

This is where **precompiled headers** come in. They allow you to take a bunch of header files (essentially a chunk of code) and compile them only once, storing the result in a binary format that is much faster for the compiler to process than plain text. This way, instead of parsing the entire Vector file every time, the compiler only needs to look at the precompiled header, which is already in a fast and easily usable binary format. This significantly speeds up compilation time, especially as your project grows larger, with more C++ files and more header files. You can add more content to the precompiled header, and as more source files use common headers, the compilation process becomes exponentially faster.

So, if you care about compilation time, you should definitely use precompiled headers.

However, there are some things you **should not** do with precompiled headers:  
The precompiled headers mentioned so far are still essentially header files that include a bunch of other headers. Therefore, you might be tempted to put everything in your project into the precompiled header, thinking it will make the build process lightning fast.

While this is true, if you put things into the precompiled header that are subject to change, and in real-world projects, things do change, you will have to rebuild the precompiled header, which takes time and could slow down the compilation process. So, **do not** put files that change frequently into the precompiled header.

That said, precompiled headers are still very useful, and it's fine to include your own project files in them. For example, it's perfectly fine to include a `Log.h` file that doesn't need to be modified, as this file is commonly used and convenient to have. You don't need to manually include Log in every C++ file in your project. However, if Log is subject to change, it's not suitable for the precompiled header, as it would need to be recompiled every time.

The real value of precompiled headers lies in external dependencies. Essentially, they are most useful for code that you didn't write, such as STL, Windows API, etc. For example, if you `#include <windows.h>`, which is a massive header file containing many other headers, you won't be modifying `windows.h` or STL, so there's no reason not to include them in the precompiled header. Their code might be many times larger than your actual project code, and having to compile them every time for every C++ file would be a nightmare. Since you're unlikely to modify them, it makes sense to include them in the precompiled header and forget about them.

## 2. Dependency Management

What PCH (precompiled headers) actually do is bundle everything together, which can obscure what is actually being used and affect readability. For example, if only a few files need to use a window library like GLFW, there's no need to include all the dependencies in the PCH. If you look at a single cpp file, you won't know what dependencies it requires, and when you import it into other files, it becomes harder to understand what it depends on. However, if you include the actual dependencies via `#include`, it becomes clear what each file needs. If you only include the PCH, and the PCH contains many includes, it can become messy.

So, **do not put all dependencies in the PCH**, because including the actual dependencies makes the code easier to read. What should go into the PCH are things like STL, because strings, vectors, and `std::cout` are used in many places, and you don't want to compile them every time. GLFW, on the other hand, might only need to be compiled once.

## 3. Examples

### For Visual Studio

We need to create a cpp file that includes the header files, then edit its properties (and clear the value on the second line):
![](./storage%20bag/Pasted%20image%2020230729134922.png)

Then, go to the project properties, set it to "Use" and specify the file name (make sure to select all platforms):
![](./storage%20bag/Pasted%20image%2020230729135113.png)

Then build the entire project. You can modify the settings in Tools to make VS display build times:
![](./storage%20bag/Pasted%20image%2020230729135926.png)

Build times without PCH and subsequent build times:
![](./storage%20bag/Pasted%20image%2020230729140124.png)

![](./storage%20bag/Pasted%20image%2020230729140246.png)

Build times with PCH and subsequent build times:
![](./storage%20bag/Pasted%20image%2020230729140351.png)

![](./storage%20bag/Pasted%20image%2020230729140425.png)

You can see that builds with PCH are much faster.

### For g++

Windows users can use Cygwin to simulate a Unix environment or directly use Windows' timing functionality:

```PowerShell
Measure-Command { g++ -std=c++11 Main.cpp }
```

![](./storage%20bag/Pasted%20image%2020230729142217.png)

Create the precompiled file:

```PowerShell
g++ -std=c++11 pch.h
```

This generates a `pch.h.gch` file, which is a massive 100MB file:

![](./storage%20bag/Pasted%20image%2020230729142104.png)

Delete `a.exe` to simulate a clean build, then time it again:

![](./storage%20bag/Pasted%20image%2020230729142132.png)

You can see that it's about six times faster.

### Summary

Hopefully, these examples provide some insight.  
To recap, why use precompiled headers? They speed up compilation time and make writing code more convenient, as you don't need to repeatedly include common headers. Unless it's a very small sandbox project, every project should use PCH. However, what you put inside it is another story.