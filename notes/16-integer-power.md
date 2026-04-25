# 16. Integer Power

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/1a834e5e3e1a4b7ba251417554e07c00?tpId=13&tqId=11165&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Given a floating-point number x of type double and an integer n of type int, compute x to the nth power.

## Solution

<!-- <div align="center"><img src="https://latex.codecogs.com/gif.latex?x^n=\left\{\begin{array}{rcl}x^{n/2}*x^{n/2}&&{n\%2=0}\\x*(x^{n/2}*x^{n/2})&&{n\%2=1}\end{array}\right." class="mathjax-pic"/></div> <br>  -->

The most intuitive solution is to multiply x by itself n times, x\*x\*x...\*x, giving a time complexity of O(N). Because multiplication is commutative, this operation can be split into two halves, (x\*x..\*x)\* (x\*x..\*x). The two halves are the same, so only one needs to be computed. Each newly split computation can continue to be split. This is divide and conquer: divide the original problem into smaller subproblems, then combine the subproblem results.

In this problem, the subproblem is x<sup>n/2</sup>. When combining subproblems, multiply the subproblem result by itself. If n is not even, splitting into two halves leaves one extra x, so one more x must be multiplied when combining the subproblems.



<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20201105012506187.png" width="400px"> </div><br>


Because (x\*x)<sup>n/2</sup> can be solved recursively, and n is halved in each recursive step, the time complexity of the whole algorithm is O(logN).

```java
public double Power(double x, int n) {
    boolean isNegative = false;
    if (n < 0) {
        n = -n;
        isNegative = true;
    }
    double res = pow(x, n);
    return isNegative ? 1 / res : res;
}

private double pow(double x, int n) {
    if (n == 0) return 1;
    if (n == 1) return x;
    double res = pow(x, n / 2);
    res = res * res;
    if (n % 2 != 0) res *= x;
    return res;
}
```

