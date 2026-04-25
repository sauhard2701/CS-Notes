## Null Object

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
