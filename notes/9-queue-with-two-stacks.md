# 9. Queue with Two Stacks

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/54275ddae22f475981afa2244dd448c6?tpId=13&tqId=11158&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Implement a queue with two stacks, supporting the queue Push and Pop operations.

## Solution

The in stack handles push operations, and the out stack handles pop operations. After an element enters the in stack, its pop order is reversed. When an element needs to be popped, it first moves into the out stack, reversing the pop order again. Therefore, the final pop order is the same as the original enqueue order: the first element in is the first element out, which is queue order.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/3ea280b5-be7d-471b-ac76-ff020384357c.gif" width="450"/> </div><br>

```java
Stack<Integer> in = new Stack<Integer>();
Stack<Integer> out = new Stack<Integer>();

public void push(int node) {
    in.push(node);
}

public int pop() throws Exception {
    if (out.isEmpty())
        while (!in.isEmpty())
            out.push(in.pop());

    if (out.isEmpty())
        throw new Exception("queue is empty");

    return out.pop();
}
```
