# 52. First Common Node of Two Linked Lists

[NowCoder](https://www.nowcoder.com/practice/6ab1d9a29e88450685099d45c9e31e46?tpId=13&tqId=11189&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/5f1cb999-cb9a-4f6c-a0af-d90377295ab8.png" width="500"/> </div><br>

## Solution

Let the length of A be a + c and the length of B be b + c, where c is the length of the shared tail. Then a + c + b = b + c + a.

When the pointer traversing linked list A reaches the end, make it restart from the head of linked list B. Similarly, when the pointer traversing linked list B reaches the end, make it restart from the head of linked list A. This ensures that the pointers traversing A and B reach the intersection at the same time.

```java
public ListNode FindFirstCommonNode(ListNode pHead1, ListNode pHead2) {
    ListNode l1 = pHead1, l2 = pHead2;
    while (l1 != l2) {
        l1 = (l1 == null) ? pHead2 : l1.next;
        l2 = (l2 == null) ? pHead1 : l2.next;
    }
    return l1;
}
```
