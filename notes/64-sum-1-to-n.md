# 64. Sum 1+2+3+...+n

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/7a0da8fc483247ff8800059e12d7caf1?tpId=13&tqId=11200&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Multiplication, division, for, while, if, else, switch, case, and conditional expressions A ? B : C must not be used.

## Solution

The most important part of a recursive solution is specifying the return condition, but this problem cannot directly use an if statement to do that.

The logical AND operator && has short-circuit behavior: if the first condition is false, the second condition is not executed. Use this property by negating the recursive return condition and using it as the first condition of &&, then converting the recursive body into the second condition. When the recursive return condition is true, the recursive body is not executed, and recursion returns.

The recursive return condition in this problem is n \<= 0, whose negation is n \> 0. The recursive body is sum += Sum_Solution(n - 1), which becomes the condition (sum += Sum_Solution(n - 1)) \> 0.

```java
public int Sum_Solution(int n) {
    int sum = n;
    boolean b = (n > 0) && ((sum += Sum_Solution(n - 1)) > 0);
    return sum;
}
```
