This section will delve into a project to discuss how to improve performance through multithreading. (You can review [62 C++ Threads](62%20Threads%20in%20C++.md))

Modern hardware is designed to handle parallel processing. If you examine any hardware you use, whether it's a phone, computer, or similar device, you'll notice they have more than one CPU core. This means you can execute instructions in parallel without waiting for the previous instruction to complete before starting the next one. You can get things done simultaneously. The entire process of program scheduling, multithreading, and parallelization is a vast subject.

Let's see how we can increase the loading speed of a real-world developed game engine by tenfold by fully utilizing our multi-core architecture.

## 1. Multithreading

With the introduction of C++11, we gained many useful tools in the standard library that help us implement multithreading in our programs. In particular, we will discuss and understand something called `std::async` and `futures`, which are interrelated.

The hardest part of running things in parallel is figuring out the dependencies and deciding what to place in different threads. You can't just take a program and say that each part will be called on a different thread, and everything will work fine—that's not how it really works. In your program, there are things that can be placed in a different thread, known as a *worker thread*, which can operate independently. It doesn't matter when it starts or ends, but when it finishes, you can get some feedback or some newly loaded resources.

In the example given below, you don't need to be familiar with game engines, as this applies to any task. However, game engines are a great case study because they handle a lot of data. When dealing with large amounts of data, you need to consider strategies or methods to mitigate the impact on CPU processing time. If you can better control all the data processing, you can use it more intelligently, converting it into thread processing, utilizing your CPU cores, and using your computer as a whole. (If necessary, you can even use your GPU or similar hardware for massive parallel processing.)

The more you do, the faster everything becomes, meaning you can handle more data. A good real-world example is that many games have long loading times because there are many game resources to load. The loading process isn't just about reading files from a disc; it may also involve decompression, sending data to the GPU, or any type of transformation in a specific environment. However, each resource, texture, or model is usually **independent of each other**, making them excellent candidates for multithreading.

Every time we load a model, we don't need to wait for the previous model to finish loading before starting the next one. We can send it to a bunch of worker threads and let it happen *asynchronously*. The beauty here is that you can stream all the data, start rendering your level and world while loading content in the background. Some content might not even be fully loaded yet, but the player can already enter the game world and start moving around.

## 2. How to Split with std::async

Cherno demonstrates this with his own developed Hazel engine. There is a `LoadMeshes` function used to import models. After the `OnAttach` function, responsible for the entire program initialization, is launched, it calls the `LoadMeshes` function. Once this function completes, we can start rendering.

We measure how long it takes from the actual application launch to rendering a frame on the screen. Here, a Timer (see [63 Timing in C++](63%20Timing%20in%20C++.md)) is used to measure the time of the `OnAttach` function:

![](./storage%20bag/Pasted%20image%2020230801214812.png)

After launching, it takes about 6.3 seconds:

![](./storage%20bag/Pasted%20image%2020230801214705.png)

This is quite a long time, and we can do better by using `std::async`.

If we go back to see what needs to be done to implement multithreading, the part of interest should be this for loop:

![](./storage%20bag/Pasted%20image%2020230803215647.png)
> It iterates through each mesh file path, and all it does is load the mesh. It's obviously very independent and doesn't depend on previously loaded meshes or anything like that.

So we can turn it into a parallel for loop:
```cpp
#include <future>

	for(const auto& file : meshFilepaths)
	{
		m_Future.push_back(std::async(std::launch::async, LoadMesh, m_Meshes,file));
	}
// First parameter: What type of job is this? Setting the launch type to async is important.
// Second parameter: Some function that actually runs asynchronously.
```

When you try multithreading, certain resources cannot be accessed simultaneously. You must lock the resource to do what you want, such as modifying it and then unlocking it so another thread can access it. The method is to use a *mutex*, which will be mentioned later.

![](./storage%20bag/Pasted%20image%2020230803221822.png)

After optimization, the launch is ten times faster.

You can see that this kind of multithreading is very beneficial for your program, allowing you to fully utilize your hardware to improve speed. A lot of performance optimization is about making the most of the hardware you're using, understanding the platform you're releasing your code on, understanding the hardware your program will run on, and then leveraging those advantages. We are dealing with multi-core machines, and using these threads allows your program to not just execute instructions sequentially but to defer or dispatch some tasks to different threads, enabling the computer to process things faster.