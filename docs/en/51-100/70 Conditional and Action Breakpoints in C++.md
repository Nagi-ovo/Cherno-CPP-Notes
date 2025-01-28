This lecture covers some simple Visual Studio development and debugging techniques, focusing not just on breakpoints, but also on the application of conditions and actions to breakpoints.

## 1. Conditional Breakpoints

With conditional breakpoints, we can instruct the debugger to place a breakpoint at a specific location, but only trigger it when certain conditions are met, such as when something in memory satisfies a particular condition.

## 2. Action Breakpoints

Action breakpoints allow us to perform certain actions, typically printing something to the console when the breakpoint is hit.

There are two types of action breakpoints:

- The first type allows you to continue execution after printing what you want. For example, if you want to log the mouse position, each time the mouse moves, the move event (which prints the mouse position) occurs. You can have the breakpoint print something to the console while keeping the program running.
- The second type prints something but still interrupts the program, pausing its execution so that we can inspect other things in memory.

## 3. Practical Usage

Right-click on the set breakpoint and select Conditions or Actions (they can be used together; opening either allows you to set the other). Here, we first test the *Action breakpoint*:

![](./storage%20bag/Pasted%20image%2020230728222350.png)

Write the variable name inside `{}`, and you can also perform type casting or add some text (as shown in the example).

![](./storage%20bag/Pasted%20image%2020230728222958.png)

Of course, you could also print these contents by adding code to the source code, but the coolest thing here is that you **do not need to terminate your application or recompile the code**. You simply print additional data to the console (Output Window) while the initial application is running, which enhances efficiency.
Another method is to set a regular breakpoint and then find the variable after the program is interrupted, but this is time-consuming.

Next, test the *Conditional breakpoint*:

![](./storage%20bag/Pasted%20image%2020230728223139.png)

The condition here can be any Boolean statement.

Conditional breakpoints are also very useful. For example, if you want to find a specific condition in a loop, it's nearly impossible with regular breakpoints. For instance, you might want to interrupt the program only at a specific enemy node (the problematic entity). If done manually, you would have to press F5 multiple times. Although it may reduce performance, this is just a debugging tool after all.