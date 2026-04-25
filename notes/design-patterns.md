<!-- GFM-TOC -->
* [1. Overview](#1-overview)
* [2. Creational Patterns](#2-creational-patterns)
    * [1. Singleton](#1-singleton)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [Examples](#examples)
        * [JDK](#jdk)
    * [2. Simple Factory](#2-simple-factory)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
    * [3. Factory Method](#3-factory-method)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [4. Abstract Factory](#4-abstract-factory)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [5. Builder](#5-builder)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [6. Prototype](#6-prototype)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
* [3. Behavioral Patterns](#3-behavioral-patterns)
    * [1. Chain of Responsibility](#1-chain-of-responsibility)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [2. Command](#2-command)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [3. Interpreter](#3-interpreter)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [4. Iterator](#4-iterator)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [5. Mediator](#5-mediator)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [6. Memento](#6-memento)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [7. Observer](#7-observer)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [8. State](#8-state)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
    * [9. Strategy](#9-strategy)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Comparison with State Pattern](#comparison-with-state-pattern)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [10. Template Method](#10-template-method)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [11. Visitor](#11-visitor)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [12. Null Object](#12-null-object)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
* [4. Structural Patterns](#4-structural-patterns)
    * [1. Adapter](#1-adapter)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [2. Bridge](#2-bridge)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [3. Composite](#3-composite)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [4. Decorator](#4-decorator)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [Design Principles](#design-principles)
        * [JDK](#jdk)
    * [5. Facade](#5-facade)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [Design Principles](#design-principles)
    * [6. Flyweight](#6-flyweight)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
    * [7. Proxy](#7-proxy)
        * [Intent](#intent)
        * [Class Diagram](#class-diagram)
        * [Implementation](#implementation)
        * [JDK](#jdk)
* [References](#references)
<!-- GFM-TOC -->


# 1. Overview

Design patterns are reusable solutions to common problems. Studying established patterns lets you reuse proven experience.

A shared design pattern vocabulary makes technical discussions shorter and clearer without requiring everyone to revisit low-level details.

# 2. Creational Patterns

## 1. Singleton

### Intent

Ensure that a class has only one instance and provide a global access point to that instance.

### Class Diagram

Implement this with a private constructor, a private static variable, and a public static method.

The private constructor prevents object instances from being created directly through the constructor. The only instance is returned through the public static method.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/eca1f422-8381-409b-ad04-98ef39ae38ba.png"/> </div><br>

### Implementation

#### I. Lazy Initialization - Not Thread Safe

In the following implementation, the private static variable `uniqueInstance` is lazily instantiated. The benefit is that if the class is never used, `uniqueInstance` is never created, saving resources.

This implementation is unsafe in a multithreaded environment. If multiple threads enter `if (uniqueInstance == null)` at the same time while `uniqueInstance` is null, multiple threads may execute `uniqueInstance = new Singleton();`, causing `uniqueInstance` to be instantiated more than once.

```java
public class Singleton {

    private static Singleton uniqueInstance;

    private Singleton() {
    }

    public static Singleton getUniqueInstance() {
        if (uniqueInstance == null) {
            uniqueInstance = new Singleton();
        }
        return uniqueInstance;
    }
}
```

#### II. Eager Initialization - Thread Safe

The thread-safety issue mainly comes from `uniqueInstance` being instantiated multiple times. Directly instantiating `uniqueInstance` avoids this issue.

However, direct instantiation loses the resource-saving benefit of lazy initialization.

```java
private static Singleton uniqueInstance = new Singleton();
```

#### III. Lazy Initialization - Thread Safe

Locking the `getUniqueInstance()` method ensures that only one thread can enter it at a time, preventing `uniqueInstance` from being instantiated multiple times.

However, once one thread enters the method, every other thread attempting to enter it must wait, even if `uniqueInstance` has already been instantiated. This can block threads for too long, so this approach has performance problems and is not recommended.

```java
public static synchronized Singleton getUniqueInstance() {
    if (uniqueInstance == null) {
        uniqueInstance = new Singleton();
    }
    return uniqueInstance;
}
```

#### IV. Double-Checked Locking - Thread Safe

`uniqueInstance` only needs to be instantiated once and can then be used directly. Locking is only needed around the instantiation code, and only when `uniqueInstance` has not yet been created.

Double-checked locking first checks whether `uniqueInstance` has already been instantiated. If not, it locks around the instantiation statement.

```java
public class Singleton {

    private volatile static Singleton uniqueInstance;

    private Singleton() {
    }

    public static Singleton getUniqueInstance() {
        if (uniqueInstance == null) {
            synchronized (Singleton.class) {
                if (uniqueInstance == null) {
                    uniqueInstance = new Singleton();
                }
            }
        }
        return uniqueInstance;
    }
}
```

Consider the implementation below, which uses only one `if` statement. When `uniqueInstance == null`, if two threads both execute the `if` statement, both enter the `if` block. Although the block contains a lock, both threads will still execute `uniqueInstance = new Singleton();`; the only difference is order, so instantiation happens twice. Therefore, double-checked locking is required, using two `if` statements: the first avoids locking after `uniqueInstance` has already been instantiated, and the second is protected by the lock so only one thread can enter it. This prevents two threads from instantiating `uniqueInstance` at the same time when it is null.

```java
if (uniqueInstance == null) {
    synchronized (Singleton.class) {
        uniqueInstance = new Singleton();
    }
}
```

It is also necessary to declare `uniqueInstance` with the `volatile` keyword. The statement `uniqueInstance = new Singleton();` is actually executed in three steps:

1. Allocate memory for `uniqueInstance`.
2. Initialize `uniqueInstance`.
3. Point `uniqueInstance` to the allocated memory address.

Because the JVM can reorder instructions, the execution order may become 1 > 3 > 2. Instruction reordering is not a problem in a single-threaded environment, but in a multithreaded environment it can let one thread obtain an instance that has not been initialized yet. For example, thread T<sub>1</sub> executes steps 1 and 3. Then T<sub>2</sub> calls `getUniqueInstance()`, sees that `uniqueInstance` is not null, and returns it, even though it has not yet been initialized.

Using `volatile` prevents JVM instruction reordering and ensures correct behavior in a multithreaded environment.

#### V. Static Inner Class

When the `Singleton` class is loaded, the static inner class `SingletonHolder` is not loaded into memory. Only when `getUniqueInstance()` is called and triggers `SingletonHolder.INSTANCE` is `SingletonHolder` loaded. At that point, the `INSTANCE` object is initialized, and the JVM guarantees that `INSTANCE` is instantiated only once.

This approach provides lazy initialization and relies on the JVM for thread-safety guarantees.

```java
public class Singleton {

    private Singleton() {
    }

    private static class SingletonHolder {
        private static final Singleton INSTANCE = new Singleton();
    }

    public static Singleton getUniqueInstance() {
        return SingletonHolder.INSTANCE;
    }
}
```

#### VI. Enum

```java
public enum Singleton {

    INSTANCE;

    private String objName;


    public String getObjName() {
        return objName;
    }


    public void setObjName(String objName) {
        this.objName = objName;
    }


    public static void main(String[] args) {

        // Singleton test
        Singleton firstSingleton = Singleton.INSTANCE;
        firstSingleton.setObjName("firstName");
        System.out.println(firstSingleton.getObjName());
        Singleton secondSingleton = Singleton.INSTANCE;
        secondSingleton.setObjName("secondName");
        System.out.println(firstSingleton.getObjName());
        System.out.println(secondSingleton.getObjName());

        // Reflection-based instance retrieval test
        try {
            Singleton[] enumConstants = Singleton.class.getEnumConstants();
            for (Singleton enumConstant : enumConstants) {
                System.out.println(enumConstant.getObjName());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

```html
firstName
secondName
secondName
secondName
```

This implementation prevents reflection attacks. In other implementations, `setAccessible()` can change a private constructor to public, allowing the constructor to be called and a new object to be instantiated. To prevent that attack, the constructor must include code that blocks multiple instantiations. This implementation relies on the JVM to guarantee a single instantiation, so the reflection attack above does not occur.

This implementation will not produce multiple instances after repeated serialization and deserialization. Other implementations need to mark all fields with `transient` and implement serialization and deserialization methods.

### Examples

- Logger Classes
- Configuration Classes
- Accesing resources in shared mode
- Factories implemented as Singletons

### JDK

- [java.lang.Runtime#getRuntime()](http://docs.oracle.com/javase/8/docs/api/java/lang/Runtime.html#getRuntime%28%29)
- [java.awt.Desktop#getDesktop()](http://docs.oracle.com/javase/8/docs/api/java/awt/Desktop.html#getDesktop--)
- [java.lang.System#getSecurityManager()](http://docs.oracle.com/javase/8/docs/api/java/lang/System.html#getSecurityManager--)

## 2. Simple Factory

### Intent

Provide a common interface for creating objects without exposing creation details to clients.

### Class Diagram

Simple Factory places instantiation logic in a separate class. That class becomes the simple factory and decides which concrete subclass should be instantiated.

This decouples client classes from concrete subclass implementations. Clients no longer need to know which subclasses exist or which one should be instantiated. There are often many clients; without Simple Factory, every client must know the details of every subclass. If a subclass changes, such as when a new subclass is added, all client classes would need to be modified.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/40c0c17e-bba6-4493-9857-147c0044a018.png"/> </div><br>

### Implementation

```java
public interface Product {
}
```

```java
public class ConcreteProduct implements Product {
}
```

```java
public class ConcreteProduct1 implements Product {
}
```

```java
public class ConcreteProduct2 implements Product {
}
```

The following Client class contains instantiation code, which is a poor implementation. If this kind of instantiation code appears in a client class, consider moving it into a simple factory.

```java
public class Client {

    public static void main(String[] args) {
        int type = 1;
        Product product;
        if (type == 1) {
            product = new ConcreteProduct1();
        } else if (type == 2) {
            product = new ConcreteProduct2();
        } else {
            product = new ConcreteProduct();
        }
        // do something with the product
    }
}
```

The following `SimpleFactory` is a simple factory implementation. It is called by all client classes that need instantiation.

```java
public class SimpleFactory {

    public Product createProduct(int type) {
        if (type == 1) {
            return new ConcreteProduct1();
        } else if (type == 2) {
            return new ConcreteProduct2();
        }
        return new ConcreteProduct();
    }
}
```

```java
public class Client {

    public static void main(String[] args) {
        SimpleFactory simpleFactory = new SimpleFactory();
        Product product = simpleFactory.createProduct(1);
        // do something with the product
    }
}
```

## 3. Factory Method

### Intent

Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method defers instantiation to subclasses.

### Class Diagram

In Simple Factory, another class creates the object. In Factory Method, subclasses create the object.

In the diagram below, `Factory` has a `doSomething()` method that needs a product object. The product object is created by `factoryMethod()`, which is abstract and must be implemented by subclasses.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f4d0afd0-8e78-4914-9e60-4366eaf065b5.png"/> </div><br>

### Implementation

```java
public abstract class Factory {
    abstract public Product factoryMethod();
    public void doSomething() {
        Product product = factoryMethod();
        // do something with the product
    }
}
```

```java
public class ConcreteFactory extends Factory {
    public Product factoryMethod() {
        return new ConcreteProduct();
    }
}
```

```java
public class ConcreteFactory1 extends Factory {
    public Product factoryMethod() {
        return new ConcreteProduct1();
    }
}
```

```java
public class ConcreteFactory2 extends Factory {
    public Product factoryMethod() {
        return new ConcreteProduct2();
    }
}
```

### JDK

- [java.util.Calendar](http://docs.oracle.com/javase/8/docs/api/java/util/Calendar.html#getInstance--)
- [java.util.ResourceBundle](http://docs.oracle.com/javase/8/docs/api/java/util/ResourceBundle.html#getBundle-java.lang.String-)
- [java.text.NumberFormat](http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html#getInstance--)
- [java.nio.charset.Charset](http://docs.oracle.com/javase/8/docs/api/java/nio/charset/Charset.html#forName-java.lang.String-)
- [java.net.URLStreamHandlerFactory](http://docs.oracle.com/javase/8/docs/api/java/net/URLStreamHandlerFactory.html#createURLStreamHandler-java.lang.String-)
- [java.util.EnumSet](https://docs.oracle.com/javase/8/docs/api/java/util/EnumSet.html#of-E-)
- [javax.xml.bind.JAXBContext](https://docs.oracle.com/javase/8/docs/api/javax/xml/bind/JAXBContext.html#createMarshaller--)

## 4. Abstract Factory

### Intent

Provide an interface for creating **families of related objects**.

### Class Diagram

The Abstract Factory pattern creates a family of objects: multiple related objects that must be created together. By contrast, Factory Method creates a single object, which is a major difference from Abstract Factory.

Abstract Factory uses Factory Method to create individual objects. In `AbstractFactory`, both `createProductA()` and `createProductB()` are implemented by subclasses; viewed separately, each method creates one object, which matches the definition of Factory Method.

The idea of creating a family of objects appears in the Client. The Client calls two methods on `AbstractFactory` to create two objects at the same time; these objects are strongly related, so the Client needs to create them together.

At a high level, Abstract Factory uses composition: the Client composes an `AbstractFactory`. Factory Method uses inheritance.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e2190c36-8b27-4690-bde5-9911020a1294.png"/> </div><br>

### Implementation

```java
public class AbstractProductA {
}
```

```java
public class AbstractProductB {
}
```

```java
public class ProductA1 extends AbstractProductA {
}
```

```java
public class ProductA2 extends AbstractProductA {
}
```

```java
public class ProductB1 extends AbstractProductB {
}
```

```java
public class ProductB2 extends AbstractProductB {
}
```

```java
public abstract class AbstractFactory {
    abstract AbstractProductA createProductA();
    abstract AbstractProductB createProductB();
}
```

```java
public class ConcreteFactory1 extends AbstractFactory {
    AbstractProductA createProductA() {
        return new ProductA1();
    }

    AbstractProductB createProductB() {
        return new ProductB1();
    }
}
```

```java
public class ConcreteFactory2 extends AbstractFactory {
    AbstractProductA createProductA() {
        return new ProductA2();
    }

    AbstractProductB createProductB() {
        return new ProductB2();
    }
}
```

```java
public class Client {
    public static void main(String[] args) {
        AbstractFactory abstractFactory = new ConcreteFactory1();
        AbstractProductA productA = abstractFactory.createProductA();
        AbstractProductB productB = abstractFactory.createProductB();
        // do something with productA and productB
    }
}
```

### JDK

- [javax.xml.parsers.DocumentBuilderFactory](http://docs.oracle.com/javase/8/docs/api/javax/xml/parsers/DocumentBuilderFactory.html)
- [javax.xml.transform.TransformerFactory](http://docs.oracle.com/javase/8/docs/api/javax/xml/transform/TransformerFactory.html#newInstance--)
- [javax.xml.xpath.XPathFactory](http://docs.oracle.com/javase/8/docs/api/javax/xml/xpath/XPathFactory.html#newInstance--)

## 5. Builder

### Intent

Encapsulate the construction process of an object and allow it to be built step by step.

### Class Diagram

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/db5e376d-0b3e-490e-a43a-3231914b6668.png"/> </div><br>

### Implementation

The following is a simplified `StringBuilder` implementation based on the JDK 1.8 source code.

```java
public class AbstractStringBuilder {
    protected char[] value;

    protected int count;

    public AbstractStringBuilder(int capacity) {
        count = 0;
        value = new char[capacity];
    }

    public AbstractStringBuilder append(char c) {
        ensureCapacityInternal(count + 1);
        value[count++] = c;
        return this;
    }

    private void ensureCapacityInternal(int minimumCapacity) {
        // overflow-conscious code
        if (minimumCapacity - value.length > 0)
            expandCapacity(minimumCapacity);
    }

    void expandCapacity(int minimumCapacity) {
        int newCapacity = value.length * 2 + 2;
        if (newCapacity - minimumCapacity < 0)
            newCapacity = minimumCapacity;
        if (newCapacity < 0) {
            if (minimumCapacity < 0) // overflow
                throw new OutOfMemoryError();
            newCapacity = Integer.MAX_VALUE;
        }
        value = Arrays.copyOf(value, newCapacity);
    }
}
```

```java
public class StringBuilder extends AbstractStringBuilder {
    public StringBuilder() {
        super(16);
    }

    @Override
    public String toString() {
        // Create a copy, don't share the array
        return new String(value, 0, count);
    }
}
```

```java
public class Client {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        final int count = 26;
        for (int i = 0; i < count; i++) {
            sb.append((char) ('a' + i));
        }
        System.out.println(sb.toString());
    }
}
```

```html
abcdefghijklmnopqrstuvwxyz
```

### JDK

- [java.lang.StringBuilder](http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuilder.html)
- [java.nio.ByteBuffer](http://docs.oracle.com/javase/8/docs/api/java/nio/ByteBuffer.html#put-byte-)
- [java.lang.StringBuffer](http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html#append-boolean-)
- [java.lang.Appendable](http://docs.oracle.com/javase/8/docs/api/java/lang/Appendable.html)
- [Apache Camel builders](https://github.com/apache/camel/tree/0e195428ee04531be27a0b659005e3aa8d159d23/camel-core/src/main/java/org/apache/camel/builder)

## 6. Prototype

### Intent

Specify the type of object to create using a prototype instance, then create new objects by copying that prototype.

### Class Diagram

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/b8922f8c-95e6-4187-be85-572a509afb71.png"/> </div><br>

### Implementation

```java
public abstract class Prototype {
    abstract Prototype myClone();
}
```

```java
public class ConcretePrototype extends Prototype {

    private String filed;

    public ConcretePrototype(String filed) {
        this.filed = filed;
    }

    @Override
    Prototype myClone() {
        return new ConcretePrototype(filed);
    }

    @Override
    public String toString() {
        return filed;
    }
}
```

```java
public class Client {
    public static void main(String[] args) {
        Prototype prototype = new ConcretePrototype("abc");
        Prototype clone = prototype.myClone();
        System.out.println(clone.toString());
    }
}
```

```html
abc
```

### JDK

- [java.lang.Object#clone()](http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html#clone%28%29)

# 3. Behavioral Patterns

## 1. Chain of Responsibility

### Intent

Give multiple objects a chance to handle a request, avoiding coupling between the sender and receiver. Chain these objects together and pass the request along the chain until one object handles it.

### Class Diagram

- Handler: defines the interface for handling requests and maintains the successor chain.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ca9f23bf-55a4-47b2-9534-a28e35397988.png"/> </div><br>

### Implementation

```java
public abstract class Handler {

    protected Handler successor;


    public Handler(Handler successor) {
        this.successor = successor;
    }


    protected abstract void handleRequest(Request request);
}
```

```java
public class ConcreteHandler1 extends Handler {

    public ConcreteHandler1(Handler successor) {
        super(successor);
    }


    @Override
    protected void handleRequest(Request request) {
        if (request.getType() == RequestType.TYPE1) {
            System.out.println(request.getName() + " is handle by ConcreteHandler1");
            return;
        }
        if (successor != null) {
            successor.handleRequest(request);
        }
    }
}
```

```java
public class ConcreteHandler2 extends Handler {

    public ConcreteHandler2(Handler successor) {
        super(successor);
    }


    @Override
    protected void handleRequest(Request request) {
        if (request.getType() == RequestType.TYPE2) {
            System.out.println(request.getName() + " is handle by ConcreteHandler2");
            return;
        }
        if (successor != null) {
            successor.handleRequest(request);
        }
    }
}
```

```java
public class Request {

    private RequestType type;
    private String name;


    public Request(RequestType type, String name) {
        this.type = type;
        this.name = name;
    }


    public RequestType getType() {
        return type;
    }


    public String getName() {
        return name;
    }
}

```

```java
public enum RequestType {
    TYPE1, TYPE2
}
```

```java
public class Client {

    public static void main(String[] args) {

        Handler handler1 = new ConcreteHandler1(null);
        Handler handler2 = new ConcreteHandler2(handler1);

        Request request1 = new Request(RequestType.TYPE1, "request1");
        handler2.handleRequest(request1);

        Request request2 = new Request(RequestType.TYPE2, "request2");
        handler2.handleRequest(request2);
    }
}
```

```html
request1 is handle by ConcreteHandler1
request2 is handle by ConcreteHandler2
```

### JDK

- [java.util.logging.Logger#log()](http://docs.oracle.com/javase/8/docs/api/java/util/logging/Logger.html#log%28java.util.logging.Level,%20java.lang.String%29)
- [Apache Commons Chain](https://commons.apache.org/proper/commons-chain/index.html)
- [javax.servlet.Filter#doFilter()](http://docs.oracle.com/javaee/7/api/javax/servlet/Filter.html#doFilter-javax.servlet.ServletRequest-javax.servlet.ServletResponse-javax.servlet.FilterChain-)

## 2. Command

### Intent

Encapsulate a command as an object, which enables the following:

- Parameterize other objects with commands.
- Put commands into a queue.
- Log command operations.
- Support undoable operations.

### Class Diagram

- Command: the command.
- Receiver: receives the command and performs the actual work.
- Invoker: calls the command.
- Client: configures commands and their receivers.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/c44a0342-f405-4f17-b750-e27cf4aadde2.png"/> </div><br>

### Implementation

Design a remote control that can switch a light on and off.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e6bded8e-41a0-489a-88a6-638e88ab7666.jpg"/> </div><br>

```java
public interface Command {
    void execute();
}
```

```java
public class LightOnCommand implements Command {
    Light light;

    public LightOnCommand(Light light) {
        this.light = light;
    }

    @Override
    public void execute() {
        light.on();
    }
}
```

```java
public class LightOffCommand implements Command {
    Light light;

    public LightOffCommand(Light light) {
        this.light = light;
    }

    @Override
    public void execute() {
        light.off();
    }
}
```

```java
public class Light {

    public void on() {
        System.out.println("Light is on!");
    }

    public void off() {
        System.out.println("Light is off!");
    }
}
```

```java
/**
 * Remote control
 */
public class Invoker {
    private Command[] onCommands;
    private Command[] offCommands;
    private final int slotNum = 7;

    public Invoker() {
        this.onCommands = new Command[slotNum];
        this.offCommands = new Command[slotNum];
    }

    public void setOnCommand(Command command, int slot) {
        onCommands[slot] = command;
    }

    public void setOffCommand(Command command, int slot) {
        offCommands[slot] = command;
    }

    public void onButtonWasPushed(int slot) {
        onCommands[slot].execute();
    }

    public void offButtonWasPushed(int slot) {
        offCommands[slot].execute();
    }
}
```

```java
public class Client {
    public static void main(String[] args) {
        Invoker invoker = new Invoker();
        Light light = new Light();
        Command lightOnCommand = new LightOnCommand(light);
        Command lightOffCommand = new LightOffCommand(light);
        invoker.setOnCommand(lightOnCommand, 0);
        invoker.setOffCommand(lightOffCommand, 0);
        invoker.onButtonWasPushed(0);
        invoker.offButtonWasPushed(0);
    }
}
```

### JDK

- [java.lang.Runnable](http://docs.oracle.com/javase/8/docs/api/java/lang/Runnable.html)
- [Netflix Hystrix](https://github.com/Netflix/Hystrix/wiki)
- [javax.swing.Action](http://docs.oracle.com/javase/8/docs/api/javax/swing/Action.html)

## 3. Interpreter

### Intent

Create an interpreter for a language, usually defined by the language grammar and parser.

### Class Diagram

- TerminalExpression: a terminal expression. Each terminal symbol requires a TerminalExpression.
- Context: holds global information outside the interpreter.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2b125bcd-1b36-43be-9b78-d90b076be549.png"/> </div><br>

### Implementation

The following is a rule validator with `and` and `or` rules. Rules can be used to build a parse tree that checks whether a text satisfies the rules defined by that tree.

For example, given the parse tree `D And (A Or (B C))`, the text `"D A"` satisfies the rules defined by that tree.

Here, Context refers to `String`.

```java
public abstract class Expression {
    public abstract boolean interpret(String str);
}
```

```java
public class TerminalExpression extends Expression {

    private String literal = null;

    public TerminalExpression(String str) {
        literal = str;
    }

    public boolean interpret(String str) {
        StringTokenizer st = new StringTokenizer(str);
        while (st.hasMoreTokens()) {
            String test = st.nextToken();
            if (test.equals(literal)) {
                return true;
            }
        }
        return false;
    }
}
```

```java
public class AndExpression extends Expression {

    private Expression expression1 = null;
    private Expression expression2 = null;

    public AndExpression(Expression expression1, Expression expression2) {
        this.expression1 = expression1;
        this.expression2 = expression2;
    }

    public boolean interpret(String str) {
        return expression1.interpret(str) && expression2.interpret(str);
    }
}
```

```java
public class OrExpression extends Expression {
    private Expression expression1 = null;
    private Expression expression2 = null;

    public OrExpression(Expression expression1, Expression expression2) {
        this.expression1 = expression1;
        this.expression2 = expression2;
    }

    public boolean interpret(String str) {
        return expression1.interpret(str) || expression2.interpret(str);
    }
}
```

```java
public class Client {

    /**
     * Build the parse tree
     */
    public static Expression buildInterpreterTree() {
        // Literal
        Expression terminal1 = new TerminalExpression("A");
        Expression terminal2 = new TerminalExpression("B");
        Expression terminal3 = new TerminalExpression("C");
        Expression terminal4 = new TerminalExpression("D");
        // B C
        Expression alternation1 = new OrExpression(terminal2, terminal3);
        // A Or (B C)
        Expression alternation2 = new OrExpression(terminal1, alternation1);
        // D And (A Or (B C))
        return new AndExpression(terminal4, alternation2);
    }

    public static void main(String[] args) {
        Expression define = buildInterpreterTree();
        String context1 = "D A";
        String context2 = "A B";
        System.out.println(define.interpret(context1));
        System.out.println(define.interpret(context2));
    }
}
```

```html
true
false
```

### JDK

- [java.util.Pattern](http://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)
- [java.text.Normalizer](http://docs.oracle.com/javase/8/docs/api/java/text/Normalizer.html)
- All subclasses of [java.text.Format](http://docs.oracle.com/javase/8/docs/api/java/text/Format.html)
- [javax.el.ELResolver](http://docs.oracle.com/javaee/7/api/javax/el/ELResolver.html)

## 4. Iterator

### Intent

Provide a way to access the elements of an aggregate object sequentially without exposing its internal representation.

### Class Diagram

- Aggregate is the aggregate class, whose `createIterator()` method produces an Iterator.
- Iterator mainly defines the `hasNext()` and `next()` methods.
- Client composes Aggregate; to iterate over Aggregate, it also needs to compose Iterator.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/89292ae1-5f13-44dc-b508-3f035e80bf89.png"/> </div><br>

### Implementation

```java
public interface Aggregate {
    Iterator createIterator();
}
```

```java
public class ConcreteAggregate implements Aggregate {

    private Integer[] items;

    public ConcreteAggregate() {
        items = new Integer[10];
        for (int i = 0; i < items.length; i++) {
            items[i] = i;
        }
    }

    @Override
    public Iterator createIterator() {
        return new ConcreteIterator<Integer>(items);
    }
}
```

```java
public interface Iterator<Item> {

    Item next();

    boolean hasNext();
}
```

```java
public class ConcreteIterator<Item> implements Iterator {

    private Item[] items;
    private int position = 0;

    public ConcreteIterator(Item[] items) {
        this.items = items;
    }

    @Override
    public Object next() {
        return items[position++];
    }

    @Override
    public boolean hasNext() {
        return position < items.length;
    }
}
```

```java
public class Client {

    public static void main(String[] args) {
        Aggregate aggregate = new ConcreteAggregate();
        Iterator<Integer> iterator = aggregate.createIterator();
        while (iterator.hasNext()) {
            System.out.println(iterator.next());
        }
    }
}
```

### JDK

- [java.util.Iterator](http://docs.oracle.com/javase/8/docs/api/java/util/Iterator.html)
- [java.util.Enumeration](http://docs.oracle.com/javase/8/docs/api/java/util/Enumeration.html)

## 5. Mediator

### Intent

Centralize complex communication and control among related objects.

### Class Diagram

- Mediator: defines an interface for communicating with each Colleague object.
- Colleague: a related object that communicates through the Mediator.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/30d6e95c-2e3c-4d32-bf4f-68128a70bc05.png"/> </div><br>

### Implementation

Alarm, CoffeePot, Calendar, and Sprinkler are a group of related objects. When one object raises an event, it needs to operate on the others, creating the dependency structure below:

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/82cfda3b-b53b-4c89-9fdb-26dd2db0cd02.jpg"/> </div><br>

The Mediator pattern can turn this complex dependency structure into a star-shaped structure:

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/5359cbf5-5a79-4874-9b17-f23c53c2cb80.jpg"/> </div><br>

```java
public abstract class Colleague {
    public abstract void onEvent(Mediator mediator);
}
```

```java
public class Alarm extends Colleague {

    @Override
    public void onEvent(Mediator mediator) {
        mediator.doEvent("alarm");
    }

    public void doAlarm() {
        System.out.println("doAlarm()");
    }
}
```

```java
public class CoffeePot extends Colleague {
    @Override
    public void onEvent(Mediator mediator) {
        mediator.doEvent("coffeePot");
    }

    public void doCoffeePot() {
        System.out.println("doCoffeePot()");
    }
}
```

```java
public class Calender extends Colleague {
    @Override
    public void onEvent(Mediator mediator) {
        mediator.doEvent("calender");
    }

    public void doCalender() {
        System.out.println("doCalender()");
    }
}
```

```java
public class Sprinkler extends Colleague {
    @Override
    public void onEvent(Mediator mediator) {
        mediator.doEvent("sprinkler");
    }

    public void doSprinkler() {
        System.out.println("doSprinkler()");
    }
}
```

```java
public abstract class Mediator {
    public abstract void doEvent(String eventType);
}
```

```java
public class ConcreteMediator extends Mediator {
    private Alarm alarm;
    private CoffeePot coffeePot;
    private Calender calender;
    private Sprinkler sprinkler;

    public ConcreteMediator(Alarm alarm, CoffeePot coffeePot, Calender calender, Sprinkler sprinkler) {
        this.alarm = alarm;
        this.coffeePot = coffeePot;
        this.calender = calender;
        this.sprinkler = sprinkler;
    }

    @Override
    public void doEvent(String eventType) {
        switch (eventType) {
            case "alarm":
                doAlarmEvent();
                break;
            case "coffeePot":
                doCoffeePotEvent();
                break;
            case "calender":
                doCalenderEvent();
                break;
            default:
                doSprinklerEvent();
        }
    }

    public void doAlarmEvent() {
        alarm.doAlarm();
        coffeePot.doCoffeePot();
        calender.doCalender();
        sprinkler.doSprinkler();
    }

    public void doCoffeePotEvent() {
        // ...
    }

    public void doCalenderEvent() {
        // ...
    }

    public void doSprinklerEvent() {
        // ...
    }
}
```

```java
public class Client {
    public static void main(String[] args) {
        Alarm alarm = new Alarm();
        CoffeePot coffeePot = new CoffeePot();
        Calender calender = new Calender();
        Sprinkler sprinkler = new Sprinkler();
        Mediator mediator = new ConcreteMediator(alarm, coffeePot, calender, sprinkler);
        // When the alarm event arrives, call the mediator to operate on related objects
        alarm.onEvent(mediator);
    }
}
```

```java
doAlarm()
doCoffeePot()
doCalender()
doSprinkler()
```

### JDK

- All scheduleXXX() methods of [java.util.Timer](http://docs.oracle.com/javase/8/docs/api/java/util/Timer.html)
- [java.util.concurrent.Executor#execute()](http://docs.oracle.com/javase/8/docs/api/java/util/concurrent/Executor.html#execute-java.lang.Runnable-)
- submit() and invokeXXX() methods of [java.util.concurrent.ExecutorService](http://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ExecutorService.html)
- scheduleXXX() methods of [java.util.concurrent.ScheduledExecutorService](http://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ScheduledExecutorService.html)
- [java.lang.reflect.Method#invoke()](http://docs.oracle.com/javase/8/docs/api/java/lang/reflect/Method.html#invoke-java.lang.Object-java.lang.Object...-)

## 6. Memento

### Intent

Capture an object's internal state without violating encapsulation, so the object can be restored to that state later.

### Class Diagram

- Originator: the original object whose state is saved.
- Caretaker: responsible for storing the memento.
- Memento: stores the Originator's state. A memento effectively exposes two interfaces: a narrow interface for the Caretaker, which can only pass the memento to other objects, and a wider interface for the Originator, which can access all data needed to restore a previous state. Ideally, only the Originator can access the memento's internal state.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/50678f34-694f-45a4-91c6-34d985c83fee.png"/> </div><br>

### Implementation

The following example implements a simple calculator that accepts two values and returns their sum. The Memento pattern lets the calculator store those values and later restore them from the saved state.

Implementation reference: [Memento Pattern - Calculator Example - Java Sourcecode](https://www.oodesign.com/memento-pattern-calculator-example-java-sourcecode.html)

```java
/**
 * Originator Interface
 */
public interface Calculator {

    // Create Memento
    PreviousCalculationToCareTaker backupLastCalculation();

    // setMemento
    void restorePreviousCalculation(PreviousCalculationToCareTaker memento);

    int getCalculationResult();

    void setFirstNumber(int firstNumber);

    void setSecondNumber(int secondNumber);
}
```

```java
/**
 * Originator Implementation
 */
public class CalculatorImp implements Calculator {

    private int firstNumber;
    private int secondNumber;

    @Override
    public PreviousCalculationToCareTaker backupLastCalculation() {
        // create a memento object used for restoring two numbers
        return new PreviousCalculationImp(firstNumber, secondNumber);
    }

    @Override
    public void restorePreviousCalculation(PreviousCalculationToCareTaker memento) {
        this.firstNumber = ((PreviousCalculationToOriginator) memento).getFirstNumber();
        this.secondNumber = ((PreviousCalculationToOriginator) memento).getSecondNumber();
    }

    @Override
    public int getCalculationResult() {
        // result is adding two numbers
        return firstNumber + secondNumber;
    }

    @Override
    public void setFirstNumber(int firstNumber) {
        this.firstNumber = firstNumber;
    }

    @Override
    public void setSecondNumber(int secondNumber) {
        this.secondNumber = secondNumber;
    }
}
```

```java
/**
 * Memento Interface to Originator
 *
 * This interface allows the originator to restore its state
 */
public interface PreviousCalculationToOriginator {
    int getFirstNumber();
    int getSecondNumber();
}
```

```java
/**
 *  Memento interface to CalculatorOperator (Caretaker)
 */
public interface PreviousCalculationToCareTaker {
    // no operations permitted for the caretaker
}
```

```java
/**
 * Memento Object Implementation
 * <p>
 * Note that this object implements both interfaces to Originator and CareTaker
 */
public class PreviousCalculationImp implements PreviousCalculationToCareTaker,
        PreviousCalculationToOriginator {

    private int firstNumber;
    private int secondNumber;

    public PreviousCalculationImp(int firstNumber, int secondNumber) {
        this.firstNumber = firstNumber;
        this.secondNumber = secondNumber;
    }

    @Override
    public int getFirstNumber() {
        return firstNumber;
    }

    @Override
    public int getSecondNumber() {
        return secondNumber;
    }
}
```

```java
/**
 * CareTaker object
 */
public class Client {

    public static void main(String[] args) {
        // program starts
        Calculator calculator = new CalculatorImp();

        // assume user enters two numbers
        calculator.setFirstNumber(10);
        calculator.setSecondNumber(100);

        // find result
        System.out.println(calculator.getCalculationResult());

        // Store result of this calculation in case of error
        PreviousCalculationToCareTaker memento = calculator.backupLastCalculation();

        // user enters a number
        calculator.setFirstNumber(17);

        // user enters a wrong second number and calculates result
        calculator.setSecondNumber(-290);

        // calculate result
        System.out.println(calculator.getCalculationResult());

        // user hits CTRL + Z to undo last operation and see last result
        calculator.restorePreviousCalculation(memento);

        // result restored
        System.out.println(calculator.getCalculationResult());
    }
}
```

```html
110
-273
110
```

### JDK

- java.io.Serializable

## 7. Observer

### Intent

Define a one-to-many dependency between objects so that when one object changes state, all of its dependents are notified and update automatically.

The Subject is the observed object, and all of its dependents are Observers.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7a3c6a30-c735-4edb-8115-337288a4f0f2.jpg" width="600"/> </div><br>

### Class Diagram

The Subject can register observers, remove observers, and notify all observers. It implements these operations by maintaining a list of observers.

An Observer registers by calling the Subject's `registerObserver()` method.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a8c8f894-a712-447c-9906-5caef6a016e3.png"/> </div><br>

### Implementation

Weather data displays update their content when weather information changes. There are multiple displays, and more may be added later.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/b1df9732-86ce-4d69-9f06-fba1db7b3b5a.jpg"/> </div><br>

```java
public interface Subject {
    void registerObserver(Observer o);

    void removeObserver(Observer o);

    void notifyObserver();
}
```

```java
public class WeatherData implements Subject {
    private List<Observer> observers;
    private float temperature;
    private float humidity;
    private float pressure;

    public WeatherData() {
        observers = new ArrayList<>();
    }

    public void setMeasurements(float temperature, float humidity, float pressure) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.pressure = pressure;
        notifyObserver();
    }

    @Override
    public void registerObserver(Observer o) {
        observers.add(o);
    }

    @Override
    public void removeObserver(Observer o) {
        int i = observers.indexOf(o);
        if (i >= 0) {
            observers.remove(i);
        }
    }

    @Override
    public void notifyObserver() {
        for (Observer o : observers) {
            o.update(temperature, humidity, pressure);
        }
    }
}
```

```java
public interface Observer {
    void update(float temp, float humidity, float pressure);
}
```

```java
public class StatisticsDisplay implements Observer {

    public StatisticsDisplay(Subject weatherData) {
        weatherData.reisterObserver(this);
    }

    @Override
    public void update(float temp, float humidity, float pressure) {
        System.out.println("StatisticsDisplay.update: " + temp + " " + humidity + " " + pressure);
    }
}
```

```java
public class CurrentConditionsDisplay implements Observer {

    public CurrentConditionsDisplay(Subject weatherData) {
        weatherData.registerObserver(this);
    }

    @Override
    public void update(float temp, float humidity, float pressure) {
        System.out.println("CurrentConditionsDisplay.update: " + temp + " " + humidity + " " + pressure);
    }
}
```

```java
public class WeatherStation {
    public static void main(String[] args) {
        WeatherData weatherData = new WeatherData();
        CurrentConditionsDisplay currentConditionsDisplay = new CurrentConditionsDisplay(weatherData);
        StatisticsDisplay statisticsDisplay = new StatisticsDisplay(weatherData);

        weatherData.setMeasurements(0, 0, 0);
        weatherData.setMeasurements(1, 1, 1);
    }
}
```

```html
CurrentConditionsDisplay.update: 0.0 0.0 0.0
StatisticsDisplay.update: 0.0 0.0 0.0
CurrentConditionsDisplay.update: 1.0 1.0 1.0
StatisticsDisplay.update: 1.0 1.0 1.0
```

### JDK

- [java.util.Observer](http://docs.oracle.com/javase/8/docs/api/java/util/Observer.html)
- [java.util.EventListener](http://docs.oracle.com/javase/8/docs/api/java/util/EventListener.html)
- [javax.servlet.http.HttpSessionBindingListener](http://docs.oracle.com/javaee/7/api/javax/servlet/http/HttpSessionBindingListener.html)
- [RxJava](https://github.com/ReactiveX/RxJava)

## 8. State

### Intent

Allow an object to change its behavior when its internal state changes, making it appear as if the object changed its class.

### Class Diagram

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/79df886f-fdc3-4020-a07f-c991bb58e0d8.png"/> </div><br>

### Implementation

A gumball machine has multiple states. In each state, it behaves differently. State transitions change the machine's behavior as well.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/396be981-3f2c-4fd9-8101-dbf9c841504b.jpg" width="600"/> </div><br>

```java
public interface State {
    /**
     * Insert 25 cents
     */
    void insertQuarter();

    /**
     * Return 25 cents
     */
    void ejectQuarter();

    /**
     * Turn the crank
     */
    void turnCrank();

    /**
     * Dispense candy
     */
    void dispense();
}
```

```java
public class HasQuarterState implements State {

    private GumballMachine gumballMachine;

    public HasQuarterState(GumballMachine gumballMachine) {
        this.gumballMachine = gumballMachine;
    }

    @Override
    public void insertQuarter() {
        System.out.println("You can't insert another quarter");
    }

    @Override
    public void ejectQuarter() {
        System.out.println("Quarter returned");
        gumballMachine.setState(gumballMachine.getNoQuarterState());
    }

    @Override
    public void turnCrank() {
        System.out.println("You turned...");
        gumballMachine.setState(gumballMachine.getSoldState());
    }

    @Override
    public void dispense() {
        System.out.println("No gumball dispensed");
    }
}
```

```java
public class NoQuarterState implements State {

    GumballMachine gumballMachine;

    public NoQuarterState(GumballMachine gumballMachine) {
        this.gumballMachine = gumballMachine;
    }

    @Override
    public void insertQuarter() {
        System.out.println("You insert a quarter");
        gumballMachine.setState(gumballMachine.getHasQuarterState());
    }

    @Override
    public void ejectQuarter() {
        System.out.println("You haven't insert a quarter");
    }

    @Override
    public void turnCrank() {
        System.out.println("You turned, but there's no quarter");
    }

    @Override
    public void dispense() {
        System.out.println("You need to pay first");
    }
}
```

```java
public class SoldOutState implements State {

    GumballMachine gumballMachine;

    public SoldOutState(GumballMachine gumballMachine) {
        this.gumballMachine = gumballMachine;
    }

    @Override
    public void insertQuarter() {
        System.out.println("You can't insert a quarter, the machine is sold out");
    }

    @Override
    public void ejectQuarter() {
        System.out.println("You can't eject, you haven't inserted a quarter yet");
    }

    @Override
    public void turnCrank() {
        System.out.println("You turned, but there are no gumballs");
    }

    @Override
    public void dispense() {
        System.out.println("No gumball dispensed");
    }
}
```

```java
public class SoldState implements State {

    GumballMachine gumballMachine;

    public SoldState(GumballMachine gumballMachine) {
        this.gumballMachine = gumballMachine;
    }

    @Override
    public void insertQuarter() {
        System.out.println("Please wait, we're already giving you a gumball");
    }

    @Override
    public void ejectQuarter() {
        System.out.println("Sorry, you already turned the crank");
    }

    @Override
    public void turnCrank() {
        System.out.println("Turning twice doesn't get you another gumball!");
    }

    @Override
    public void dispense() {
        gumballMachine.releaseBall();
        if (gumballMachine.getCount() > 0) {
            gumballMachine.setState(gumballMachine.getNoQuarterState());
        } else {
            System.out.println("Oops, out of gumballs");
            gumballMachine.setState(gumballMachine.getSoldOutState());
        }
    }
}
```

```java
public class GumballMachine {

    private State soldOutState;
    private State noQuarterState;
    private State hasQuarterState;
    private State soldState;

    private State state;
    private int count = 0;

    public GumballMachine(int numberGumballs) {
        count = numberGumballs;
        soldOutState = new SoldOutState(this);
        noQuarterState = new NoQuarterState(this);
        hasQuarterState = new HasQuarterState(this);
        soldState = new SoldState(this);

        if (numberGumballs > 0) {
            state = noQuarterState;
        } else {
            state = soldOutState;
        }
    }

    public void insertQuarter() {
        state.insertQuarter();
    }

    public void ejectQuarter() {
        state.ejectQuarter();
    }

    public void turnCrank() {
        state.turnCrank();
        state.dispense();
    }

    public void setState(State state) {
        this.state = state;
    }

    public void releaseBall() {
        System.out.println("A gumball comes rolling out the slot...");
        if (count != 0) {
            count -= 1;
        }
    }

    public State getSoldOutState() {
        return soldOutState;
    }

    public State getNoQuarterState() {
        return noQuarterState;
    }

    public State getHasQuarterState() {
        return hasQuarterState;
    }

    public State getSoldState() {
        return soldState;
    }

    public int getCount() {
        return count;
    }
}
```

```java
public class Client {

    public static void main(String[] args) {
        GumballMachine gumballMachine = new GumballMachine(5);

        gumballMachine.insertQuarter();
        gumballMachine.turnCrank();

        gumballMachine.insertQuarter();
        gumballMachine.ejectQuarter();
        gumballMachine.turnCrank();

        gumballMachine.insertQuarter();
        gumballMachine.turnCrank();
        gumballMachine.insertQuarter();
        gumballMachine.turnCrank();
        gumballMachine.ejectQuarter();

        gumballMachine.insertQuarter();
        gumballMachine.insertQuarter();
        gumballMachine.turnCrank();
        gumballMachine.insertQuarter();
        gumballMachine.turnCrank();
        gumballMachine.insertQuarter();
        gumballMachine.turnCrank();
    }
}
```

```html
You insert a quarter
You turned...
A gumball comes rolling out the slot...
You insert a quarter
Quarter returned
You turned, but there's no quarter
You need to pay first
You insert a quarter
You turned...
A gumball comes rolling out the slot...
You insert a quarter
You turned...
A gumball comes rolling out the slot...
You haven't insert a quarter
You insert a quarter
You can't insert another quarter
You turned...
A gumball comes rolling out the slot...
You insert a quarter
You turned...
A gumball comes rolling out the slot...
Oops, out of gumballs
You can't insert a quarter, the machine is sold out
You turned, but there are no gumballs
No gumball dispensed
```

## 9. Strategy

### Intent

Define a family of algorithms, encapsulate each one, and make them interchangeable.

The Strategy pattern lets algorithms vary independently from the clients that use them.

### Class Diagram

- The Strategy interface defines a family of algorithms, all of which implement the `behavior()` method.
- Context is the class that uses this algorithm family. Its `doSomething()` method calls `behavior()`, and `setStrategy(Strategy)` can dynamically change the `strategy` object, which means it can dynamically change the algorithm used by Context.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/cd1be8c2-755a-4a66-ad92-2e30f8f47922.png"/> </div><br>

### Comparison with State Pattern

The State pattern has a class diagram similar to Strategy, and both can dynamically change object behavior. However, State changes the State object composed by Context through state transitions, while Strategy changes the Strategy object composed by Context through Context's own decision. A state transition means that, while Context is running, some condition changes and causes its State object to change.

State mainly solves state transition problems: when the state changes, the Context object changes its behavior. Strategy mainly encapsulates a group of interchangeable algorithms and dynamically replaces the algorithm used by Context as needed.

### Implementation

Design a duck that can dynamically change its call. Here, the algorithm family is the duck calling behavior.

```java
public interface QuackBehavior {
    void quack();
}
```

```java
public class Quack implements QuackBehavior {
    @Override
    public void quack() {
        System.out.println("quack!");
    }
}
```

```java
public class Squeak implements QuackBehavior{
    @Override
    public void quack() {
        System.out.println("squeak!");
    }
}
```

```java
public class Duck {

    private QuackBehavior quackBehavior;

    public void performQuack() {
        if (quackBehavior != null) {
            quackBehavior.quack();
        }
    }

    public void setQuackBehavior(QuackBehavior quackBehavior) {
        this.quackBehavior = quackBehavior;
    }
}
```

```java
public class Client {

    public static void main(String[] args) {
        Duck duck = new Duck();
        duck.setQuackBehavior(new Squeak());
        duck.performQuack();
        duck.setQuackBehavior(new Quack());
        duck.performQuack();
    }
}
```

```html
squeak!
quack!
```

### JDK

- java.util.Comparator#compare()
- javax.servlet.http.HttpServlet
- javax.servlet.Filter#doFilter()

## 10. Template Method

### Intent

Define the skeleton of an algorithm and defer some steps to subclasses.

With Template Method, subclasses can redefine certain steps of an algorithm without changing its structure.

### Class Diagram

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ac6a794b-68c0-486c-902f-8d988eee5766.png"/> </div><br>

### Implementation

Making coffee and tea follows similar processes, but some steps differ. Reuse the code for the shared steps.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/11236498-1417-46ce-a1b0-e10054256955.png"/> </div><br>

```java
public abstract class CaffeineBeverage {

    final void prepareRecipe() {
        boilWater();
        brew();
        pourInCup();
        addCondiments();
    }

    abstract void brew();

    abstract void addCondiments();

    void boilWater() {
        System.out.println("boilWater");
    }

    void pourInCup() {
        System.out.println("pourInCup");
    }
}
```

```java
public class Coffee extends CaffeineBeverage {
    @Override
    void brew() {
        System.out.println("Coffee.brew");
    }

    @Override
    void addCondiments() {
        System.out.println("Coffee.addCondiments");
    }
}
```

```java
public class Tea extends CaffeineBeverage {
    @Override
    void brew() {
        System.out.println("Tea.brew");
    }

    @Override
    void addCondiments() {
        System.out.println("Tea.addCondiments");
    }
}
```

```java
public class Client {
    public static void main(String[] args) {
        CaffeineBeverage caffeineBeverage = new Coffee();
        caffeineBeverage.prepareRecipe();
        System.out.println("-----------");
        caffeineBeverage = new Tea();
        caffeineBeverage.prepareRecipe();
    }
}
```

```html
boilWater
Coffee.brew
pourInCup
Coffee.addCondiments
-----------
boilWater
Tea.brew
pourInCup
Tea.addCondiments
```

### JDK

- java.util.Collections#sort()
- java.io.InputStream#skip()
- java.io.InputStream#read()
- java.util.AbstractList#indexOf()

## 11. Visitor

### Intent

Add new capabilities to an object structure, such as a composite structure.

### Class Diagram

- Visitor: declares a `visit` operation for each ConcreteElement.
- ConcreteVisitor: stores accumulated results during traversal.
- ObjectStructure: an object structure, which may be a composite structure or a collection.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/79c6f036-bde6-4393-85a3-ef36a0327bd2.png"/> </div><br>

### Implementation

```java
public interface Element {
    void accept(Visitor visitor);
}
```

```java
class CustomerGroup {

    private List<Customer> customers = new ArrayList<>();

    void accept(Visitor visitor) {
        for (Customer customer : customers) {
            customer.accept(visitor);
        }
    }

    void addCustomer(Customer customer) {
        customers.add(customer);
    }
}
```

```java
public class Customer implements Element {

    private String name;
    private List<Order> orders = new ArrayList<>();

    Customer(String name) {
        this.name = name;
    }

    String getName() {
        return name;
    }

    void addOrder(Order order) {
        orders.add(order);
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
        for (Order order : orders) {
            order.accept(visitor);
        }
    }
}
```

```java
public class Order implements Element {

    private String name;
    private List<Item> items = new ArrayList();

    Order(String name) {
        this.name = name;
    }

    Order(String name, String itemName) {
        this.name = name;
        this.addItem(new Item(itemName));
    }

    String getName() {
        return name;
    }

    void addItem(Item item) {
        items.add(item);
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);

        for (Item item : items) {
            item.accept(visitor);
        }
    }
}
```

```java
public class Item implements Element {

    private String name;

    Item(String name) {
        this.name = name;
    }

    String getName() {
        return name;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}
```

```java
public interface Visitor {
    void visit(Customer customer);

    void visit(Order order);

    void visit(Item item);
}
```

```java
public class GeneralReport implements Visitor {

    private int customersNo;
    private int ordersNo;
    private int itemsNo;

    public void visit(Customer customer) {
        System.out.println(customer.getName());
        customersNo++;
    }

    public void visit(Order order) {
        System.out.println(order.getName());
        ordersNo++;
    }

    public void visit(Item item) {
        System.out.println(item.getName());
        itemsNo++;
    }

    public void displayResults() {
        System.out.println("Number of customers: " + customersNo);
        System.out.println("Number of orders:    " + ordersNo);
        System.out.println("Number of items:     " + itemsNo);
    }
}
```

```java
public class Client {
    public static void main(String[] args) {
        Customer customer1 = new Customer("customer1");
        customer1.addOrder(new Order("order1", "item1"));
        customer1.addOrder(new Order("order2", "item1"));
        customer1.addOrder(new Order("order3", "item1"));

        Order order = new Order("order_a");
        order.addItem(new Item("item_a1"));
        order.addItem(new Item("item_a2"));
        order.addItem(new Item("item_a3"));
        Customer customer2 = new Customer("customer2");
        customer2.addOrder(order);

        CustomerGroup customers = new CustomerGroup();
        customers.addCustomer(customer1);
        customers.addCustomer(customer2);

        GeneralReport visitor = new GeneralReport();
        customers.accept(visitor);
        visitor.displayResults();
    }
}
```

```html
customer1
order1
item1
order2
item1
order3
item1
customer2
order_a
item_a1
item_a2
item_a3
Number of customers: 2
Number of orders:    4
Number of items:     6
```

### JDK

- javax.lang.model.element.Element and javax.lang.model.element.ElementVisitor
- javax.lang.model.type.TypeMirror and javax.lang.model.type.TypeVisitor

## 12. Null Object

### Intent

Use a null object that does nothing instead of NULL.

When a method returns NULL, callers must check whether the return value is NULL. This creates a lot of redundant checking code. If a caller forgets the check and directly uses the returned object, a null pointer exception may be thrown.

### Class Diagram

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/22870bbe-898f-4c17-a31a-d7c5ee5d1c10.png"/> </div><br>

### Implementation

```java
public abstract class AbstractOperation {
    abstract void request();
}
```

```java
public class RealOperation extends AbstractOperation {
    @Override
    void request() {
        System.out.println("do something");
    }
}
```

```java
public class NullOperation extends AbstractOperation{
    @Override
    void request() {
        // do nothing
    }
}
```

```java
public class Client {
    public static void main(String[] args) {
        AbstractOperation abstractOperation = func(-1);
        abstractOperation.request();
    }

    public static AbstractOperation func(int para) {
        if (para < 0) {
            return new NullOperation();
        }
        return new RealOperation();
    }
}
```

# 4. Structural Patterns

## 1. Adapter

### Intent

Convert the interface of a class into another interface that clients expect.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/3d5b828e-5c4d-48d8-a440-281e4a8e1c92.png"/> </div><br>

### Class Diagram

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ff5152fc-4ff3-44c4-95d6-1061002c364a.png"/> </div><br>

### Implementation

Duck and Turkey have different calls: Duck calls `quack()`, while Turkey calls `gobble()`.

Adapt Turkey's `gobble()` method to Duck's `quack()` method so a turkey can pretend to be a duck.

```java
public interface Duck {
    void quack();
}
```

```java
public interface Turkey {
    void gobble();
}
```

```java
public class WildTurkey implements Turkey {
    @Override
    public void gobble() {
        System.out.println("gobble!");
    }
}
```

```java
public class TurkeyAdapter implements Duck {
    Turkey turkey;

    public TurkeyAdapter(Turkey turkey) {
        this.turkey = turkey;
    }

    @Override
    public void quack() {
        turkey.gobble();
    }
}
```

```java
public class Client {
    public static void main(String[] args) {
        Turkey turkey = new WildTurkey();
        Duck duck = new TurkeyAdapter(turkey);
        duck.quack();
    }
}
```

### JDK

- [java.util.Arrays#asList()](http://docs.oracle.com/javase/8/docs/api/java/util/Arrays.html#asList%28T...%29)
- [java.util.Collections#list()](https://docs.oracle.com/javase/8/docs/api/java/util/Collections.html#list-java.util.Enumeration-)
- [java.util.Collections#enumeration()](https://docs.oracle.com/javase/8/docs/api/java/util/Collections.html#enumeration-java.util.Collection-)
- [javax.xml.bind.annotation.adapters.XMLAdapter](http://docs.oracle.com/javase/8/docs/api/javax/xml/bind/annotation/adapters/XmlAdapter.html#marshal-BoundType-)

## 2. Bridge

### Intent

Separate an abstraction from its implementation so the two can vary independently.

### Class Diagram

- Abstraction: defines the interface of the abstraction.
- Implementor: defines the interface for implementation classes.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2a1f8b0f-1dd7-4409-b177-a381c58066ad.png"/> </div><br>

### Implementation

`RemoteControl` represents the remote control and corresponds to the Abstraction.

`TV` represents the television and corresponds to the Implementor.

The Bridge pattern separates the remote control from the television, allowing either side to change independently.

```java
public abstract class TV {
    public abstract void on();

    public abstract void off();

    public abstract void tuneChannel();
}
```

```java
public class Sony extends TV {
    @Override
    public void on() {
        System.out.println("Sony.on()");
    }

    @Override
    public void off() {
        System.out.println("Sony.off()");
    }

    @Override
    public void tuneChannel() {
        System.out.println("Sony.tuneChannel()");
    }
}
```

```java
public class RCA extends TV {
    @Override
    public void on() {
        System.out.println("RCA.on()");
    }

    @Override
    public void off() {
        System.out.println("RCA.off()");
    }

    @Override
    public void tuneChannel() {
        System.out.println("RCA.tuneChannel()");
    }
}
```

```java
public abstract class RemoteControl {
    protected TV tv;

    public RemoteControl(TV tv) {
        this.tv = tv;
    }

    public abstract void on();

    public abstract void off();

    public abstract void tuneChannel();
}
```

```java
public class ConcreteRemoteControl1 extends RemoteControl {
    public ConcreteRemoteControl1(TV tv) {
        super(tv);
    }

    @Override
    public void on() {
        System.out.println("ConcreteRemoteControl1.on()");
        tv.on();
    }

    @Override
    public void off() {
        System.out.println("ConcreteRemoteControl1.off()");
        tv.off();
    }

    @Override
    public void tuneChannel() {
        System.out.println("ConcreteRemoteControl1.tuneChannel()");
        tv.tuneChannel();
    }
}
```

```java
public class ConcreteRemoteControl2 extends RemoteControl {
    public ConcreteRemoteControl2(TV tv) {
        super(tv);
    }

    @Override
    public void on() {
        System.out.println("ConcreteRemoteControl2.on()");
        tv.on();
    }

    @Override
    public void off() {
        System.out.println("ConcreteRemoteControl2.off()");
        tv.off();
    }

    @Override
    public void tuneChannel() {
        System.out.println("ConcreteRemoteControl2.tuneChannel()");
        tv.tuneChannel();
    }
}
```

```java
public class Client {
    public static void main(String[] args) {
        RemoteControl remoteControl1 = new ConcreteRemoteControl1(new RCA());
        remoteControl1.on();
        remoteControl1.off();
        remoteControl1.tuneChannel();
        RemoteControl remoteControl2 = new ConcreteRemoteControl2(new Sony());
         remoteControl2.on();
         remoteControl2.off();
         remoteControl2.tuneChannel();
    }
}
```

### JDK

- AWT (It provides an abstraction layer which maps onto the native OS the windowing support.)
- JDBC

## 3. Composite

### Intent

Compose objects into tree structures to represent whole-part hierarchies, allowing clients to treat individual objects and composite objects uniformly.

### Class Diagram

The Component class is the parent of both Composite and Leaf. A Composite can be viewed as an internal node in the tree.

A composite object owns one or more component objects, so its operations can be delegated to those components. Each component may itself be another composite object or a leaf object.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2b8bfd57-b4d1-4a75-bfb0-bcf1fba4014a.png"/> </div><br>

### Implementation

```java
public abstract class Component {
    protected String name;

    public Component(String name) {
        this.name = name;
    }

    public void print() {
        print(0);
    }

    abstract void print(int level);

    abstract public void add(Component component);

    abstract public void remove(Component component);
}
```

```java
public class Composite extends Component {

    private List<Component> child;

    public Composite(String name) {
        super(name);
        child = new ArrayList<>();
    }

    @Override
    void print(int level) {
        for (int i = 0; i < level; i++) {
            System.out.print("--");
        }
        System.out.println("Composite:" + name);
        for (Component component : child) {
            component.print(level + 1);
        }
    }

    @Override
    public void add(Component component) {
        child.add(component);
    }

    @Override
    public void remove(Component component) {
        child.remove(component);
    }
}
```

```java
public class Leaf extends Component {
    public Leaf(String name) {
        super(name);
    }

    @Override
    void print(int level) {
        for (int i = 0; i < level; i++) {
            System.out.print("--");
        }
        System.out.println("left:" + name);
    }

    @Override
    public void add(Component component) {
        throw new UnsupportedOperationException(); // Trade transparency for the Single Responsibility Principle, so callers do not need to distinguish leaf nodes from composite nodes
    }

    @Override
    public void remove(Component component) {
        throw new UnsupportedOperationException();
    }
}
```

```java
public class Client {
    public static void main(String[] args) {
        Composite root = new Composite("root");
        Component node1 = new Leaf("1");
        Component node2 = new Composite("2");
        Component node3 = new Leaf("3");
        root.add(node1);
        root.add(node2);
        root.add(node3);
        Component node21 = new Leaf("21");
        Component node22 = new Composite("22");
        node2.add(node21);
        node2.add(node22);
        Component node221 = new Leaf("221");
        node22.add(node221);
        root.print();
    }
}
```

```html
Composite:root
--left:1
--Composite:2
----left:21
----Composite:22
------left:221
--left:3
```

### JDK

- javax.swing.JComponent#add(Component)
- java.awt.Container#add(Component)
- java.util.Map#putAll(Map)
- java.util.List#addAll(Collection)
- java.util.Set#addAll(Collection)

## 4. Decorator

### Intent

Add responsibilities to an object dynamically.

### Class Diagram

Decorator and ConcreteComponent both inherit from Component. A ConcreteComponent implementation does not depend on other objects, while a Decorator composes a Component, allowing it to wrap either another Decorator or a ConcreteComponent. Decoration means wrapping the decorated object to extend its behavior dynamically. Part of a Decorator method belongs to the Decorator itself, and then it calls the decorated object's method to preserve the original behavior. Therefore, ConcreteComponent should sit at the bottom of the decoration hierarchy, because only its implementation does not depend on another object.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/6b833bc2-517a-4270-8a5e-0a5f6df8cd96.png"/> </div><br>

### Implementation

Design different kinds of beverages. A beverage can have condiments added, such as milk, and new condiments should be addable dynamically. Each condiment increases the beverage price, so the final beverage cost must be calculated.

The diagram below shows adding Mocha to a DarkRoast beverage, then adding Whip. DarkRoast is wrapped by Mocha, and Mocha is wrapped by Whip. They all inherit from the same parent class and expose a `cost()` method; the outer class's `cost()` method calls the inner class's `cost()` method.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/c9cfd600-bc91-4f3a-9f99-b42f88a5bb24.jpg" width="600"/> </div><br>

```java
public interface Beverage {
    double cost();
}
```

```java
public class DarkRoast implements Beverage {
    @Override
    public double cost() {
        return 1;
    }
}
```

```java
public class HouseBlend implements Beverage {
    @Override
    public double cost() {
        return 1;
    }
}
```

```java
public abstract class CondimentDecorator implements Beverage {
    protected Beverage beverage;
}
```

```java
public class Milk extends CondimentDecorator {

    public Milk(Beverage beverage) {
        this.beverage = beverage;
    }

    @Override
    public double cost() {
        return 1 + beverage.cost();
    }
}
```

```java
public class Mocha extends CondimentDecorator {

    public Mocha(Beverage beverage) {
        this.beverage = beverage;
    }

    @Override
    public double cost() {
        return 1 + beverage.cost();
    }
}
```

```java
public class Client {

    public static void main(String[] args) {
        Beverage beverage = new HouseBlend();
        beverage = new Mocha(beverage);
        beverage = new Milk(beverage);
        System.out.println(beverage.cost());
    }
}
```

```html
3.0
```

### Design Principles

Classes should be open for extension and closed for modification: adding new functionality should not require changing existing code. Beverages can dynamically receive new condiments without modifying the beverage code.

It is unrealistic to design every class around this principle. Apply it where change is most likely.

### JDK

- java.io.BufferedInputStream(InputStream)
- java.io.DataInputStream(InputStream)
- java.io.BufferedOutputStream(OutputStream)
- java.util.zip.ZipOutputStream(OutputStream)
- java.util.Collections#checked[List|Map|Set|SortedSet|SortedMap]()

## 5. Facade

### Intent

Provide a unified interface to a set of interfaces in a subsystem, making the subsystem easier to use.

### Class Diagram

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f9978fa6-9f49-4a0f-8540-02d269ac448f.png"/> </div><br>

### Implementation

Watching a movie requires operating many devices. Use the Facade pattern to implement a one-click movie mode.

```java
public class SubSystem {
    public void turnOnTV() {
        System.out.println("turnOnTV()");
    }

    public void setCD(String cd) {
        System.out.println("setCD( " + cd + " )");
    }

    public void startWatching(){
        System.out.println("startWatching()");
    }
}
```

```java
public class Facade {
    private SubSystem subSystem = new SubSystem();

    public void watchMovie() {
        subSystem.turnOnTV();
        subSystem.setCD("a movie");
        subSystem.startWatching();
    }
}
```

```java
public class Client {
    public static void main(String[] args) {
        Facade facade = new Facade();
        facade.watchMovie();
    }
}
```

### Design Principles

Principle of Least Knowledge: talk only to your close friends. In other words, a client object should interact with as few objects as possible.

## 6. Flyweight

### Intent

Use sharing to support large numbers of fine-grained objects whose internal state is partly identical.

### Class Diagram

- Flyweight: the shared object.
- IntrinsicState: internal state shared by flyweight objects.
- ExtrinsicState: external state that differs for each flyweight object.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/5f5c22d5-9c0e-49e1-b5b0-6cc7032724d4.png"/> </div><br>

### Implementation

```java
public interface Flyweight {
    void doOperation(String extrinsicState);
}
```

```java
public class ConcreteFlyweight implements Flyweight {

    private String intrinsicState;

    public ConcreteFlyweight(String intrinsicState) {
        this.intrinsicState = intrinsicState;
    }

    @Override
    public void doOperation(String extrinsicState) {
        System.out.println("Object address: " + System.identityHashCode(this));
        System.out.println("IntrinsicState: " + intrinsicState);
        System.out.println("ExtrinsicState: " + extrinsicState);
    }
}
```

```java
public class FlyweightFactory {

    private HashMap<String, Flyweight> flyweights = new HashMap<>();

    Flyweight getFlyweight(String intrinsicState) {
        if (!flyweights.containsKey(intrinsicState)) {
            Flyweight flyweight = new ConcreteFlyweight(intrinsicState);
            flyweights.put(intrinsicState, flyweight);
        }
        return flyweights.get(intrinsicState);
    }
}
```

```java
public class Client {

    public static void main(String[] args) {
        FlyweightFactory factory = new FlyweightFactory();
        Flyweight flyweight1 = factory.getFlyweight("aa");
        Flyweight flyweight2 = factory.getFlyweight("aa");
        flyweight1.doOperation("x");
        flyweight2.doOperation("y");
    }
}
```

```html
Object address: 1163157884
IntrinsicState: aa
ExtrinsicState: x
Object address: 1163157884
IntrinsicState: aa
ExtrinsicState: y
```

### JDK

Java uses caches to speed up access to large numbers of small objects.

- java.lang.Integer#valueOf(int)
- java.lang.Boolean#valueOf(boolean)
- java.lang.Byte#valueOf(byte)
- java.lang.Character#valueOf(char)

## 7. Proxy

### Intent

Control access to another object.

### Class Diagram

There are four common kinds of proxy:

- Remote Proxy: controls access to a remote object in another address space. It encodes requests and parameters, then sends the encoded request to the object in the other address space.
- Virtual Proxy: creates expensive objects on demand. It can cache additional information about the real object to defer access to it. For example, when a website loads a large image that cannot be completed immediately, a virtual proxy can cache the image size and generate a temporary placeholder for the original image.
- Protection Proxy: controls access to an object based on permissions. It checks whether the caller has the access rights required to perform a request.
- Smart Reference: replaces a simple pointer and performs extra operations when accessing an object, such as counting references, loading the object into memory on first reference, and checking whether the real object is locked before access so other objects cannot modify it.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/9b679ff5-94c6-48a7-b9b7-2ea868e828ed.png"/> </div><br>

### Implementation

The following is a Virtual Proxy implementation. It simulates delayed image loading by using temporary content with the same size as the image until the image finishes loading.

```java
public interface Image {
    void showImage();
}
```

```java
public class HighResolutionImage implements Image {

    private URL imageURL;
    private long startTime;
    private int height;
    private int width;

    public int getHeight() {
        return height;
    }

    public int getWidth() {
        return width;
    }

    public HighResolutionImage(URL imageURL) {
        this.imageURL = imageURL;
        this.startTime = System.currentTimeMillis();
        this.width = 600;
        this.height = 600;
    }

    public boolean isLoad() {
        // Simulate image loading, delayed by 3 seconds
        long endTime = System.currentTimeMillis();
        return endTime - startTime > 3000;
    }

    @Override
    public void showImage() {
        System.out.println("Real Image: " + imageURL);
    }
}
```

```java
public class ImageProxy implements Image {

    private HighResolutionImage highResolutionImage;

    public ImageProxy(HighResolutionImage highResolutionImage) {
        this.highResolutionImage = highResolutionImage;
    }

    @Override
    public void showImage() {
        while (!highResolutionImage.isLoad()) {
            try {
                System.out.println("Temp Image: " + highResolutionImage.getWidth() + " " + highResolutionImage.getHeight());
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        highResolutionImage.showImage();
    }
}
```

```java
public class ImageViewer {

    public static void main(String[] args) throws Exception {
        String image = "http://image.jpg";
        URL url = new URL(image);
        HighResolutionImage highResolutionImage = new HighResolutionImage(url);
        ImageProxy imageProxy = new ImageProxy(highResolutionImage);
        imageProxy.showImage();
    }
}
```

### JDK

- java.lang.reflect.Proxy
- RMI

# References

- Freeman. Head First Design Patterns [M]. China Electric Power Press, 2007.
- Gamma E. Design Patterns: Elements of Reusable Object-Oriented Software [M]. China Machine Press, 2007.
- Bloch J. Effective java[M]. Addison-Wesley Professional, 2017.
- [Design Patterns](http://www.oodesign.com/)
- [Design patterns implemented in Java](http://java-design-patterns.com/)
- [The breakdown of design patterns in JDK](http://www.programering.com/a/MTNxAzMwATY.html)
