# 53. Count Occurrences in Sorted Array

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/70610bf967994b22bb1c26f9ae901fa2?tpId=13&tqId=11190&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

```html
Input:
nums = 1, 2, 3, 3, 3, 3, 4, 6
K = 3

Output:
4
```

## Solution

If the first and last positions of the given number k in the sorted array can be found, the number of occurrences can be known.

First consider how to find the first position of a number in a sorted array. A normal binary search is shown below; after finding the given element k, it immediately returns the current index.

```java
public int binarySearch(int[] nums, int K) {
    int l = 0, h = nums.length - 1;
    while (l <= h) {
        int m = l + (h - l) / 2;
        if (nums[m] == K) {
            return m;
        } else if (nums[m] > K) {
            h = m - 1;
        } else {
            l = m + 1;
        }
    }
    return -1;
}
```

However, when searching for the first position, after finding the element, the search should continue to the left. That is, when nums[m]\>=k, continue searching in the left interval, and the left interval should include position m.

```java
private int binarySearch(int[] nums, int K) {
    int l = 0, h = nums.length;
    while (l < h) {
        int m = l + (h - l) / 2;
        if (nums[m] >= K)
            h = m;
        else
            l = m + 1;
    }
    return l;
}
```

Finding the last position can be converted into finding the first position of k+1, then moving one position backward.

```java
public int GetNumberOfK(int[] nums, int K) {
    int first = binarySearch(nums, K);
    int last = binarySearch(nums, K + 1);
    return (first == nums.length || nums[first] != K) ? 0 : last - first;
}
```

Note that in the binarySearch method above for finding the first position, the initial value of h is nums.length, not nums.length - 1. Consider the following example:

```
nums = [2,2], k = 2
```

If h is nums.length - 1, then when finding the last position, binarySearch(nums, k + 1) - 1 = 1 - 1 = 0. This is because binarySearch can only return values in the range [0, nums.length - 1]. For binarySearch([2,2], 3), the desired return value is the insertion position of 3 in nums, which is one position after the last array index, namely nums.length. Therefore, h must be set to nums.length so that binarySearch returns a larger range and can cover the case where k is greater than the last element of nums.
