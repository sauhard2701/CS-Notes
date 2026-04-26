# Object-Oriented Programming
<!-- GFM-TOC -->
* [Object-Oriented Programming](#object-oriented-programming)
    * [1. Three Core Features](#_1-three-core-features)
        * [Encapsulation](#encapsulation)
        * [Inheritance](#inheritance)
        * [Polymorphism](#polymorphism)
    * [2. Class Diagrams](#_2-class-diagrams)
        * [Generalization](#generalization)
        * [Realization](#realization)
        * [Aggregation](#aggregation)
        * [Composition](#composition)
        * [Association](#association)
        * [Dependency](#dependency)
    * [3. Design Principles](#_3-design-principles)
        * [S.O.L.I.D](#solid)
        * [Other Common Principles](#other-common-principles)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Three Core Features

### Encapsulation

Encapsulation uses abstract data types to wrap data together with operations based on that data, forming an indivisible independent entity. Data is protected inside the abstract data type, internal details are hidden as much as possible, and only a few external interfaces are exposed for interaction. Users do not need to care about an object's internal details, but can access the object through its public interface.

Advantages:

- Reduces coupling: modules can be developed, tested, optimized, used, understood, and modified independently.
- Reduces maintenance burden: modules are easier to understand, and debugging can avoid affecting other modules.
- Improves performance tuning: profiling can identify which modules affect system performance.
- Improves software reuse.
- Reduces the risk of building large systems: even if the whole system is unavailable, these independent modules may still be usable.

The following `Person` class encapsulates attributes such as `name`, `gender`, and `age`. External code can only use `get()` methods to access a `Person` object's `name` and `gender`, but cannot access `age`; however, `age` can be used by the `work()` method.

Notice that the `gender` attribute is stored as an `int`. Encapsulation hides this implementation detail from users. If the data type used by `gender` needs to change later, it can be changed without affecting client code.

```java
public class Person {

    private String name;
    private int gender;
    private int age;

    public String getName() {
        return name;
    }

    public String getGender() {
        return gender == 0 ? "man" : "woman";
    }

    public void work() {
        if (18 <= age && age <= 50) {
            System.out.println(name + " is working very hard!");
        } else {
            System.out.println(name + " can't work any more!");
        }
    }
}
```

### Inheritance

Inheritance implements an **IS-A** relationship. For example, Cat and Animal form an IS-A relationship, so Cat can inherit from Animal and obtain Animal's non-private attributes and methods.

Inheritance should follow the Liskov Substitution Principle: subclass objects must be able to replace all superclass objects.

Cat can be used as an Animal, meaning an Animal reference can refer to a Cat object. A superclass reference pointing to a subclass object is called **upcasting**.

```java
Animal animal = new Cat();
```

### Polymorphism

Polymorphism is divided into compile-time polymorphism and runtime polymorphism:

- Compile-time polymorphism mainly refers to method overloading.
- Runtime polymorphism means the concrete type referenced by an object reference in the program is determined only during runtime.

Runtime polymorphism has three requirements:

- Inheritance
- Overriding
- Upcasting

In the code below, the Instrument class has two subclasses: Wind and Percussion. Both override the superclass `play()` method, and the `main()` method uses the superclass Instrument to reference Wind and Percussion objects. When the Instrument reference calls `play()`, the `play()` method of the actual referenced object's class is executed, not the method from Instrument.

```java
public class Instrument {

    public void play() {
        System.out.println("Instument is playing...");
    }
}
```

```java
public class Wind extends Instrument {

    public void play() {
        System.out.println("Wind is playing...");
    }
}
```

```java
public class Percussion extends Instrument {

    public void play() {
        System.out.println("Percussion is playing...");
    }
}
```

```java
public class Music {

    public static void main(String[] args) {
        List<Instrument> instruments = new ArrayList<>();
        instruments.add(new Wind());
        instruments.add(new Percussion());
        for(Instrument instrument : instruments) {
            instrument.play();
        }
    }
}
```

```
Wind is playing...
Percussion is playing...
```

## 2. Class Diagrams

The following class diagrams are drawn with [PlantUML](https://www.planttext.com/). For more syntax and usage, see: http://plantuml.com/ .

### Generalization

Used to describe inheritance relationships. In Java, this uses the `extends` keyword.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/c0874e0a-dba3-467e-9c86-dd9313e0843e.jpg" width="180px"> </div><br>

```text
@startuml

title Generalization

class Vihical
class Car
class Trunck

Vihical <|-- Car
Vihical <|-- Trunck

@enduml
```

### Realization

Used to implement an interface. In Java, this uses the `implements` keyword.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/83d466bd-946b-4430-854a-cf7b0696d4c8.jpg" width="170px"> </div><br>

```text
@startuml

title Realization

interface MoveBehavior
class Fly
class Run

MoveBehavior <|.. Fly
MoveBehavior <|.. Run

@enduml
```

### Aggregation

Indicates that the whole is composed of parts, but the whole and parts are not strongly dependent. If the whole no longer exists, the parts can still exist.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a0ce43b7-afa8-4397-a96e-5c12a070f2ae.jpg" width="300px"> </div><br>

```text
@startuml

title Aggregation

class Computer
class Keyboard
class Mouse
class Screen

Computer o-- Keyboard
Computer o-- Mouse
Computer o-- Screen

@enduml
```

### Composition

Unlike aggregation, composition has a strong dependency between the whole and its parts. If the whole no longer exists, the parts no longer exist either. For example, a company and its departments form composition: if the company is gone, the departments are gone. But a company and its employees form aggregation, because employees still exist if the company is gone.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/6a88a398-c494-41f5-bb62-9f7fb811df7c.jpg" width="280px"> </div><br>

```text
@startuml

title Composition

class Company
class DepartmentA
class DepartmentB

Company *-- DepartmentA
Company *-- DepartmentB

@enduml
```

### Association

Indicates an association between objects of different classes. This is a static relationship, independent of runtime state, and can be determined from the beginning. It can also represent one-to-one, many-to-one, and many-to-many relationships. For example, students and schools form an association: one school can have many students, but one student belongs to only one school, so this is a many-to-one relationship that can be determined before runtime.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a3e4dc62-0da5-4d22-94f2-140078281812.jpg" width="200px"> </div><br>

```text
@startuml

title Association

class School
class Student

School "1" - "n" Student

@enduml
```

### Dependency

Unlike association, dependency takes effect during runtime. A dependency between class A and class B mainly appears in three forms:

- Class A is a local variable in a method of class B.
- Class A is a parameter of a method of class B.
- Class A sends a message to class B, causing class B to change.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/379444c9-f1d1-45cd-b7aa-b0c18427d388.jpg" width="330px"> </div><br>

```text
@startuml

title Dependency

class Vihicle {
    move(MoveBehavior)
}

interface MoveBehavior {
    move()
}

note "MoveBehavior.move()" as N

Vihicle ..> MoveBehavior

Vihicle .. N

@enduml
```

## 3. Design Principles

### S.O.L.I.D

| Abbreviation | Full Name | English Name |
| :---: | :---: | :---: |
| SRP | The Single Responsibility Principle    | Single Responsibility Principle |
| OCP | The Open Closed Principle              | Open Closed Principle |
| LSP | The Liskov Substitution Principle      | Liskov Substitution Principle |
| ISP | The Interface Segregation Principle    | Interface Segregation Principle |
| DIP | The Dependency Inversion Principle     | Dependency Inversion Principle |

#### 1. Single Responsibility Principle

> There should be only one reason to modify a class.

In other words, a class should be responsible for only one thing. When a class needs to do too many things, it should be decomposed.

If a class takes on too many responsibilities, those responsibilities become coupled. A change in one responsibility may weaken the class's ability to fulfill its other responsibilities.

#### 2. Open Closed Principle

> Classes should be open for extension and closed for modification.

Extension means adding new functionality, so this principle requires new functionality to be added without modifying existing code.

The most typical design pattern that follows the Open Closed Principle is the Decorator pattern. It can dynamically attach responsibilities to objects without modifying class code.

#### 3. Liskov Substitution Principle

> Subclass objects must be able to replace all superclass objects.

Inheritance is an IS-A relationship. A subclass must be usable as its superclass and should be more specific than its superclass.

If this principle is not satisfied, subclass behavior can differ greatly, increasing the complexity of the inheritance hierarchy.

#### 4. Interface Segregation Principle

> Clients should not be forced to depend on methods they do not use.

Therefore, multiple specialized interfaces are better than one general-purpose interface.

#### 5. Dependency Inversion Principle

> High-level modules should not depend on low-level modules; both should depend on abstractions.</br>Abstractions should not depend on details; details should depend on abstractions.

High-level modules contain important policy choices and business modules in an application. If high-level modules depend on low-level modules, changes in low-level modules directly affect high-level modules and force them to change as well.

Depending on abstractions means:

- No variable should hold a pointer or reference to a concrete class.
- No class should derive from a concrete class.
- No method should override an already implemented method from any base class.

### Other Common Principles

In addition to the classic principles above, the following design principles are also common in real development.

| Abbreviation | Full Name | English Name |
| :---: | :---: | :---: |
|LOD|    The Law of Demeter                   | Law of Demeter |
|CRP|    The Composite Reuse Principle        | Composite Reuse Principle |
|CCP|    The Common Closure Principle         | Common Closure Principle |
|SAP|    The Stable Abstractions Principle    | Stable Abstractions Principle |
|SDP|    The Stable Dependencies Principle    | Stable Dependencies Principle |

#### 1. Law of Demeter

The Law of Demeter is also called the Least Knowledge Principle, abbreviated LKP. It means an object should know as little as possible about other objects: do not talk to strangers.

#### 2. Composite Reuse Principle

Prefer object composition over inheritance for reuse.

#### 3. Common Closure Principle

Classes that change together should be grouped together, in the same package. If application code must be modified, we want all changes to happen in one package, rather than being scattered across many packages.

#### 4. Stable Abstractions Principle

The most stable packages should be the most abstract packages, and unstable packages should be concrete. In other words, a package's level of abstraction should be proportional to its stability.

#### 5. Stable Dependencies Principle

Dependencies between packages should point in the direction of stability. A package should depend on packages that are more stable than itself.

## References

- Thinking in Java
- Agile Software Development: Principles, Patterns, and Practices
- [SOLID Principles of Object-Oriented Design](http://www.cnblogs.com/shanyou/archive/2009/09/21/1570716.html)
- [Understanding UML Class Diagrams and Sequence Diagrams](http://design-patterns.readthedocs.io/zh_CN/latest/read_uml.html#generalization)
- [UML Series: Sequence Diagrams](http://www.cnblogs.com/wolf-sun/p/UML-Sequence-diagram.html)
- [Three Core Features of Object-Oriented Programming: Encapsulation, Inheritance, and Polymorphism](http://blog.csdn.net/jianyuerensheng/article/details/51602015)
