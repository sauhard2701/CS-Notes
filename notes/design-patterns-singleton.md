## Singleton

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

        // 单例测试
        Singleton firstSingleton = Singleton.INSTANCE;
        firstSingleton.setObjName("firstName");
        System.out.println(firstSingleton.getObjName());
        Singleton secondSingleton = Singleton.INSTANCE;
        secondSingleton.setObjName("secondName");
        System.out.println(firstSingleton.getObjName());
        System.out.println(secondSingleton.getObjName());

        // 反射获取实例测试
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
- [java.lang.System#getSecurityManager()](https://docs.oracle.com/javase/8/docs/api/java/lang/System.html#getSecurityManager--)

