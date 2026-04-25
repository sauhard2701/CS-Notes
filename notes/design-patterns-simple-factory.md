## Simple Factory

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
