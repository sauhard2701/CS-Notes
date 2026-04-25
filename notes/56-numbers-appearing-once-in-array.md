# 56. Numbers Appearing Once in Array

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/389fc1c3d3be4479a154f63f495abff8?tpId=13&tqId=11193&tab=answerKey&from=cyc_github)

## Problem Description

In an integer array, all numbers except two appear twice. Find those two numbers.

## Solution

The XOR result of two equal elements is 0, and the XOR result of 0 with any number x is x.

XOR all elements in the array to get the XOR result of the two non-duplicated elements. For example, for the array [x,x,y,y,z,k], x^x^y^y^z^k = 0^y^y^z^k = y^y^z^k = 0^z^k = z^k.

Two unequal elements must differ in their bit-level representations, so the XOR result diff of these two elements must be nonzero. The bit operation diff & -diff obtains the rightmost 1 bit in diff, so set diff = diff & -diff. Use diff as the basis for distinguishing the two elements: one element must have an XOR result of 0 with diff, and the other must have a nonzero result. Suppose the two unequal elements are z and k. Traverse all elements in the array and check whether the XOR result of the element with diff is 0. If so, XOR the element with z and assign it to z; otherwise, XOR it with k and assign it to k. Equal elements in the array must be XORed with z together or with k together, not one with z and one with k. Since the XOR result of equal elements is 0, the final z and k are just the XOR results of the two unequal elements with 0, meaning the unequal elements themselves.

In the solution below, the first elements of the num1 and num2 arrays are used to hold the return values... This return-value style is not recommended in real development.

```java
public int[] FindNumsAppearOnce (int[] nums) {
    int[] res = new int[2];
    int diff = 0;
    for (int num : nums)
        diff ^= num;
    diff &= -diff;
    for (int num : nums) {
        if ((num & diff) == 0)
            res[0] ^= num;
        else
            res[1] ^= num;
    }
    if (res[0] > res[1]) {
        swap(res);
    }
    return res;
}

private void swap(int[] nums) {
    int t = nums[0];
    nums[0] = nums[1];
    nums[1] = t;
}
```
