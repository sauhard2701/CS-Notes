# Java Virtual Machine
<!-- GFM-TOC -->
* [Java Virtual Machine](#java-virtual-machine)
    * [1. Runtime Data Areas](#_1-runtime-data-areas)
        * [Program Counter](#program-counter)
        * [Java Virtual Machine Stack](#java-virtual-machine-stack)
        * [Native Method Stack](#native-method-stack)
        * [Heap](#heap)
        * [Method Area](#method-area)
        * [Runtime Constant Pool](#runtime-constant-pool)
        * [Direct Memory](#direct-memory)
    * [2. Garbage Collection](#_2-garbage-collection)
        * [Determine Whether an Object Is Collectible](#determine-whether-an-object-is-collectible)
        * [Reference Types](#reference-types)
        * [Garbage Collection Algorithms](#garbage-collection-algorithms)
        * [Garbage Collectors](#garbage-collectors)
    * [3. Memory Allocation and Collection Strategies](#_3-memory-allocation-and-collection-strategies)
        * [Minor GC and Full GC](#minor-gc-and-full-gc)
        * [Memory Allocation Strategy](#memory-allocation-strategy)
        * [Full GC Trigger Conditions](#full-gc-trigger-conditions)
    * [4. Class Loading Mechanism](#_4-class-loading-mechanism)
        * [Class Lifecycle](#class-lifecycle)
        * [Class Loading Process](#class-loading-process)
        * [Class Initialization Timing](#class-initialization-timing)
        * [Classes and Class Loaders](#classes-and-class-loaders)
        * [Class Loader Classification](#class-loader-classification)
        * [Parent Delegation Model](#parent-delegation-model)
        * [Custom Class Loader Implementation](#custom-class-loader-implementation)
    * [References](#references)
<!-- GFM-TOC -->


Most of this article references **Zhou Zhiming's Understanding the Java Virtual Machine**. For deeper study, read the original book.

## 1. Runtime Data Areas

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/5778d113-8e13-4c53-b5bf-801e58080b97.png" width="400px"> </div><br>

### Program Counter

Records the address of the virtual-machine bytecode instruction currently being executed. If a native method is being executed, the value is empty.

### Java Virtual Machine Stack

Each Java method creates a stack frame when it executes. The stack frame stores the local variable table, operand stack, constant-pool references, and related information. The process from method invocation to completion corresponds to a stack frame being pushed onto and popped from the Java Virtual Machine stack.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/8442519f-0b4d-48f4-8229-56f984363c69.png" width="400px"> </div><br>

Use the -Xss virtual-machine parameter to specify the Java Virtual Machine stack size for each thread. The default is 256K in JDK 1.4 and 1M in JDK 1.5+:

```java
java -Xss2M HackTheJava
```

This area may throw the following exceptions:

- StackOverflowError is thrown when the stack depth requested by a thread exceeds the maximum value.
- OutOfMemoryError is thrown when the stack dynamically expands but cannot request enough memory.

### Native Method Stack

The native method stack is similar to the Java Virtual Machine stack. The difference is that the native method stack serves native methods.

Native methods are usually written in other languages, such as C, C++, or assembly, and compiled into programs based on the local hardware and operating system. These methods require special handling.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/66a6899d-c6b0-4a47-8569-9d08f0baf86c.png" width="300px"> </div><br>

### Heap

All objects allocate memory here, making it the main area for garbage collection (the "GC heap").

Modern garbage collectors generally use generational collection algorithms. The main idea is to apply different garbage-collection algorithms to different types of objects. The heap can be divided into two parts:

- Young Generation
- Old Generation

The heap does not require contiguous memory and can grow dynamically. If growth fails, an OutOfMemoryError is thrown.

Use the -Xms and -Xmx virtual-machine parameters to specify the heap size of a program. The first parameter sets the initial value, and the second sets the maximum value.

```java
java -Xms1M -Xmx2M HackTheJava
```

### Method Area

Stores loaded class information, constants, static variables, code compiled by the just-in-time compiler, and related data.

Like the heap, it does not require contiguous memory and can expand dynamically. If expansion fails, it also throws an OutOfMemoryError.

The main goals of garbage collection in this area are reclaiming the constant pool and unloading classes, but this is generally difficult to implement.

The HotSpot virtual machine treated it as the permanent generation for garbage collection. However, the size of the permanent generation is difficult to determine because it is affected by many factors and changes after each Full GC, so OutOfMemoryError exceptions often occur. To make the method area easier to manage, JDK 1.8 removed the permanent generation and moved the method area to metaspace, which is located in native memory rather than virtual-machine memory.

The method area is part of the JVM specification. Both the permanent generation and metaspace are implementation approaches. After JDK 1.8, data originally stored in the permanent generation was split between the heap and metaspace. Metaspace stores class metadata, while static variables and the constant pool are placed in the heap.

### Runtime Constant Pool

The runtime constant pool is part of the method area.

The constant pool in a Class file, which contains literals and symbolic references generated by the compiler, is placed in this area after the class is loaded.

In addition to constants generated at compile time, dynamically generated constants are also allowed, such as those from String's intern().

### Direct Memory

NIO was introduced in JDK 1.4. It can use native libraries to allocate off-heap memory directly, then operate on that memory through a DirectByteBuffer object in the Java heap. This can significantly improve performance in some scenarios because it avoids copying data back and forth between heap memory and off-heap memory.

## 2. Garbage Collection

Garbage collection mainly targets the heap and method area. The program counter, virtual-machine stack, and native method stack are private to each thread. They exist only during the thread's lifetime and disappear when the thread ends, so these three areas do not need garbage collection.

### Determine Whether an Object Is Collectible

#### 1. Reference Counting

Add a reference counter to each object. When a reference to the object is added, the counter increases by 1; when a reference becomes invalid, the counter decreases by 1. Objects with a reference count of 0 can be collected.

When two objects reference each other cyclically, their reference counters never become 0, so they cannot be collected. Because cyclic references exist, the Java Virtual Machine does not use reference counting.

```java
public class Test {

    public Object instance = null;

    public static void main(String[] args) {
        Test a = new Test();
        Test b = new Test();
        a.instance = b;
        b.instance = a;
        a = null;
        b = null;
        doSomething();
    }
}
```

In the code above, the object instances referenced by a and b hold references to each other. Therefore, after the references to objects a and b are removed, the two objects still reference each other, causing the two Test objects to be impossible to collect.

#### 2. Reachability Analysis

Search starts from GC Roots. Reachable objects are live, and unreachable objects can be collected.

The Java Virtual Machine uses this algorithm to determine whether objects can be collected. GC Roots generally include:

- objects referenced by local variable tables in the virtual-machine stack
- objects referenced by JNI in the native method stack
- objects referenced by class static properties in the method area
- objects referenced by constants in the method area

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/83d909d2-3858-4fe1-8ff4-16471db0b180.png" width="350px"> </div><br>


#### 3. Method Area Collection

Because the method area mainly stores permanent-generation objects, and permanent-generation objects have a much lower collection rate than young-generation objects, collecting the method area is not cost-effective.

The main tasks are reclaiming the constant pool and unloading classes.

To avoid memory overflow, scenarios that heavily use reflection and dynamic proxies require the virtual machine to support class unloading.

There are many conditions for unloading a class. The following three conditions must be met, and even then the class is not necessarily unloaded:

- All instances of the class have been collected, so no instances of the class exist in the heap.
- The ClassLoader that loaded the class has been collected.
- The Class object corresponding to the class is not referenced anywhere, so the class methods cannot be accessed through reflection anywhere.

#### 4. finalize()

Similar to a C++ destructor, it is used to close external resources. However, approaches such as try-finally can do this better. finalize() is expensive to run, highly uncertain, and cannot guarantee the call order among objects, so it is best avoided.

When an object is collectible, if its finalize() method needs to run, the object may make itself referenced again inside that method and rescue itself. This rescue can happen only once. If a collectible object previously rescued itself through finalize(), that method will not be called again during later collection.

### Reference Types

Whether reference counting is used to determine the number of references to an object, or reachability analysis is used to determine whether an object is reachable, deciding whether an object can be collected is related to references.

Java provides four reference types with different strengths.

#### 1. Strong Reference

Objects associated with strong references will not be collected.

Create a strong reference by creating a new object with new.

```java
Object obj = new Object();
```

#### 2. Soft Reference

Objects associated with soft references are collected only when memory is insufficient.

Use the SoftReference class to create a soft reference.

```java
Object obj = new Object();
SoftReference<Object> sf = new SoftReference<Object>(obj);
obj = null;  // make the object associated only with the soft reference
```

#### 3. Weak Reference

Objects associated with weak references will definitely be collected, meaning they can survive only until the next garbage collection.

Use the WeakReference class to create a weak reference.

```java
Object obj = new Object();
WeakReference<Object> wf = new WeakReference<Object>(obj);
obj = null;
```

#### 4. Phantom Reference

Also called a phantom reference, it does not affect an object's lifetime, and the object cannot be obtained through a phantom reference.

The only purpose of setting a phantom reference for an object is to receive a system notification when the object is collected.

Use PhantomReference to create a phantom reference.

```java
Object obj = new Object();
PhantomReference<Object> pf = new PhantomReference<Object>(obj, null);
obj = null;
```

### Garbage Collection Algorithms

#### 1. Mark-Sweep

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/005b481b-502b-4e3f-985d-d043c2b330aa.png" width="400px"> </div><br>

During the marking phase, the program checks whether each object is live. If it is live, the program marks the object header.

During the sweep phase, objects are reclaimed and mark bits are cleared. It also checks whether a reclaimed block is contiguous with the previous free block; if so, the two blocks are merged. Reclaiming an object means treating the object as a block and linking it into a singly linked list called the free list. Later allocation only needs to traverse this free list to find a block.

During allocation, the program searches the free list for a block whose size is greater than or equal to the new object's size. If the found block equals size, the block is returned directly. If the found block is larger than size, it is split into two parts of size and (block - size); the block of size is returned, and the block of (block - size) is returned to the free list.

Drawbacks:

- both the marking and sweeping processes are inefficient;
- it creates many non-contiguous memory fragments, which can prevent memory allocation for large objects.

#### 2. Mark-Compact

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ccd773a5-ad38-4022-895c-7ac318f31437.png" width="400px"> </div><br>

Move all surviving objects toward one end, then directly clear the memory outside the boundary.

Advantage:

- does not create memory fragmentation

Drawback:

- requires moving many objects, so processing efficiency is relatively low.

#### 3. Copying

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/b2b77b9e-958c-4016-8ae5-9c6edd83871e.png" width="400px"> </div><br>

Divide memory into two equal-sized blocks and use only one at a time. When that block is used up, copy the surviving objects to the other block, then clear the used memory space.

The main drawback is that only half of the memory is used.

Modern commercial virtual machines use this collection algorithm to collect the young generation, but they do not divide memory into two equal-sized blocks. Instead, they use one larger Eden space and two smaller Survivor spaces, using Eden and one Survivor at a time. During collection, all surviving objects in Eden and the used Survivor are copied to the other Survivor, then Eden and the used Survivor are cleared.

In the HotSpot virtual machine, the default Eden-to-Survivor size ratio is 8:1, ensuring 90% memory utilization. If more than 10% of objects survive each collection, one Survivor is not enough. At this point, allocation guarantee from the old generation is needed, meaning old-generation space is borrowed to store objects that do not fit.

#### 4. Generational Collection

Modern commercial virtual machines use generational collection algorithms, dividing memory into several areas according to object lifetime and applying appropriate collection algorithms to each area.

The heap is generally divided into the young generation and old generation.

- Young generation: copying algorithm
- Old generation: mark-sweep or mark-compact algorithm

### Garbage Collectors

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/c625baa0-dde6-449e-93df-c3a67f2f430f.jpg" width=""/> </div><br>

The figure above shows the seven garbage collectors in the HotSpot virtual machine. Lines indicate collectors that can be used together.

- Single-threaded vs. multithreaded: single-threaded means the garbage collector uses only one thread, while multithreaded means it uses multiple threads.
- Serial vs. concurrent: serial means the garbage collector and user program execute alternately, so the user program must pause during garbage collection; concurrent means the garbage collector and user program execute at the same time. Except for CMS and G1, the other garbage collectors execute serially.

#### 1. Serial Collector

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/22fda4ae-4dd5-489d-ab10-9ebfdad22ae0.jpg" width=""/> </div><br>

Serial means it executes in a serial manner.

It is a single-threaded collector and uses only one thread for garbage collection.

Its advantage is simplicity and efficiency. In a single-CPU environment, it has the highest single-threaded collection efficiency because there is no thread-interaction overhead.

It is the default young-generation collector in Client scenarios because memory is generally not very large there. Its pause time for collecting one or two hundred megabytes of garbage can be kept within just over one hundred milliseconds. As long as this is not too frequent, the pause time is acceptable.

#### 2. ParNew Collector

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/81538cd5-1bcf-4e31-86e5-e198df1e013b.jpg" width=""/> </div><br>

It is the multithreaded version of the Serial collector.

It is the default young-generation collector in Server scenarios. Besides performance reasons, the main reason is that, apart from the Serial collector, it is the only collector that can work with the CMS collector.

#### 3. Parallel Scavenge Collector

Like ParNew, it is a multithreaded collector.

Other collectors aim to minimize user-thread pause time during garbage collection, while this collector aims to achieve controllable throughput. Therefore, it is called a throughput-first collector. Here, throughput is the ratio of CPU time spent running user programs to total CPU time.

Shorter pause times are better for programs that interact with users because good response speed improves user experience. High throughput uses CPU time efficiently and completes computation tasks as quickly as possible, making it suitable for background tasks that require little interaction.

Reducing pause time trades off throughput and young-generation space: the young generation becomes smaller, garbage collection becomes more frequent, and throughput decreases.

GC adaptive tuning (GC Ergonomics) can be enabled with a switch parameter, so details such as young-generation size (-Xmn), the Eden-to-Survivor ratio, and the age at which objects are promoted to the old generation do not need to be manually specified. The virtual machine collects performance monitoring information based on current system operation and dynamically adjusts these parameters to provide the most suitable pause time or maximum throughput.

#### 4. Serial Old Collector

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/08f32fd3-f736-4a67-81ca-295b2a7972f2.jpg" width=""/> </div><br>

It is the old-generation version of the Serial collector and is also used by virtual machines in Client scenarios. If used in Server scenarios, it has two main purposes:

- In JDK 1.5 and earlier, before Parallel Old appeared, it was used together with the Parallel Scavenge collector.
- It serves as a fallback for the CMS collector when Concurrent Mode Failure occurs during concurrent collection.

#### 5. Parallel Old Collector

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/278fe431-af88-4a95-a895-9c3b80117de3.jpg" width=""/> </div><br>

It is the old-generation version of the Parallel Scavenge collector.

In scenarios that emphasize throughput and are sensitive to CPU resources, consider Parallel Scavenge plus Parallel Old first.

#### 6. CMS Collector

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/62e77997-6957-4b68-8d12-bfd609bb2c68.jpg" width=""/> </div><br>

CMS stands for Concurrent Mark Sweep, where Mark Sweep refers to the mark-sweep algorithm.

It is divided into the following four steps:

- Initial mark: only marks objects directly associated with GC Roots. It is very fast and requires a pause.
- Concurrent mark: performs GC Roots tracing. It takes the longest time in the entire collection process and does not require a pause.
- Remark: corrects mark records for objects whose marks changed because the user program continued running during concurrent marking. It requires a pause.
- Concurrent sweep: does not require a pause.

During the longest phases, concurrent marking and concurrent sweeping, collector threads can work together with user threads without a pause.

It has the following drawbacks:

- Low throughput: low pause time is achieved at the cost of throughput, resulting in insufficient CPU utilization.
- Cannot handle floating garbage and may encounter Concurrent Mode Failure. Floating garbage is garbage generated while user threads continue running during the concurrent sweep phase; it can be collected only during the next GC. Because floating garbage exists, some memory must be reserved, meaning CMS cannot wait until the old generation is almost full before collecting like other collectors. If the reserved memory is not enough to hold floating garbage, Concurrent Mode Failure occurs, and the virtual machine temporarily enables Serial Old as a replacement for CMS.
- Space fragmentation caused by the mark-sweep algorithm often leaves remaining old-generation space but no sufficiently large contiguous region to allocate the current object, forcing an early Full GC.

#### 7. G1 Collector

G1, or Garbage-First, is a garbage collector for server-side applications. It performs well in multi-CPU and large-memory scenarios. The HotSpot development team designed it to eventually replace the CMS collector.

The heap is divided into the young generation and old generation. Other collectors collect either the entire young generation or the old generation, while G1 can collect the young and old generations together.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/4cf711a8-7ab2-4152-b85c-d5c226733807.png" width="600"/> </div><br>

G1 divides the heap into multiple independent, equal-sized regions. The young generation and old generation are no longer physically separated.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/9bbddeeb-e939-41f0-8e8e-2b1a0aa7e0a7.png" width="600"/> </div><br>

Introducing the concept of regions divides the original contiguous memory space into many smaller spaces, allowing each small space to be collected independently. This division provides great flexibility and makes a predictable pause-time model possible. G1 records the garbage-collection time of each region and the space recovered from it, based on past collection experience, and maintains a priority list. Each time, based on the allowed collection time, it prioritizes collecting the regions with the highest value.

Each region has a Remembered Set that records the regions containing objects referenced by objects in that region. By using Remembered Sets, full-heap scans can be avoided during reachability analysis.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f99ee771-c56f-47fb-9148-c0036695b5fe.jpg" width=""/> </div><br>

Ignoring the cost of maintaining Remembered Sets, the G1 collector's operation can be roughly divided into the following steps:

- Initial mark
- Concurrent mark
- Final mark: to correct mark records that changed because the user program continued running during concurrent marking, the virtual machine records object changes during this period in each thread's Remembered Set Logs. In the final mark phase, the Remembered Set Logs must be merged into the Remembered Sets. This phase requires pausing threads, but it can execute in parallel.
- Evacuation selection: first sorts each region by collection value and cost, then creates a collection plan based on the user's expected GC pause time. This phase can theoretically execute concurrently with the user program, but because only part of the regions are collected, the time is controllable by the user, and pausing user threads greatly improves collection efficiency.

It has the following characteristics:

- Space compaction: overall, it is implemented based on the mark-compact algorithm; locally, between two regions, it is implemented based on the copying algorithm. This means memory fragmentation is not produced during execution.
- Predictable pauses: users can explicitly specify that, within a time slice of M milliseconds, time spent on GC must not exceed N milliseconds.

## 3. Memory Allocation and Collection Strategies

### Minor GC and Full GC

- Minor GC: collects the young generation. Because young-generation objects have short lifetimes, Minor GC runs frequently and is generally fast.

- Full GC: collects the old generation and young generation. Old-generation objects have long lifetimes, so Full GC runs rarely and is much slower than Minor GC.

### Memory Allocation Strategy

#### 1. Objects Prefer Eden Allocation

In most cases, objects are allocated in the young-generation Eden space. When Eden does not have enough space, a Minor GC is triggered.

#### 2. Large Objects Go Directly to Old Generation

Large objects are objects that require contiguous memory space. Typical large objects include very long strings and arrays.

Frequent large objects can trigger garbage collection early to obtain enough contiguous space for allocation.

-XX:PretenureSizeThreshold causes objects larger than this value to be allocated directly in the old generation, avoiding large memory copies between Eden and Survivor spaces.

#### 3. Long-Lived Objects Enter Old Generation

An age counter is defined for each object. An object is born in Eden. If it survives a Minor GC, it is moved to Survivor and its age increases by 1. When its age reaches a certain threshold, it is moved to the old generation.

-XX:MaxTenuringThreshold defines the age threshold.

#### 4. Dynamic Object Age Determination

The virtual machine does not always require an object's age to reach MaxTenuringThreshold before promotion to the old generation. If the total size of all objects of the same age in Survivor is greater than half of the Survivor space, objects whose age is greater than or equal to that age can enter the old generation directly without waiting for the age required by MaxTenuringThreshold.

#### 5. Space Allocation Guarantee

Before a Minor GC occurs, the virtual machine first checks whether the largest available contiguous space in the old generation is greater than the total space of all objects in the young generation. If so, the Minor GC is considered safe.

If not, the virtual machine checks whether the value of HandlePromotionFailure allows allocation guarantee failure. If it does, it continues checking whether the largest available contiguous space in the old generation is greater than the average size of objects promoted to the old generation in previous collections. If it is greater, it tries a Minor GC. If it is smaller, or if HandlePromotionFailure does not allow the risk, a Full GC is performed.

### Full GC Trigger Conditions

For Minor GC, the trigger condition is simple: when Eden is full, a Minor GC is triggered. Full GC is more complex and has the following conditions:

#### 1. Call System.gc()

This only suggests that the virtual machine perform a Full GC; the virtual machine may not actually do it. This approach is not recommended. Let the virtual machine manage memory instead.

#### 2. Insufficient Old Generation Space

Common scenarios for insufficient old-generation space include large objects entering the old generation directly, as described above, and long-lived objects entering the old generation.

To avoid Full GC caused by these reasons, avoid creating overly large objects and arrays where possible. In addition, use the -Xmn virtual-machine parameter to increase the young-generation size so objects are collected in the young generation as much as possible instead of entering the old generation. You can also increase the age at which objects enter the old generation with -XX:MaxTenuringThreshold, allowing objects to survive longer in the young generation.

#### 3. Space Allocation Guarantee Failure

Minor GC using the copying algorithm requires old-generation memory space as an allocation guarantee. If the guarantee fails, a Full GC is performed. See section 5 above for details.

#### 4. Insufficient Permanent Generation Space in JDK 1.7 and Earlier

In JDK 1.7 and earlier, the method area in the HotSpot virtual machine is implemented with the permanent generation, which stores data such as Class information, constants, and static variables.

When the system needs to load many classes, reflect on many classes, or call many methods, the permanent generation may become full. If CMS GC is not configured, Full GC is also performed. If memory still cannot be reclaimed after Full GC, the virtual machine throws java.lang.OutOfMemoryError.

To avoid Full GC caused by this reason, increase the permanent-generation space or switch to CMS GC.

#### 5. Concurrent Mode Failure

If objects need to be placed into the old generation while CMS GC is running, and the old generation does not have enough space at that moment, possibly because too much floating garbage causes temporary space shortage during GC, a Concurrent Mode Failure error occurs and triggers Full GC.

## 4. Class Loading Mechanism

Classes are dynamically loaded the first time they are used during runtime, rather than all being loaded at once. Loading everything at once would consume a large amount of memory.

### Class Lifecycle

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/335fe19c-4a76-45ab-9320-88c90d6a0d7e.png" width="600px"> </div><br>

It includes the following seven phases:

-   **Loading**  
-   **Verification**  
-   **Preparation**  
-   **Resolution**  
-   **Initialization**  
- Using
- Unloading

### Class Loading Process

It includes five phases: loading, verification, preparation, resolution, and initialization.

#### 1. Loading

Loading is one phase of class loading. Do not confuse the two.

The loading process completes the following three tasks:

- Obtain the binary byte stream that defines the class through its fully qualified name.
- Convert the static storage structure represented by the byte stream into the runtime storage structure of the method area.
- Generate a Class object representing the class in memory, serving as the access entry to the class's data in the method area.


The binary byte stream can be obtained in the following ways:

- Read from a ZIP package, which is the basis for JAR, EAR, and WAR formats.
- Obtain from the network; the most typical application is Applet.
- Generate at runtime, such as the binary byte stream of proxy classes generated by ProxyGenerator.generateProxyClass in java.lang.reflect.Proxy for dynamic proxy technology.
- Generate from other files, such as generating the corresponding Class class from a JSP file.

#### 2. Verification

Ensures that the information contained in the byte stream of the Class file satisfies the requirements of the current virtual machine and does not endanger the virtual machine's own security.

#### 3. Preparation

Class variables are variables modified by static. The preparation phase allocates memory for class variables and sets their initial values, using memory from the method area.

Instance variables are not allocated memory in this phase. They are allocated in the heap along with the object when the object is instantiated. Note that instantiation is not part of class loading. Class loading happens before all instantiation operations, and class loading occurs only once, while instantiation can occur many times.

The initial value is generally a zero value. For example, the class variable value below is initialized to 0 rather than 123.

```java
public static int value = 123;
```

If the class variable is a constant, it is initialized to the value defined by the expression rather than 0. For example, the constant value below is initialized to 123 rather than 0.

```java
public static final int value = 123;
```

#### 4. Resolution

The process of replacing symbolic references in the constant pool with direct references.

In some cases, resolution can begin after the initialization phase. This supports Java's dynamic binding.

#### 5. Initialization

<div data="modify -->"></div>
The initialization phase is when the Java program code defined in the class truly begins to execute. It is the process in which the virtual machine executes the class constructor &lt;clinit\>() method. In the preparation phase, class variables have already been assigned system-required initial values. In the initialization phase, class variables and other resources are initialized according to the programmer's explicit plan in the program.

&lt;clinit\>() is generated by the compiler by automatically collecting and merging all class-variable assignment actions and statements in static blocks. The collection order is determined by the order in which statements appear in the source file. In particular, a static block can access only class variables defined before it. Class variables defined after it can be assigned but not accessed. For example:

```java
public class Test {
    static {
        i = 0;                // assigning the variable compiles normally
        System.out.print(i);  // the compiler reports "illegal forward reference" here
    }
    static int i = 1;
}
```

Because the parent class's &lt;clinit\>() method executes first, static blocks defined in the parent class execute before those in the subclass. For example:

```java
static class Parent {
    public static int A = 1;
    static {
        A = 2;
    }
}

static class Sub extends Parent {
    public static int B = A;
}

public static void main(String[] args) {
     System.out.println(Sub.B);  // 2
}
```

Static blocks cannot be used in interfaces, but interfaces still have assignment operations for class-variable initialization, so interfaces generate &lt;clinit\>() methods just like classes. Unlike classes, executing an interface's &lt;clinit\>() method does not require first executing the parent interface's &lt;clinit\>() method. The parent interface is initialized only when a variable defined in it is used. Also, when an interface implementation class is initialized, the interface's &lt;clinit\>() method is not executed.

The virtual machine guarantees that a class's &lt;clinit\>() method is correctly locked and synchronized in a multithreaded environment. If multiple threads initialize a class at the same time, only one thread executes that class's &lt;clinit\>() method, while the other threads block and wait until the active thread finishes executing it. If a time-consuming operation appears in a class's &lt;clinit\>() method, multiple threads may be blocked, and this kind of blocking can be very hidden in practice.

### Class Initialization Timing

#### 1. Active References

The virtual-machine specification does not strictly require when loading must occur, but it strictly states that class initialization must occur in exactly the following five cases. Loading, verification, and preparation will happen accordingly:

- When the four bytecode instructions new, getstatic, putstatic, and invokestatic are encountered, if the class has not been initialized, its initialization must be triggered first. The most common scenarios that generate these four instructions are instantiating an object with the new keyword, reading or setting a class's static field (except static fields modified by final whose results have already been placed into the constant pool at compile time), and calling a class's static method.

- When methods in the java.lang.reflect package are used to make reflective calls on a class, if the class has not been initialized, its initialization must be triggered first.

- When initializing a class, if its parent class has not yet been initialized, the parent class's initialization must be triggered first.

- When the virtual machine starts, the user must specify a main class to execute, namely the class containing main(). The virtual machine initializes this main class first.

- When using dynamic language support in JDK 1.7, if the final resolution result of a java.lang.invoke.MethodHandle instance is a method handle of REF_getStatic, REF_putStatic, or REF_invokeStatic, and the class corresponding to that method handle has not been initialized, its initialization must be triggered first.

#### 2. Passive References

The actions in the five scenarios above are called active references to a class. Other ways of referencing a class do not trigger initialization and are called passive references. Common examples of passive references include:

- Referencing a parent class's static field through a subclass does not initialize the subclass.

```java
System.out.println(SubClass.value);  // the value field is defined in SuperClass
```

- Referencing a class through an array definition does not trigger initialization of that class. This process initializes the array class, which is a subclass automatically generated by the virtual machine that directly extends Object and contains array properties and methods.

```java
SuperClass[] sca = new SuperClass[10];
```

- Constants are stored in the calling class's constant pool during compilation. They do not directly reference the class that defines the constant in essence, so initialization of the defining class is not triggered.

```java
System.out.println(ConstClass.HELLOWORLD);
```

### Classes and Class Loaders

For two classes to be equal, the classes themselves must be equal and must be loaded by the same class loader. This is because each class loader has an independent class namespace.

Equality here includes true return values from the equals(), isAssignableFrom(), and isInstance() methods of the class's Class object, as well as true results when using the instanceof keyword to determine object membership.

### Class Loader Classification

From the perspective of the Java Virtual Machine, only the following two different class loaders exist:

- Bootstrap ClassLoader, implemented in C++, and part of the virtual machine itself.

- Loaders for all other classes, implemented in Java, independent of the virtual machine, and inherited from the abstract class java.lang.ClassLoader.

From the perspective of Java developers, class loaders can be classified more finely:

- Bootstrap ClassLoader: responsible for loading class libraries stored in the &lt;JRE_HOME\>\lib directory, or in the path specified by the -Xbootclasspath parameter, into virtual-machine memory, as long as they are recognized by the virtual machine. Recognition is based only on file name, such as rt.jar; class libraries with unrecognized names will not be loaded even if placed in the lib directory. The bootstrap class loader cannot be directly referenced by Java programs. When writing a custom class loader, if a loading request needs to be delegated to the bootstrap class loader, use null instead.

- Extension ClassLoader: implemented by ExtClassLoader (sun.misc.Launcher$ExtClassLoader). It loads all class libraries in &lt;JAVA_HOME\>/lib/ext or in paths specified by the java.ext.dir system variable into memory. Developers can use the extension class loader directly.

- Application ClassLoader: implemented by AppClassLoader (sun.misc.Launcher$AppClassLoader). Because this class loader is the return value of ClassLoader's getSystemClassLoader() method, it is usually called the system class loader. It loads class libraries specified on the user class path (ClassPath). Developers can use this class loader directly. If an application has not customized its own class loader, this is generally the default class loader in the program.

### Parent Delegation Model

Applications implement class loading through cooperation among three class loaders. Custom class loaders can also be added.

The following figure shows the hierarchy among class loaders, called the parent delegation model. This model requires every class loader except the top-level bootstrap class loader to have its own parent class loader. The parent-child relationship here is generally implemented through composition, not inheritance.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/0dd2d40a-5b2b-4d45-b176-e75a4cd4bdbf.png" width="500px"> </div><br>

#### 1. Workflow

A class loader first forwards a class loading request to its parent class loader. It tries to load the class itself only when the parent class loader cannot complete the request.

#### 2. Benefits

It gives Java classes a priority-based hierarchy together with their class loaders, thereby keeping core classes unified.

For example, java.lang.Object is stored in rt.jar. If another java.lang.Object is written and placed in ClassPath, the program can compile. Because the parent delegation model exists, Object in rt.jar has higher priority than Object in ClassPath. This is because Object in rt.jar uses the bootstrap class loader, while Object in ClassPath uses the application class loader. Since Object in rt.jar has higher priority, every Object in the program is that Object.

#### 3. Implementation

The following is a code snippet from the abstract class java.lang.ClassLoader. The loadClass() method works as follows: first check whether the class has already been loaded; if not, ask the parent class loader to load it. When the parent class loader fails and throws ClassNotFoundException, it then tries to load the class itself.

```java
public abstract class ClassLoader {
    // The parent class loader for delegation
    private final ClassLoader parent;

    public Class<?> loadClass(String name) throws ClassNotFoundException {
        return loadClass(name, false);
    }

    protected Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {
        synchronized (getClassLoadingLock(name)) {
            // First, check if the class has already been loaded
            Class<?> c = findLoadedClass(name);
            if (c == null) {
                try {
                    if (parent != null) {
                        c = parent.loadClass(name, false);
                    } else {
                        c = findBootstrapClassOrNull(name);
                    }
                } catch (ClassNotFoundException e) {
                    // ClassNotFoundException thrown if class not found
                    // from the non-null parent class loader
                }

                if (c == null) {
                    // If still not found, then invoke findClass in order
                    // to find the class.
                    c = findClass(name);
                }
            }
            if (resolve) {
                resolveClass(c);
            }
            return c;
        }
    }

    protected Class<?> findClass(String name) throws ClassNotFoundException {
        throw new ClassNotFoundException(name);
    }
}
```

### Custom Class Loader Implementation

FileSystemClassLoader in the following code is a custom class loader. It extends java.lang.ClassLoader and is used to load classes from the file system. It first searches the file system for the class bytecode file (.class file) based on the class's fully qualified name, then reads the file content, and finally converts the bytecode into an instance of java.lang.Class through defineClass().

java.lang.ClassLoader's loadClass() implements the logic of the parent delegation model. Custom class loaders generally do not override it, but they need to override findClass().

```java
public class FileSystemClassLoader extends ClassLoader {

    private String rootDir;

    public FileSystemClassLoader(String rootDir) {
        this.rootDir = rootDir;
    }

    protected Class<?> findClass(String name) throws ClassNotFoundException {
        byte[] classData = getClassData(name);
        if (classData == null) {
            throw new ClassNotFoundException();
        } else {
            return defineClass(name, classData, 0, classData.length);
        }
    }

    private byte[] getClassData(String className) {
        String path = classNameToPath(className);
        try {
            InputStream ins = new FileInputStream(path);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            int bufferSize = 4096;
            byte[] buffer = new byte[bufferSize];
            int bytesNumRead;
            while ((bytesNumRead = ins.read(buffer)) != -1) {
                baos.write(buffer, 0, bytesNumRead);
            }
            return baos.toByteArray();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    private String classNameToPath(String className) {
        return rootDir + File.separatorChar
                + className.replace('.', File.separatorChar) + ".class";
    }
}
```

## References

- Zhou Zhiming. Understanding the Java Virtual Machine [M]. China Machine Press, 2011.
- [Chapter 2. The Structure of the Java Virtual Machine](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-2.html#jvms-2.5.4)
- [Jvm memory](https://www.slideshare.net/benewu/jvm-memory)
[Getting Started with the G1 Garbage Collector](http://www.oracle.com/webfolder/technetwork/tutorials/obe/java/G1GettingStarted/index.html)
- [JNI Part1: Java Native Interface Introduction and “Hello World” application](http://electrofriends.com/articles/jni/jni-part1-java-native-interface/)
- [Memory Architecture Of JVM(Runtime Data Areas)](https://hackthejava.wordpress.com/2015/01/09/memory-architecture-by-jvmruntime-data-areas/)
- [JVM Run-Time Data Areas](https://www.programcreek.com/2013/04/jvm-run-time-data-areas/)
- [Android on x86: Java Native Interface and the Android Native Development Kit](http://www.drdobbs.com/architecture-and-design/android-on-x86-java-native-interface-and/240166271)
- [Understanding the JVM (2): GC Algorithms and Memory Allocation Strategies](https://crowhawk.github.io/2017/08/10/jvm_2/)
- [Understanding the JVM (3): Seven Garbage Collectors](https://crowhawk.github.io/2017/08/15/jvm_3/)
- [JVM Internals](http://blog.jamesdbloom.com/JVMInternals.html)
- [In-Depth Discussion of Java Class Loaders](https://www.ibm.com/developerworks/cn/java/j-lo-classloader/index.html#code6)
- [Guide to WeakHashMap in Java](http://www.baeldung.com/java-weakhashmap)
- [Tomcat example source code file (ConcurrentCache.java)](https://alvinalexander.com/java/jwarehouse/apache-tomcat-6.0.16/java/org/apache/el/util/ConcurrentCache.java.shtml)
