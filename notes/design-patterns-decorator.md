## Decorator

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
