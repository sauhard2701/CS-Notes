# 47. Maximum Value of Gifts

[NowCoder](https://www.nowcoder.com/questionTerminal/72a99e28381a407991f2c96d8cb238ab)

## Problem Description

Each cell of an m\*n board contains a gift with a certain value greater than 0. Starting from the top-left corner, collect gifts while moving one cell right or down each time until reaching the bottom-right corner. Given a board, find the maximum value of gifts that can be collected. For example, for the following board:

```
1    10   3    8
12   2    9    6
5    7    4    11
3    7    16   5
```

The maximum gift value is 1+12+5+7+7+16+5=53.

## Solution

This should be solved with dynamic programming rather than depth-first search. Depth-first search is too complex and is not the optimal solution.

```java
public int getMost(int[][] values) {
    if (values == null || values.length == 0 || values[0].length == 0)
        return 0;
    int n = values[0].length;
    int[] dp = new int[n];
    for (int[] value : values) {
        dp[0] += value[0];
        for (int i = 1; i < n; i++)
            dp[i] = Math.max(dp[i], dp[i - 1]) + value[i];
    }
    return dp[n - 1];
}
```
