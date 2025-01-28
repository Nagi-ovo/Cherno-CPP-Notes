This lesson is about *threads*, which is to say, how we can achieve *parallelization*. Most computers or processors nowadays have more than one logical processing thread, and as we delve into more complex projects, moving certain tasks to two different execution threads can be highly beneficial. Not only for performance enhancement but also for what else we can accomplish with them.

For example, we use `std::cin.get()` to request user input, but while waiting for input, we can't do anything else until the user presses Enter. Our thread is essentially blocked. But what if we could do something else in the meantime? Like printing something to the console, and so on.

## 1. Implementing with Threads

```cpp
#include <iostream>
#include <thread>

static bool s_Finish = false;

void DoWork()
{
	using namespace std::literals::chrono_literals; // Introducing chrono literals for easier time unit representation.
	std::cout << "Started thread id:" << std::this_thread::get_id() << std::endl;
	while (!s_Finish)
	{
		std::cout << "Working...\n" << std::endl;
		std::this_thread::sleep_for(1s); // Using 1s directly to represent one second
	}
}

int main()
{
	std::thread worker(DoWork);

	std::cin.get();
	s_Finish = true;
//	worker.join(); //
	std::cout << "Finished" << std::endl;
	std::cout << "Started thread id:" << std::this_thread::get_id() << std::endl;
	std::cin.get();
}
```

![](./storage%20bag/Pasted%20image%2020230723183331.png)

This is a simple example of multithreading in C++. The main workflow of the code is as follows:

1. The global `s_Finish` flag is declared as `static` to limit its scope to the current source file.

2. The `DoWork` function is a thread routine. It enters an infinite loop, printing "Working..." every second until the `s_Finish` flag is set to `true`.

3. In the `main` function, a new thread named `worker` is created. The `DoWork` function is passed as an argument to the thread's constructor, indicating that this function should run in the newly created thread.

4. The `std::cin.get();` statement is a blocking call that waits for the user to press the Enter key.

5. Once Enter is pressed, the `s_Finish` flag is set to `true`, causing the `DoWork` function to break out of its loop and return.

6. The `worker.join();` statement is used to wait for the thread to complete its execution before the program can continue. It is crucial to ensure that threads complete execution before the main thread (in this case, the program) ends. If the program ends while the `worker` thread is still running, it will be abruptly terminated, which could lead to various issues, such as resources not being properly released.

Threads are important; they are very useful for speeding up programs, primarily aimed at optimization, and can also be used to perform tasks like those in the example above.