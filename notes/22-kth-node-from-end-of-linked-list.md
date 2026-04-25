# 22. Kth Node from End of Linked List

[NowCoder](https://www.nowcoder.com/practice/886370fe658f41b498d40fb34ae76ff9?tpId=13&tqId=11167&tab=answerKey&from=cyc_github)

## Solution

Let the linked list length be N. Set two pointers, P1 and P2. First move P1 forward K nodes, leaving N - K nodes to move. Then move P1 and P2 at the same time. When P1 reaches the end of the linked list, P2 has moved to the N - Kth node, which is the Kth node from the end.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/6b504f1f-bf76-4aab-a146-a9c7a58c2029.png" width="500"/> </div><br>

```java
public ListNode FindKthToTail(ListNode head, int k) {
    if (head == null)
        return null;
    ListNode P1 = head;
    while (P1 != null && k-- > 0)
        P1 = P1.next;
    if (k > 0)
        return null;
    ListNode P2 = head;
    while (P1 != null) {
        P1 = P1.next;
        P2 = P2.next;
    }
    return P2;
}
```
