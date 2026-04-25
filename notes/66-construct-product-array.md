# 66. Construct Product Array

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/94a4d381a68b47b7a8bed86f2975db46?tpId=13&tqId=11204&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Given an array A[0, 1,..., n-1], construct an array B[0, 1,..., n-1], where B[i]=A[0]\*A[1]\*...\*A[i-1]\*A[i+1]\*...\*A[n-1]. Division must not be used.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/4240a69f-4d51-4d16-b797-2dfe110f30bd.png" width="250px"> </div><br>


## Solution

```java
public int[] multiply(int[] A) {
    int n = A.length;
    int[] B = new int[n];
    for (int i = 0, product = 1; i < n; product *= A[i], i++)       /* Accumulate products from left to right */
        B[i] = product;
    for (int i = n - 1, product = 1; i >= 0; product *= A[i], i--)  /* Accumulate products from right to left */
        B[i] *= product;
    return B;
}
```
