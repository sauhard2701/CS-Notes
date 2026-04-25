# 63. Maximum Stock Profit

## Problem Link

[Leetcode：121. Best Time to Buy and Sell Stock ](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/)

## Problem Description

One buy and one sell are allowed, and the buy must happen first. Find the maximum profit.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/42661013-750f-420b-b3c1-437e9a11fb65.png" width="220px"> </div><br>

## Solution

Use a greedy strategy. Suppose the sell operation happens at round i; the buy price should be the lowest price before i. Therefore, while traversing the array, record the current lowest buy price and try each position as the sell price, taking the maximum profit.

```java
public int maxProfit(int[] prices) {
    if (prices == null || prices.length == 0)
        return 0;
    int soFarMin = prices[0];
    int maxProfit = 0;
    for (int i = 1; i < prices.length; i++) {
        soFarMin = Math.min(soFarMin, prices[i]);
        maxProfit = Math.max(maxProfit, prices[i] - soFarMin);
    }
    return maxProfit;
}
```
