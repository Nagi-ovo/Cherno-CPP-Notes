## 1. Optimizing the Use of std::vector in C++

To optimize the use of `std::vector`, we first need to understand how it works and how we can modify it to perform better.

The `std::vector` class essentially works like this:
You create a vector, and then you start `push_back` elements, which means adding elements to the array. If the vector's capacity is not large enough to accommodate the new elements you want to add, the vector needs to allocate new memory, at least enough to hold the new elements and the existing content. It then copies the elements from the old memory location to the new one and deletes the old memory.
So, when we try to `push_back` an element, if the capacity is exhausted, it will resize and reallocate—this is one of the reasons that slows down the code. In fact, we need to keep reallocating, which is a slow operation, especially when we have to copy all the existing elements, which is something we want to avoid.
This is our current strategy for optimizing copying: how to avoid copying objects, especially when dealing with vectors, particularly vectors of objects (we are not storing pointers to vectors, but the vector objects themselves).

Understanding your environment is one of the most important things in the optimization process.
Now we are trying to optimize copying, so we need to know when and why copying occurs.

```cpp
struct Vertex
{
	float x, y, z;

	Vertex(float x, float y, float z)
		: x(x), y(y), z(z)
	{
	}

	Vertex(const Vertex& vertex)
		: x(vertex.x), y(vertex.y), z(vertex.z)
	{
		std::cout << "Copied!" << std::endl;
	}
};

std::ostream& operator<<(std::ostream& stream, const Vertex& vertex)
{
	stream << vertex.x << "," << vertex.y << "," << vertex.z;
	return stream;
}

int main()
{
	std::vector<Vertex> vertices;
	vertices.push_back({1, 2, 3});
	vertices.push_back({4, 5, 6});

	std::cin.get();
}
```

We notice that copying occurs 3 times:
![](./storage%20bag/Pasted%20image%2020230712215507.png)

Let's change to the default constructor approach and add one more element:

```cpp
vertices.push_back(Vertex(1,2,3));
vertices.push_back(Vertex(4,5,6));
vertices.push_back(Vertex(7, 8, 9));
```

![](./storage%20bag/Pasted%20image%2020230712215757.png)

Why did C++ copy my vertex 6 times? Let's debug further.
![](./storage%20bag/Pasted%20image%2020230712215910.png)

We `push_back` a vertex element, and a copy occurs. Why is that?
The reason is that when we create a vertex, we are actually constructing it in the *current stack frame* of the main function, so we are creating it on the stack of `main`. Then we need to move this newly created vertex from the `main` function into the actual vector, into the memory allocated by the vector.

### Optimization 1

What we are doing is **copying** the vertex from the `main` function into the vector class, which is the first thing we can optimize. If we can construct the vertex in the appropriate place, in the memory actually allocated by the vector, that is our first optimization strategy.

### Optimization 2

![](./storage%20bag/Pasted%20image%2020230712220616.png)

We can see that our vector resized twice here. If we understand our "environment," meaning if we know that we plan to put 3 vertex objects into the vector, why not let the vector reserve enough memory for 3 elements from the start, so it doesn't have to resize twice? This is the second optimization strategy.

```cpp
vertices.reserve(3);
```

This is different from resizing (`resize`) or passing 3 in the constructor:
![](./storage%20bag/Pasted%20image%2020230712221136.png)

This won't even compile because it doesn't just allocate enough memory to store 3 vertex objects; it actually constructs 3 vertex objects, whereas we just want enough memory to hold them. This is what `reserve` does—it ensures we have enough memory.
![](./storage%20bag/Pasted%20image%2020230712221403.png)

We've already saved half the copies. Without `reserve`, the number of copies would grow *exponentially*. However, we can do even better: we still have one copy because the vertex is actually constructed in the `main` function and then copied into the actual vector. We want to construct it directly in the vector, and we can use `emplace_back` instead of `push_back`.

```cpp
std::vector<Vertex> vertices;
vertices.reserve(3);
vertices.emplace_back(1, 2, 3);
vertices.emplace_back(4, 5, 6);
vertices.emplace_back(7, 8, 9);
```

In this case, instead of passing an already constructed vertex object, we are just passing the constructor argument list, which tells our vector: in the memory of our vector, construct a vertex object using the following arguments.
![](./storage%20bag/Pasted%20image%2020230712222016.png)

No copies at all.

Let's review how we simply optimized it: just by understanding how it works, realizing that the vertex object was actually copied 6 times. Writing this optimized code isn't difficult, but the modified code will run much faster than the original, and it doesn't even take much time to optimize—just knowing what's actually happening, understanding our environment, and knowing how to use the available tools to optimize it.