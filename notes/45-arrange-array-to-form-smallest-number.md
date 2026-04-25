# 45. Arrange Array to Form Smallest Number

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/8fecd3f8ba334add803bf2a06af1b993?tpId=13&tqId=11185&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Given an array of positive integers, concatenate all numbers in the array to form a number, and print the smallest possible concatenated number. For example, given the array {3, 32, 321}, the smallest number these three numbers can form is 321323.

## Solution

This can be viewed as a sorting problem. When comparing two strings S1 and S2, compare S1+S2 with S2+S1. If S1+S2 \< S2+S1, S1 should come first; otherwise, S2 should come first.

```java
public String PrintMinNumber(int[] numbers) {
    if (numbers == null || numbers.length == 0)
        return "";
    int n = numbers.length;
    String[] nums = new String[n];
    for (int i = 0; i < n; i++)
        nums[i] = numbers[i] + "";
    Arrays.sort(nums, (s1, s2) -> (s1 + s2).compareTo(s2 + s1));
    String ret = "";
    for (String str : nums)
        ret += str;
    return ret;
}
```
