## 1. Destructor

A *Destructor* runs when you destroy an object, while a *Constructor* [Constructor](25%20Constructors%20in%20C++.md#^0156ab) runs when you create an instance of an object.

The destructor applies to both stack and heap-allocated memory. Therefore, if you create an object using the *new* keyword (which exists on the heap) and then call *delete*, the destructor will be invoked.

If you only have stack-based objects, the object will be deleted when it goes out of scope, so the destructor will also be called at that time.

Destructor: `~ClassName`

![](./storage%20bag/Pasted%20image%2020230703151448.png)

Stack invocation (destroyed after leaving scope):
![](./storage%20bag/Pasted%20image%2020230703151702.png)

![](./storage%20bag/Pasted%20image%2020230703151733.png)

## 2. Practical Usage

Why use a *destructor*? If you perform some initialization work in the constructor, you might want to release or destroy resources in the destructor. If you don't do this, it could lead to memory leaks.

A good example is *heap*-allocated objects. If you manually allocate any type of memory on the heap, you should also manually clean it up. If you use an Entity or perform allocation within the Entity's constructor, you should clean them up in the destructor. Because after the destructor is called, that Entity object no longer exists.

Generally, you don't manually call the *destructor*.

```cpp
Entity e;
e.~Entity();  // Destroyed Entity
```