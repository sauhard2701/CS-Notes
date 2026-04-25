# 3. Duplicate Number in Array

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/6fe361ede7e54db1b84adc81d09d8524?tpId=13&tqId=11203&tab=answerKey&from=cyc_github)

## Problem Description

In an array of length n, all numbers are in the range 0 to n-1. Some numbers in the array are duplicated, but it is unknown how many numbers are duplicated or how many times each one appears. Find any duplicate number in the array.

```html
Input:
{2, 3, 1, 0, 2, 5}

Output:
2
```

## Solution

The required time complexity is O(N), and the space complexity is O(1). Therefore, sorting cannot be used, and no extra marker array can be used.

For problems where array elements are in the range [0, n-1], move the element with value i to index i. During this adjustment, if index i already contains a value i, then value i is duplicated.

Take (2, 3, 1, 0, 2, 5) as an example. When traversal reaches index 4, the value at that index is 2, but index 2 already contains value 2, so 2 is known to be duplicated:

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/643b6f18-f933-4ac5-aa7a-e304dbd7fe49.gif" width="350px"> </div><br>


```java
public int duplicate(int[] nums) {
    for (int i = 0; i < nums.length; i++) {
        while (nums[i] != i) {
            if (nums[i] == nums[nums[i]]) {
                return  nums[i];
            }
            swap(nums, i, nums[i]);
        }
        swap(nums, i, nums[i]);
    }
    return -1;
}

private void swap(int[] nums, int i, int j) {
    int t = nums[i];
    nums[i] = nums[j];
    nums[j] = t;
}

```

