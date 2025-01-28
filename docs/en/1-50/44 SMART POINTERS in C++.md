Previously, we learned that `new` allocates memory on the heap and requires `delete` to free that memory because it doesn't automatically release it. *Smart pointers* are a way to automate this process.

When you call `new`, you no longer need to call `delete`. In many cases where smart pointers are used, you don't even need to call `new`.

A smart pointer is essentially a wrapper around a raw pointer:
When you create a smart pointer, it calls `new` and allocates memory for you, and then, depending on the type of smart pointer you use, this memory will be automatically freed at a certain point.

## 1. unique_ptr

*unique_ptr* is a *scoped pointer*, meaning that when this pointer goes out of scope, it will be destroyed, and `delete` will be called. See [previous lesson](<43%20Object%20Lifetime%20in%20C++%20(Stack_Scope%20Lifetimes).md#^58d90d>)

Why is it called a *unique* pointer?
Because it must be ==_unique_==. You cannot copy a `unique_ptr` because if you copy it, you would have two `unique_ptr`s pointing to the same memory. If one of them dies, it will free that memory, meaning the other `unique_ptr` pointing to the same memory would point to already freed memory. So you cannot copy it.

You cannot call `unique_ptr` like this:

```cpp
std::unique_ptr<Entity> entity = new Entity();
```

Because its constructor is *explicit*, meaning you need to ==_explicitly_== call the constructor.

Correct way:

```cpp
std::unique_ptr<Entity> entity(new Entity()); // <template parameter>
entity->Print();
```

You can call its functions using the arrow operator just like a raw pointer.

A **better** way is:

```cpp
std::unique_ptr<Entity> entity = std::make_unique<Entity>();
```

This is important for `unique_ptr`, mainly for *exception safety*. If the constructor happens to throw an exception, it will be slightly safer. You won't end up with a *dangling pointer* (a pointer that doesn't reference anything) causing memory leaks.

![](./storage%20bag/Pasted%20image%2020230710164219.png)

As shown in the image, when going out of scope, our entity will be automatically destroyed.

This is the simplest smart pointer, very useful and with low overhead (or even no overhead). It's just a ==_stack-allocated object_==, and when the stack-allocated object dies (is destroyed), it will call `delete` on your pointer and free the memory.

As mentioned earlier, `unique_ptr` cannot be copied. If you look at its definition, you'll find that its copy constructor and copy assignment operator are actually deleted, which is why you'll get a compilation error when running the following code.
![](./storage%20bag/Pasted%20image%2020230710164823.png)

This is specifically designed to prevent you from shooting yourself in the foot because you cannot copy this: once one of the pointers dies (becomes invalid), they both "die" (become invalid) because the underlying memory of the heap-allocated object will be freed. (Meaning it's not actually a pointer but an object)

So if you want to "share" this pointer, that's where the *shared pointer* comes in.

## 2. shared_ptr

Shared pointers are a bit different; they are a bit hardcore because they do a lot of other things under the hood.
The way `shared_ptr` is implemented actually depends on the compiler and the standard library you're using in your compiler. However, in all the systems the author has seen, it uses *reference counting*.

Reference counting is essentially a method to track how many references your pointer has. Once the reference count reaches 0, it is deleted.

For example, I just created a shared pointer, and then I created another shared pointer to copy it. At this point, my reference count is 2. When the first pointer becomes invalid, my reference counter decreases by 1, and then when the last one becomes invalid, my reference count goes back to 0, and it is truly "dead," so the memory is freed.

This will compile (but don't use it this way!):

```cpp
std::shared_ptr<Entity> sharedEntity(new Entity());  // Don't use it this way!
```

However, you definitely don't want to use `shared_ptr` this way. In `unique_ptr`, the reason for not directly calling `new` is due to exception safety, but in `shared_ptr`, it's different.

Because `shared_ptr` needs to allocate another block of memory, called the control block, to store the reference count. If you first create a new Entity and then pass it to the `shared_ptr` constructor, it has to do two memory allocations: first, the allocation for new Entity, and then the allocation for the control block of the shared_ptr.

However, if you use `make_shared`, you can combine them:

```cpp
std::shared_ptr<Entity> sharedEntity = std::make_shared<Entity>();
```

This is more efficient and obviously helpful for those who don't like using new and delete.

### Copying Shared Pointers

With shared pointers, you can of course copy them.
In the following code, there are two scopes. You can see that when the inner scope dies, the sharedEntity becomes invalid, but the Entity is not destructed and deleted because e0 is still valid and holds a reference to the Entity. Press F10 again, and when all references are gone, when all stack-allocated objects tracking `shared_ptr` die, the underlying Entity will be freed from memory and deleted.
![](./storage%20bag/Pasted%20image%2020230711154437.png)

## 3. weak_ptr

There's one more thing you can use with `shared_ptr`

```cpp
std::shared_ptr<Entity> sharedEntity = std::make_shared<Entity>();
std::weak_ptr<Entity> weakEntity = sharedEntity;
```

What's done here is the same as what was done earlier when copying sharedEntity, but earlier it would increase the reference count, whereas here it does not:
When you assign a `shared_ptr` to another `shared_ptr`, the reference count increases. But when you assign a `shared_ptr` to a `weak_ptr`, it does not increase the reference count.

So what's the benefit of this?
If you don't want ownership of the Entity, like you might be sorting a list of Entities, you don't care if they are valid, you just need to store a reference to them.
You can know if the underlying object it references is still alive? If so, you can perform other operations. But it won't keep the underlying object alive because it doesn't increase the reference count.
![](./storage%20bag/Pasted%20image%2020230711160448.png)

As shown in the image, after changing to `weak_ptr`, it is destroyed when exiting the first scope. At this point, the `weak_ptr` e0 is pointing to an invalid Entity. However, you can ask this weak pointer: are you still valid?

These are very useful smart pointers, but they certainly do not completely replace the `new` and `delete` keywords. Only when you want to declare a heap-allocated object and don't want to clean it up yourself should you use smart pointers, preferably `unique_ptr` because it has lower overhead. But if you need to share between objects and can't use `unique_ptr`, then use `shared_ptr`.