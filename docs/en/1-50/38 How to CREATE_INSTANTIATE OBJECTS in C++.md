How do we instantiate our class? Generally, we have two choices, and the difference between them lies in where the memory comes from and where our object is actually created.

When we create an object in C++, it requires some memory. Even if we write a completely empty class: no class members, nothing, it must still occupy at least one byte of memory, but this is not common because our class has many members that need to be stored somewhere. The application divides memory into two main parts: _heap and stack_ **heap** and **stack**.

In C++, we can choose where to create the object, on the heap or on the stack, and they have different functional differences.

For example, *stack* objects have an automatic **lifetime**, their lifetime is determined by the *scope* where they are declared. Once out of this scope, their memory will be quickly released. Because when this scope ends, the stack pops, and everything placed on this stack, in this scope, will be released.

But the *heap* is different, the heap is a big and mysterious place. Once you allocate an object on the heap, you have actually created an object that will always exist there. Until you decide: I don't need it anymore, I want to release this object, you can do anything with that memory.

## 1. Creating on the Stack

```cpp
#include <iostream>
#include <string>
#define LOG(x) std::cout << x << std::endl;

using String = std::string;

class Entity
{
private:
	String m_Name;
public:
	Entity() : m_Name("Unknown"){}
	Entity(const String& name) : m_Name(name) {}

	const String& GetName() const { return m_Name; }
};


int main()
{
	Entity entity("Cherno");           // Cherno
	Entity entity1 = Entity("Cherno"); // Cherno
	LOG(entity.GetName());
	LOG(entity1.GetName());
	std::cin.get();
}
```

#### When to create objects on the stack like this?

Almost always. If you can create objects this way, then do so, this is the basic rule.
Because in C++ this is the fastest and most controlled way to initialize objects.

Now let's discuss:

#### Why in some cases you can't do this:

If you want it to survive beyond the function's lifetime.

- Function

```cpp
void Function()
{
	Entity entity = Entity("Cherno");
}                      // Once this curly brace is reached, this entity will be destroyed from memory
```

- Instantiation

![](./storage%20bag/Pasted%20image%2020230708151150.png)

> When debugging to the point of leaving the scope of the curly braces, e still points to the same address, but m_Name is no longer there.

![](./storage%20bag/Pasted%20image%2020230708151324.png)

> Because that object has been released or destroyed, the entity object named Cherno no longer exists, it is no longer in the stack structure.

Another reason we might not want to allocate on the stack is: if this entity is too large, and we might have many entities, we might not have enough space to allocate, because the stack is usually very small, generally one or two megabytes, depending on your platform and compiler.
Therefore, you may have to allocate on the *heap*.

## 2. Allocating on the Heap

```cpp
Entity* entity = new Entity("Cherno");
```

The biggest difference here is not the pointer, but the *new* keyword.
When we call `new Entity`, what actually happens is that we allocate memory on the heap, we call the constructor, and then this `new Entity` actually returns an `Entity*` (pointer). It returns the memory address of the entity allocated on the heap, which is why we declare it as type `Entity*`.

However, *new* should not be used everywhere, simply because of performance reasons, allocating on the heap takes longer than on the stack, and if you allocate on the heap, then you **must manually release the allocated memory**

```cpp
delete entity;
```

Use *new* and then *delete*, this is how C++ works.

```cpp
int main()
{
	Entity* e;
	{
		Entity* entity = new Entity("Cherno");
		e = entity;                             // entity is already a pointer, remove &
		LOG((*entity).GetName());               // Dereference
		/* Or */
		LOG(entity->GetName());                 // -> arrow operator

	}

	std::cin.get();
	delete e;
}
```

Here, it is important to note that `entity` is a local variable created in the inner scope, and its lifetime is limited to that scope. When the program execution leaves that scope, the `entity` pointer will go out of scope and can no longer be accessed. If you try to use `delete entity` after leaving the scope, it will lead to undefined behavior because the `entity` pointer is already invalid.

On the contrary, `e` is a pointer defined in the outer scope, and the value of `entity` is assigned to `e`. Therefore, after leaving the inner scope, `e` still retains the pointer to the dynamically allocated `Entity` object. Therefore, using `delete e` can correctly release the memory of that object.

So if the object is very large, or you want to explicitly control the lifetime of the object, then create it on the heap.
If it's not these two cases, then allocate on the stack, it's simpler, and it's automatically recycled and faster.
Allocating on the heap requires manual *delete*, and forgetting to call it can lead to memory leaks.

Later, we will use *smart pointers*, which allow us to still allocate on the heap and still get that size advantage, and when the pointer goes out of scope, the object will be automatically deleted.