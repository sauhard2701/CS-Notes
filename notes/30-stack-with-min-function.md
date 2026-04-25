# 30. Stack with Min Function

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/4c776177d2c04c2494f2555c9fcc1e49?tpId=13&tqId=11173&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Implement a stack that contains a min() function, which returns the minimum value in the current stack.

## Solution

Use an extra minStack whose top element is the minimum value in the current stack. When performing push and pop operations on the stack, perform corresponding push and pop operations on minStack so that the top of minStack is always the minimum value in the current stack. During a push operation, compare the pushed element with the current minimum value and push the smaller value onto minStack.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20201104013936126.png" width="350px"> </div><br>

```java
private Stack<Integer> dataStack = new Stack<>();
private Stack<Integer> minStack = new Stack<>();

public void push(int node) {
    dataStack.push(node);
    minStack.push(minStack.isEmpty() ? node : Math.min(minStack.peek(), node));
}

public void pop() {
    dataStack.pop();
    minStack.pop();
}

public int top() {
    return dataStack.peek();
}

public int min() {
    return minStack.peek();
}
```
