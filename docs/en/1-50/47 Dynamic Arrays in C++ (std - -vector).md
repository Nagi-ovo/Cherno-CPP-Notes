Now we are finally starting to write some C++ Standard Library stuff. The *Standard Template Library* (STL) is essentially a library filled with *containers*, which are container types. These containers hold specific data, and it's called the Standard Template Library because it can template anything.

You just need to know that *templates* can handle the underlying data types you provide, which means you don't need to write your own data structures or anything like that.

## 1. C++ Dynamic Array (std::vector)

So C++ provides us with a class called `Vector`, which is in the *std namespace*.

Why is it called Vector? You can learn the story behind it in this [link](https://stackoverflow.com/questions/581426/why-is-a-c-vector-called-a-vector):
	It is called a vector because the designer of the Standard Template Library, Alex Stepanov, chose this name to distinguish it from built-in arrays. He now admits that this was a mistake because mathematics already uses the term "vector" to refer to a fixed-length sequence of numbers. C++11 further compounded this mistake by introducing a class named 'array', which behaves like a mathematical vector.
	The lesson from Alex is: Be very careful when naming things.

So it really shouldn't be called *Vector*, but rather something like *ArrayList*, which would make more sense because it is essentially a dynamic array. It's somewhat like a collection, a collection that does not enforce the uniqueness of its elements.
In other words, it's basically an *array*, but unlike C++'s ordinary array types (raw arrays or the standard array class [31 Arrays in C++](31%20Arrays%20in%20C++.md)), it can resize itself, which means when you create this vector, this dynamic array, it doesn't have a fixed size. You can give it a fixed size if you want to initialize it with a specific size. But generally, we don't set a size for it.
You just need to create this Vector and put elements into it. Every time you add an element, the array size grows.
Principle: When you exceed the allocated memory size, it creates a new array in memory that is larger than the first one, copies everything into it, and then deletes the old one, so you have a new array with more storage space. (So you can guess that Alex thought at the time that a dynamic array could extend infinitely like a vector...)

```cpp
struct Vertex
{
	float x, y, z;
};

std::ostream& operator<<(std::ostream& stream, const Vertex& vertex)
{
	stream << vertex.x << "," << vertex.y << "," << vertex.z;
	return  stream;
}


int main()
{
	Vertex* vertices = new Vertex[5];

	std::cin.get();
}
```
We might have a program that allows users to input data, and we certainly don't want to tell users that they can't input more once they exceed the allocated memory. We need a way to resize the capacity when you reach their maximum capacity to store more data. Another solution is to allocate an excessively large array, which is also not ideal because you would waste a lot of memory.

This is where the Vector class comes in:
```cpp
#include <vector>

std::vector<Vertex> vertices; // Unlike Java, you can specify primitive types like int, float, etc.
```
Here, objects are stored instead of pointers, mainly because storing Vertex objects is technically better than storing pointers. If you allocate objects, your memory allocation will be in a straight line, and a dynamic array is a contiguous array in memory, meaning it's not *fragmented*. You get one vertex followed by another (x, y, z). This is optimal because if you want to traverse them, set them, change them, or read them, no matter what you want to do with them, they are all on the same cache line in a sense.

```cpp
#include <iostream>
#include <string>
#include <vector>

struct Vertex
{
	float x, y, z;
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

	// Two methods
	for (int i = 0; i < vertices.size(); i++)
	{
		std::cout << vertices[i] << std::endl;
	}

	for (Vertex& v : vertices)
	//for (Vertex v : vertices)
	// Here, each vertex is actually copied into this for-range loop, and we want to avoid copying by adding &
	{
		std::cout << v << std::endl;
	}
	/*for (Vertex v : vertices) is the range-based for loop syntax introduced in C++11, also known as the range loop or foreach loop.

In this loop, each iteration assigns an element from the container vertices to the loop variable v. The loop traverses the entire container, processing each element one by one.

vertices is a std::vector container that stores Vertex struct objects. By using the range-based for loop, you can access each element in the container one by one and assign it to the variable v.

Inside the loop body, you can use the variable v as you would with a normal Vertex object. Here, the overloaded operator<< function is used to output each Vertex object to the std::cout stream.

In summary, the range-based for loop syntax for (Vertex v : vertices) makes traversing container elements more concise and intuitive, reducing the hassle of manual index iteration. It is one of the commonly used loop forms in C++.*/
	std::cin.get();
}

//Output:
//1,2,3
//4,5,6

//1,2,3
//4,5,6
```

If we want to clear the vertices list:
```cpp
vertices.clear();  // Resets the array size to 0
```
We can also remove a specific element:
```cpp
vertices.erase() // The parameter should be an iterator

// If we want to remove the second element, i.e., index 1
vertices.erase(vertices.begin() + 1);  // 1,2,3
```

## 2. Notes
Another thing to mention is that when you pass these vectors to functions or classes or other things, you need to make sure you are passing them by reference:
```cpp
void Function(const std::vector<Vertex>& vertices){}
```
This ensures that you are not copying the entire array into this function, which is very important.