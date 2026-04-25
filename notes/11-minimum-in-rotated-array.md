# 11. Minimum in Rotated Array

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/9f3231a991af4f55b95579b44b7a01ba?tpId=13&tqId=11159&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Moving several elements from the beginning of an array to the end is called rotating the array. Given a rotation of a non-decreasing sorted array, output the minimum element of the rotated array.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/0038204c-4b8a-42a5-921d-080f6674f989.png" width="210px"> </div><br>

## Solution

Splitting the rotated array in half produces a new rotated array that contains the minimum element, plus a non-decreasing sorted array. The new rotated array has half the length of the original array, reducing the problem size by half. This halving property gives the algorithm a time complexity of O(log<sub>2</sub>N).

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/424f34ab-a9fd-49a6-9969-d76b42251365.png" width="300px"> </div><br>

The key is determining which of the two halves is the rotated array and which is the non-decreasing array. It is easy to see that the first element of a non-decreasing array must be less than or equal to its last element.

Solve this by modifying binary search, where l represents low, m represents mid, and h represents high:

- When nums[m] \<= nums[h], the interval [m, h] is a non-decreasing array and [l, m] is the rotated array, so set h = m;
- Otherwise, the interval [m + 1, h] is the rotated array, so set l = m + 1.

```java
public int minNumberInRotateArray(int[] nums) {
    if (nums.length == 0)
        return 0;
    int l = 0, h = nums.length - 1;
    while (l < h) {
        int m = l + (h - l) / 2;
        if (nums[m] <= nums[h])
            h = m;
        else
            l = m + 1;
    }
    return nums[l];
}
```

If duplicate array elements are allowed, a special case can occur: nums[l] == nums[m] == nums[h]. In this case, it is impossible to determine which interval contains the answer, so switch to linear search. For example, in the array {1,1,1,0,1}, l, m, and h all point to 1, so there is no way to know which interval contains the minimum value 0.

```java
public int minNumberInRotateArray(int[] nums) {
    if (nums.length == 0)
        return 0;
    int l = 0, h = nums.length - 1;
    while (l < h) {
        int m = l + (h - l) / 2;
        if (nums[l] == nums[m] && nums[m] == nums[h])
            return minNumber(nums, l, h);
        else if (nums[m] <= nums[h])
            h = m;
        else
            l = m + 1;
    }
    return nums[l];
}

private int minNumber(int[] nums, int l, int h) {
    for (int i = l; i < h; i++)
        if (nums[i] > nums[i + 1])
            return nums[i + 1];
    return nums[l];
}
```
