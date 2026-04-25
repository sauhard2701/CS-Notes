# 15. Number of 1 Bits

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/8ee967e43c2c4ec193b040ea7fbb10b8?tpId=13&tqId=11164&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Given an integer, output the number of 1 bits in its binary representation.

### Solution

The bit operation n&(n-1) sets the lowest 1 bit in n's binary representation to 0. Keep setting 1 bits to 0 until n becomes 0. Time complexity: O(M), where M is the number of 1 bits.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20201105004127554.png" width="500px"> </div><br>


```java
public int NumberOf1(int n) {
    int cnt = 0;
    while (n != 0) {
        cnt++;
        n &= (n - 1);
    }
    return cnt;
}
```
