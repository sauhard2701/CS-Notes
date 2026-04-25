# 62. Last Remaining Number in Circle

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/f78a359491e64a50bce2d89cff857eb6?tpId=13&tqId=11199&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Let the children form a large circle. Randomly choose a number m, and let the child numbered 0 start counting. Each time the child who counts m-1 leaves the circle, sings a song, chooses any gift from the gift box, and does not return to the circle. Counting then continues from the next child, from 0 to m-1, and so on until only one child remains, who does not need to perform.

## Solution

This is the Josephus problem. The solution for a circle of length n can be viewed as the solution for length n-1 plus the count length m. Because it is a circle, take modulo n at the end.

```java
public int LastRemaining_Solution(int n, int m) {
    if (n == 0)     /* Handle special input */
        return -1;
    if (n == 1)     /* Recursive return condition */
        return 0;
    return (LastRemaining_Solution(n - 1, m) + m) % n;
}
```
