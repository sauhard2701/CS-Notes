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
