# 61. Straight in Playing Cards

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/762836f4d43d43ca9deb273b3de8e1f4?tpId=13&tqId=11198&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Given five cards, where jokers are wildcards and have face value 0, determine whether the five cards can form a straight.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/eaa506b6-0747-4bee-81f8-3cda795d8154.png" width="350px"> </div><br>


## Solution

```java
public boolean isContinuous(int[] nums) {

    if (nums.length < 5)
        return false;

    Arrays.sort(nums);

    // Count wildcards
    int cnt = 0;
    for (int num : nums)
        if (num == 0)
            cnt++;

    // Use wildcards to fill gaps in the straight
    for (int i = cnt; i < nums.length - 1; i++) {
        if (nums[i + 1] == nums[i])
            return false;
        cnt -= nums[i + 1] - nums[i] - 1;
    }

    return cnt >= 0;
}
```
