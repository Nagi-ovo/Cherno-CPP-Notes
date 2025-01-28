# Creating and Using Libraries in C++

This lesson primarily focuses on how to set up multiple projects in Visual Studio and how to create a library that can be used across all projects. This is a crucial point, especially if your project is large in scale. It not only helps you create modules or libraries using code and reuse them multiple times but also allows you to mix languages.

## 1. Adding Projects

[13 BEST Visual Studio Setup for C++ Projects!](13%20%20BEST%20Visual%20Studio%20Setup%20for%20C++%20Projects!.md) Please refer to this lesson to configure the first project, "Game".
Then, right-click on the Solution to create a second project:

![](./storage%20bag/Pasted%20image%2020230714135723.png)

![](./storage%20bag/Pasted%20image%2020230714135807.png)

After creation, the directory should look like this:

![](./storage%20bag/Pasted%20image%2020230714135939.png)

> Ensure that the configuration type of the Game project is set to an executable file:

Since we are going to statically link, the configuration type of the Engine should be set to a static library:
![](./storage%20bag/Pasted%20image%2020230714140145.png)

If I want to use this namespace, there are two methods:

- Relative Path:

```cpp
#include "../../Engine/src/Engine.h"

int main()
{
	engine::PrintMessage();
}
```

However, fatal issues can occur if the file location is moved, so we should use absolute paths, especially using the compiler's include paths.

- Absolute Path:
  ![](./storage%20bag/Pasted%20image%2020230714141754.png)

```cpp
#include "Engine.h" // This is sufficient
```

## 2. Linking

Now we need to link.
Click on Engine's build, and you can see the output:

```text
1>Engine.vcxproj -> C:\Dev\YouTube\C++\Game\x64\Debug\Engine.lib
```

This `.lib` file is exactly what we want to link. We can set it as an input in the linker settings, but we don't need to do this manually; Visual Studio can automate this operation because this project is within the actual solution:

Game->Add->Reference, then click OK.
![](./storage%20bag/Pasted%20image%2020230714142402.png)
This will link that `.lib` file to our executable, just as if we had added it to the linker's input.
An advantage is that Engine is now a dependency of Game, meaning Game depends on Engine. If something inside Engine changes, then compiling Game will also compile Engine and Game itself.

Proof: Clean Solution, then build Game, and you can see:

```text
1>------ Build started: Project: Engine, Configuration: Debug x64 ------
1>Engine.cpp
1>Engine.vcxproj -> C:\Dev\YouTube\C++\Game\x64\Debug\Engine.lib
2>------ Build started: Project: Game, Configuration: Debug x64 ------
2>Application.cpp
2>Game.vcxproj -> C:\Dev\YouTube\C++\Game\bin\x64Debug\Game.exe
```

What it actually does is build Engine first and then build Game. Game needs Engine to work because Game references Engine and needs to link it.