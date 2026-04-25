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
