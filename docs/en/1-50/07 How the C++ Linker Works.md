## 1. Linking

Once the files are compiled, we need a process called *Linking*, whose main task is to locate each symbol and function and link them together. Since each .cpp file is transformed into a .obj file during compilation, if we want to create a project with many .cpp files, each file cannot communicate with the others. Therefore, we need a [Linker](05%20How%20C++%20Works.md#^620dbb) to link them.

Even if you write everything in a single file, finding the [entry part](05%20How%20C++%20Works.md#^2224fe) of the program, i.e., where the main function is located, also requires the linker to link the main function with other components.

## 2. Error Handling

### 2.1

Syntax errors, function not found: Error examples such as C+XXXX indicate issues during [Compiling](./storage%20bag/06%20How%20the%20C++%20Compiler%20Works.md).

### 2.2

Missing main function entry point: Error examples such as LNK+XXXX represent problems occurring during the linking phase.

### 2.3

Unresolved external symbol: There is a difference between function definition and function declaration. If a function is not called, it won't trigger an error. Alternatively, this can be resolved using `static`, which ensures that linking only occurs within the file.

### 2.4

Duplicate symbol: This occurs when there are functions or variables with the same name and signature, i.e., two functions with the same name, return type, and parameters. The linker doesn't know which one to link. This is likely to happen if a function is called in a .h file and also [#include](06%20How%20the%20C++%20Compiler%20Works.md#^f8f616) in another file, causing this issue. This can be resolved using `static`, ensuring that linking only occurs within the file, or by using `inline`.
The recommended approach is to place all function declarations in the .h header file and the definitions in the .cpp file.