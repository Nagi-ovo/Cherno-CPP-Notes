# Using Dynamic Libraries in C++

## 1. Dynamic Linking

Dynamic linking occurs at *runtime*, whereas static linking happens at compile time.  
When you compile a static library, you link it into an executable file, i.e., an application, or into a dynamic library. It's like taking the contents of that static library and embedding them into other binary data, either in your dynamic library or in your executable file.

There are many opportunities for optimization because the compiler and linker now fully understand the code that is actually included in the application during static linking (static linking allows more optimizations to take place).  
Dynamic linking, on the other hand, happens at runtime, so your dynamic link library is only loaded when you actually launch your executable. Therefore, it is not actually part of the executable file (an additional file is loaded into memory at runtime).

Now, the executable file needs to have certain libraries, certain dynamic libraries, or certain external files available before it can actually run. This is why, when you launch an application on Windows, you might see an error message pop up: "DLL required," "DLL not found," etc.  
This is a form of dynamic linking. The executable file is aware of the existence of the dynamic link library and treats it as a requirement, even though the dynamic library is still a separate file, a separate module, and is loaded at runtime. You can also completely dynamically load the dynamic library, meaning the executable file has no direct relationship with the dynamic library. However, within your executable, you can search for and load certain dynamic libraries at runtime, obtain function pointers, or access whatever you need from the dynamic library, and then use it.

For dynamic libraries, keep in mind two versions.  
The first is the "static" version of the dynamic library, where my application requires this dynamic link library at runtime, and I already know what functions are inside and what I can use.  
The second version is where I want to arbitrarily load this dynamic library, and I don’t even need to know what’s inside, but I want to extract something or perform many operations.  
Both versions of dynamic libraries have great uses, but let’s focus on the first one: I know my application needs this library, but I want to link it dynamically.

If you compare static and dynamic linking, there are actually some differences in how functions and similar declarations are handled during dynamic linking. However, GLFW, like most libraries, supports both static and dynamic linking using the same header files.

As mentioned in the previous lesson, it is very important to compile both `.dll` and `dll.lib` together because if you try to use a different static library while linking to the DLL at runtime, you might encounter mismatched functions and incorrect memory addresses, causing function pointers to not work properly.

Loading `dll.lib`  
![](./storage%20bag/Pasted%20image%2020230714123416.png)

Build and run the program:  
![](./storage%20bag/Pasted%20image%2020230713214927.png)

The code cannot proceed because `glfw3.dll` was not found. At this point, we need to tell the program where this DLL file is located.  
A simple solution is to place the DLL file in the same location as the executable:  
![](./storage%20bag/Pasted%20image%2020230713215146.png)

Run successfully.