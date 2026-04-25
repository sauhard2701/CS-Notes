# 6. Print Linked List from Tail to Head

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/d0267f7f55b3412ba93bd35cfa8e8035?tpId=13&tqId=11156&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Print the value of each node in reverse order from tail to head.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f5792051-d9b2-4ca4-a234-a4a2de3d5a57.png" width="300px"> </div><br>

## Solution

### 1. Use Recursion

To print the linked list 1-\>2-\>3 in reverse order (3,2,1), first print the linked list 2-\>3 in reverse order (3,2), then print the first node 1. The linked list 2-\>3 can be viewed as a new linked list, and the same solving function can be used to print it in reverse order. Calling the solving function inside itself is recursion.

```java
public ArrayList<Integer> printListFromTailToHead(ListNode listNode) {
    ArrayList<Integer> ret = new ArrayList<>();
    if (listNode != null) {
        ret.addAll(printListFromTailToHead(listNode.next));
        ret.add(listNode.val);
    }
    return ret;
}
```

### 2. Use Head Insertion

Head insertion, as the name suggests, inserts nodes at the head. While traversing the original linked list, insert the current node at the head of the new linked list so that it becomes the first node.

Linked-list operations need to maintain successor relationships. For example, to insert node2 after node1, modify the successor relationships as follows:

```java
node3 = node1.next;
node2.next = node3;
node1.next = node2;
```

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/58c8e370-3bec-4c2b-bf17-c8d34345dd17.gif" width="220px"> </div><br>



To insert a node at the head, introduce an auxiliary node called the head node. This node stores no value and only makes insertion easier. Do not confuse the head node with the first node; the first node is the first actual node in the linked list that stores a value.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/0dae7e93-cfd1-4bd3-97e8-325b032b716f-1572687622947.gif" width="420px"> </div><br>

```java
public ArrayList<Integer> printListFromTailToHead(ListNode listNode) {
    // Build the reversed linked list with head insertion
    ListNode head = new ListNode(-1);
    while (listNode != null) {
        ListNode memo = listNode.next;
        listNode.next = head.next;
        head.next = listNode;
        listNode = memo;
    }
    // Build the ArrayList
    ArrayList<Integer> ret = new ArrayList<>();
    head = head.next;
    while (head != null) {
        ret.add(head.val);
        head = head.next;
    }
    return ret;
}
```

### 3. Use Stack

A stack is last-in, first-out. Put values into a stack in order while traversing the linked list, and the final pop order is the reverse order.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/9d1deeba-4ae1-41dc-98f4-47d85b9831bc.gif" width="340px"> </div><br>

```java
public ArrayList<Integer> printListFromTailToHead(ListNode listNode) {
    Stack<Integer> stack = new Stack<>();
    while (listNode != null) {
        stack.add(listNode.val);
        listNode = listNode.next;
    }
    ArrayList<Integer> ret = new ArrayList<>();
    while (!stack.isEmpty())
        ret.add(stack.pop());
    return ret;
}
```
