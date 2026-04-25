# LeetCode Solutions - Greedy
<!-- GFM-TOC -->
* [LeetCode Solutions - Greedy](#leetcode-solutions---greedy)
    * [1. Assign Cookies](#1-assign-cookies)
    * [2. Non-overlapping Intervals](#2-non-overlapping-intervals)
    * [3. Minimum Number of Arrows to Burst Balloons](#3-minimum-number-of-arrows-to-burst-balloons)
    * [4. Queue Reconstruction by Height](#4-queue-reconstruction-by-height)
    * [5. Best Time to Buy and Sell Stock](#5-best-time-to-buy-and-sell-stock)
    * [6. Best Time to Buy and Sell Stock II](#6-best-time-to-buy-and-sell-stock-ii)
    * [7. Can Place Flowers](#7-can-place-flowers)
    * [8. Is Subsequence](#8-is-subsequence)
    * [9. Non-decreasing Array](#9-non-decreasing-array)
    * [10. Maximum Subarray](#10-maximum-subarray)
    * [11. Partition Labels](#11-partition-labels)
<!-- GFM-TOC -->


Ensure that every operation is locally optimal and that the final result is globally optimal.

## 1. Assign Cookies

455\. Assign Cookies (Easy)

[Leetcode](https://leetcode.com/problems/assign-cookies/description/) / [LeetCode China](https://leetcode-cn.com/problems/assign-cookies/description/)

```html
Input: grid[1,3], size[1,2,4]
Output: 2
```

Problem description: each child has a greed factor `grid`, and each cookie has a size `size`. A child is satisfied only if the cookie size is greater than or equal to the child's greed factor. Find the maximum number of children that can be satisfied.

1. The cookie assigned to a child should be as small as possible while still satisfying the child, so larger cookies can be reserved for children with larger greed factors.
2. Since the child with the smallest greed factor is easiest to satisfy, satisfy that child first.

In the solution above, each cookie assignment chooses what appears to be the best current allocation, but this does not by itself guarantee that the local optimum leads to the global optimum. Assume a global optimum exists and prove by contradiction: suppose there is an optimal strategy better than the greedy strategy used here. If no such strategy exists, then the greedy strategy is optimal and the solution is globally optimal.

Proof: suppose that in one choice, the greedy strategy assigns the mth cookie to the child with the smallest current greed factor, where the mth cookie is the smallest cookie that can satisfy that child. Suppose an optimal strategy assigns the nth cookie to the same child, with m \< n. After this round of assignment, the greedy strategy must leave a cookie larger than the one left by the optimal strategy. Therefore, in later assignments, the greedy strategy can satisfy at least as many children. Thus no strategy better than the greedy strategy exists; the greedy strategy is optimal.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e69537d2-a016-4676-b169-9ea17eeb9037.gif" width="430px"> </div><br>

```java
public int findContentChildren(int[] grid, int[] size) {
    if (grid == null || size == null) return 0;
    Arrays.sort(grid);
    Arrays.sort(size);
    int gi = 0, si = 0;
    while (gi < grid.length && si < size.length) {
        if (grid[gi] <= size[si]) {
            gi++;
        }
        si++;
    }
    return gi;
}
```

## 2. Non-overlapping Intervals

435\. Non-overlapping Intervals (Medium)

[Leetcode](https://leetcode.com/problems/non-overlapping-intervals/description/) / [LeetCode China](https://leetcode-cn.com/problems/non-overlapping-intervals/description/)

```html
Input: [ [1,2], [1,2], [1,2] ]

Output: 2

Explanation: You need to remove two [1,2] to make the rest of intervals non-overlapping.
```

```html
Input: [ [1,2], [2,3] ]

Output: 0

Explanation: You don't need to remove any of the intervals since they're already non-overlapping.
```

Problem description: calculate how many intervals must be removed to make a set of intervals non-overlapping.

First calculate the maximum number of non-overlapping intervals that can be formed, then subtract that count from the total number of intervals.

In each choice, the interval end is most important. The smaller the selected interval's end, the more space remains for later intervals, so more intervals can be selected later.

Sort by interval end, and each time choose the interval with the smallest end that does not overlap the previous interval.

```java
public int eraseOverlapIntervals(int[][] intervals) {
    if (intervals.length == 0) {
        return 0;
    }
    Arrays.sort(intervals, Comparator.comparingInt(o -> o[1]));
    int cnt = 1;
    int end = intervals[0][1];
    for (int i = 1; i < intervals.length; i++) {
        if (intervals[i][0] < end) {
            continue;
        }
        end = intervals[i][1];
        cnt++;
    }
    return intervals.length - cnt;
}
```

Creating a `Comparator` with a lambda expression can make the algorithm run too slowly. If runtime matters, replace it with a normal `Comparator` statement:

```java
Arrays.sort(intervals, new Comparator<int[]>() {
     @Override
     public int compare(int[] o1, int[] o2) {
         return (o1[1] < o2[1]) ? -1 : ((o1[1] == o2[1]) ? 0 : 1);
     }
});
```

When implementing `compare()`, avoid subtraction such as `return o1[1] - o2[1];` to prevent overflow.

## 3. Minimum Number of Arrows to Burst Balloons

452\. Minimum Number of Arrows to Burst Balloons (Medium)

[Leetcode](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/description/) / [LeetCode China](https://leetcode-cn.com/problems/minimum-number-of-arrows-to-burst-balloons/description/)

```
Input:
[[10,16], [2,8], [1,6], [7,12]]

Output:
2
```

Problem description: balloons are placed on a horizontal number line and may overlap. Arrows are shot vertically toward the coordinate axis and burst all balloons in their path. Find the minimum number of arrows required to burst all balloons.

This also counts non-overlapping intervals, but unlike Non-overlapping Intervals, [1, 2] and [2, 3] are considered overlapping in this problem.

```java
public int findMinArrowShots(int[][] points) {
    if (points.length == 0) {
        return 0;
    }
    Arrays.sort(points, Comparator.comparingInt(o -> o[1]));
    int cnt = 1, end = points[0][1];
    for (int i = 1; i < points.length; i++) {
        if (points[i][0] <= end) {
            continue;
        }
        cnt++;
        end = points[i][1];
    }
    return cnt;
}
```

## 4. Queue Reconstruction by Height

406\. Queue Reconstruction by Height(Medium)

[Leetcode](https://leetcode.com/problems/queue-reconstruction-by-height/description/) / [LeetCode China](https://leetcode-cn.com/problems/queue-reconstruction-by-height/description/)

```html
Input:
[[7,0], [4,4], [7,1], [5,0], [6,1], [5,2]]

Output:
[[5,0], [7,0], [5,2], [6,1], [4,4], [7,1]]
```

Problem description: a student is described by two components `(h, k)`. `h` is height, and `k` means there are `k` students in front whose height is greater than or equal to this student's height.

To ensure insertions do not affect later operations, taller students should be inserted first. Otherwise, the kth position where a shorter student was correctly inserted may become the k+1 position.

Sort height `h` in descending order and count `k` in ascending order, then insert each student at position `k` in the queue.

```java
public int[][] reconstructQueue(int[][] people) {
    if (people == null || people.length == 0 || people[0].length == 0) {
        return new int[0][0];
    }
    Arrays.sort(people, (a, b) -> (a[0] == b[0] ? a[1] - b[1] : b[0] - a[0]));
    List<int[]> queue = new ArrayList<>();
    for (int[] p : people) {
        queue.add(p[1], p);
    }
    return queue.toArray(new int[queue.size()][]);
}
```

## 5. Best Time to Buy and Sell Stock

121\. Best Time to Buy and Sell Stock (Easy)

[Leetcode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/) / [LeetCode China](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock/description/)

Problem description: one stock transaction consists of one buy and one sell. Only one transaction is allowed; find the maximum profit.

Record the minimum price seen so far, use it as the buy price, and use the current price as the sell price to check whether the current profit is the maximum profit.

```java
public int maxProfit(int[] prices) {
    int n = prices.length;
    if (n == 0) return 0;
    int soFarMin = prices[0];
    int max = 0;
    for (int i = 1; i < n; i++) {
        if (soFarMin > prices[i]) soFarMin = prices[i];
        else max = Math.max(max, prices[i] - soFarMin);
    }
    return max;
}
```


## 6. Best Time to Buy and Sell Stock II

122\. Best Time to Buy and Sell Stock II (Easy)

[Leetcode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/description/) / [LeetCode China](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-ii/description/)

Problem description: multiple transactions are allowed, but transactions cannot overlap.

For [a, b, c, d], if a \<= b \<= c \<= d, the maximum profit is d - a. Since d - a = (d - c) + (c - b) + (b - a), whenever `prices[i] - prices[i-1] \> 0`, add `prices[i] - prices[i-1]` to the profit.

```java
public int maxProfit(int[] prices) {
    int profit = 0;
    for (int i = 1; i < prices.length; i++) {
        if (prices[i] > prices[i - 1]) {
            profit += (prices[i] - prices[i - 1]);
        }
    }
    return profit;
}
```


## 7. Can Place Flowers

605\. Can Place Flowers (Easy)

[Leetcode](https://leetcode.com/problems/can-place-flowers/description/) / [LeetCode China](https://leetcode-cn.com/problems/can-place-flowers/description/)

```html
Input: flowerbed = [1,0,0,0,1], n = 1
Output: True
```

Problem description: in the `flowerbed` array, 1 means a flower has already been planted. Flowers need at least one empty unit between them. Determine whether `n` flowers can be planted.

```java
public boolean canPlaceFlowers(int[] flowerbed, int n) {
    int len = flowerbed.length;
    int cnt = 0;
    for (int i = 0; i < len && cnt < n; i++) {
        if (flowerbed[i] == 1) {
            continue;
        }
        int pre = i == 0 ? 0 : flowerbed[i - 1];
        int next = i == len - 1 ? 0 : flowerbed[i + 1];
        if (pre == 0 && next == 0) {
            cnt++;
            flowerbed[i] = 1;
        }
    }
    return cnt >= n;
}
```

## 8. Is Subsequence

392\. Is Subsequence (Medium)

[Leetcode](https://leetcode.com/problems/is-subsequence/description/) / [LeetCode China](https://leetcode-cn.com/problems/is-subsequence/description/)

```html
s = "abc", t = "ahbgdc"
Return true.
```

```java
public boolean isSubsequence(String s, String t) {
    int index = -1;
    for (char c : s.toCharArray()) {
        index = t.indexOf(c, index + 1);
        if (index == -1) {
            return false;
        }
    }
    return true;
}
```

## 9. Non-decreasing Array

665\. Non-decreasing Array (Easy)

[Leetcode](https://leetcode.com/problems/non-decreasing-array/description/) / [LeetCode China](https://leetcode-cn.com/problems/non-decreasing-array/description/)

```html
Input: [4,2,3]
Output: True
Explanation: You could modify the first 4 to 1 to get a non-decreasing array.
```

Problem description: determine whether an array can become non-decreasing by modifying at most one number.

When `nums[i] \< nums[i - 1]` appears, decide which number should be modified so the array before `i` becomes non-decreasing and **does not affect later operations**. Prefer setting `nums[i - 1] = nums[i]`, because if `nums[i] = nums[i - 1]` is used, `nums[i]` becomes larger and may become greater than `nums[i + 1]`, affecting later operations. One special case is `nums[i] \< nums[i - 2]`; then changing `nums[i - 1] = nums[i]` cannot make the array non-decreasing, so only `nums[i] = nums[i - 1]` works.

```java
public boolean checkPossibility(int[] nums) {
    int cnt = 0;
    for (int i = 1; i < nums.length && cnt < 2; i++) {
        if (nums[i] >= nums[i - 1]) {
            continue;
        }
        cnt++;
        if (i - 2 >= 0 && nums[i - 2] > nums[i]) {
            nums[i] = nums[i - 1];
        } else {
            nums[i - 1] = nums[i];
        }
    }
    return cnt <= 1;
}
```



## 10. Maximum Subarray

53\. Maximum Subarray (Easy)

[Leetcode](https://leetcode.com/problems/maximum-subarray/description/) / [LeetCode China](https://leetcode-cn.com/problems/maximum-subarray/description/)

```html
For example, given the array [-2,1,-3,4,-1,2,1,-5,4],
the contiguous subarray [4,-1,2,1] has the largest sum = 6.
```

```java
public int maxSubArray(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }
    int preSum = nums[0];
    int maxSum = preSum;
    for (int i = 1; i < nums.length; i++) {
        preSum = preSum > 0 ? preSum + nums[i] : nums[i];
        maxSum = Math.max(maxSum, preSum);
    }
    return maxSum;
}
```

## 11. Partition Labels

763\. Partition Labels (Medium)

[Leetcode](https://leetcode.com/problems/partition-labels/description/) / [LeetCode China](https://leetcode-cn.com/problems/partition-labels/description/)

```html
Input: S = "ababcbacadefegdehijhklij"
Output: [9,7,8]
Explanation:
The partition is "ababcbaca", "defegde", "hijhklij".
This is a partition so that each letter appears in at most one part.
A partition like "ababcbacadefegde", "hijhklij" is incorrect, because it splits S into less parts.
```

```java
public List<Integer> partitionLabels(String S) {
    int[] lastIndexsOfChar = new int[26];
    for (int i = 0; i < S.length(); i++) {
        lastIndexsOfChar[char2Index(S.charAt(i))] = i;
    }
    List<Integer> partitions = new ArrayList<>();
    int firstIndex = 0;
    while (firstIndex < S.length()) {
        int lastIndex = firstIndex;
        for (int i = firstIndex; i < S.length() && i <= lastIndex; i++) {
            int index = lastIndexsOfChar[char2Index(S.charAt(i))];
            if (index > lastIndex) {
                lastIndex = index;
            }
        }
        partitions.add(lastIndex - firstIndex + 1);
        firstIndex = lastIndex + 1;
    }
    return partitions;
}

private int char2Index(char c) {
    return c - 'a';
}
```
