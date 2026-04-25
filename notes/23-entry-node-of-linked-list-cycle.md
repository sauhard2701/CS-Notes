# 23. Entry Node of Linked List Cycle

[NowCoder](https://www.nowcoder.com/practice/253d2c59ec3e4bc68da16833f79a38e4?tpId=13&tqId=11208&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

A linked list contains a cycle. Find the entry node of the cycle. Extra space must not be used.

## Solution

Use two pointers: a fast pointer fast that moves two nodes at a time, and a slow pointer slow that moves one node at a time. Because a cycle exists, the two pointers must meet at some node in the cycle.

Assume the cycle entry node is y1, and the meeting node is z1.

Assume the fast pointer fast loops around the cycle N times. Its total path length is x+Ny+(N-1)z. The multiplier of z is (N-1) because the fast and slow pointers finally meet at node z1, so no further distance after z1 is needed.

The slow pointer slow has a total path length of x+y.

Because the fast pointer moves twice as fast as the slow pointer, x+Ny+(N-1)z = 2(x+y).

The goal is to find the cycle entry node y1, which can also be viewed as finding the length x. First, rewrite the equation above in terms of x: x=(N-2)y+(N-1)z.

The equation above does not show a strong pattern, but y+z is the total length of the cycle. Rewrite it again as x=(N-2)(y+z)+z. The left side is the distance from the start point x1 to the cycle entry node y1. The right side is the distance of (N-2) full loops around the cycle plus another distance z from the meeting point z1. Therefore, if two pointers start at x1 and z1 at the same time and each moves one step at a time, they will finally meet at the cycle entry node.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/bb7fc182-98c2-4860-8ea3-630e27a5f29f.png" width="500"/> </div><br>

```java
public ListNode EntryNodeOfLoop(ListNode pHead) {
    if (pHead == null || pHead.next == null)
        return null;
    ListNode slow = pHead, fast = pHead;
    do {
        fast = fast.next.next;
        slow = slow.next;
    } while (slow != fast);
    fast = pHead;
    while (slow != fast) {
        slow = slow.next;
        fast = fast.next;
    }
    return slow;
}
```
