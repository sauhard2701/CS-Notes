# 21. Reorder Array: Odd Before Even

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/ef1f53ef31ca408cada5093c8780f44b?tpId=13&tqId=11166&tab=answerKey&from=cyc_github)

## Problem Description

The relative order among odd numbers and among even numbers must remain unchanged, which is somewhat different from the book. For example, for [1,2,3,4,5], the result after adjustment should be [1,3,5,2,4], not a result like {5,1,3,4,2} where the relative order changes.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/d03a2efa-ef19-4c96-97e8-ff61df8061d3.png" width="200px"> </div><br>

## Solution

Method 1: Create a new array. Time complexity O(N), space complexity O(N).

```java
public int[] reOrderArray (int[] nums) {
    // Number of odd values
    int oddCnt = 0;
    for (int x : nums)
        if (!isEven(x))
            oddCnt++;
    int[] copy = nums.clone();
    int i = 0, j = oddCnt;
    for (int num : copy) {
        if (num % 2 == 1)
            nums[i++] = num;
        else
            nums[j++] = num;
    }
    return nums;
}

private boolean isEven(int x) {
    return x % 2 == 0;
}
```

Method 2: Use the bubble-sort idea, moving the current even number to the current rightmost position each time. Time complexity O(N<sup>2</sup>), space complexity O(1), trading time for space.

```java
public int[] reOrderArray(int[] nums) {
    int N = nums.length;
    for (int i = N - 1; i > 0; i--) {
        for (int j = 0; j < i; j++) {
            if (isEven(nums[j]) && !isEven(nums[j + 1])) {
                swap(nums, j, j + 1);
            }
        }
    }
    return nums;
}

private boolean isEven(int x) {
    return x % 2 == 0;
}

private void swap(int[] nums, int i, int j) {
    int t = nums[i];
    nums[i] = nums[j];
    nums[j] = t;
}
```
