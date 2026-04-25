## Facade

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
