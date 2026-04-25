# 65. Add Without Arithmetic Operators

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/59ac416b4b944300b617d4f7f111b215?tpId=13&tqId=11201&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Write a function to compute the sum of two integers without using the arithmetic operators +, -, \*, or /.

## Solution

a ^ b represents the sum of two numbers without considering carries, and (a & b) \<\< 1 represents the carry.

The recursion terminates because (a & b) \<\< 1 adds one more 0 on the right. As recursion continues, the number of rightmost 0s in the carry gradually increases, and eventually the carry becomes 0, ending recursion.

```java
public int Add(int a, int b) {
    return b == 0 ? a : Add(a ^ b, (a & b) << 1);
}
```
