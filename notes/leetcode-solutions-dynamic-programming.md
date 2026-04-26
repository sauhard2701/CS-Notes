# LeetCode Solutions - Dynamic Programming
<!-- GFM-TOC -->
* [LeetCode Solutions - Dynamic Programming](#leetcode-solutions---dynamic-programming)
    * [Fibonacci Sequence](#fibonacci-sequence)
        * [1. Climbing Stairs](#_1-climbing-stairs)
        * [2. House Robber](#_2-house-robber)
        * [3. House Robber II](#_3-house-robber-ii)
        * [4. Derangements](#_4-derangements)
        * [5. Cow Reproduction](#_5-cow-reproduction)
    * [Matrix Paths](#matrix-paths)
        * [1. Minimum Path Sum](#_1-minimum-path-sum)
        * [2. Unique Paths](#_2-unique-paths)
    * [Array Ranges](#array-ranges)
        * [1. Range Sum Query - Immutable](#_1-range-sum-query---immutable)
        * [2. Arithmetic Slices](#_2-arithmetic-slices)
    * [Integer Partition](#integer-partition)
        * [1. Integer Break](#_1-integer-break)
        * [2. Perfect Squares](#_2-perfect-squares)
        * [3. Decode Ways](#_3-decode-ways)
    * [Longest Increasing Subsequence](#longest-increasing-subsequence)
        * [1. Longest Increasing Subsequence](#_1-longest-increasing-subsequence)
        * [2. Maximum Length of Pair Chain](#_2-maximum-length-of-pair-chain)
        * [3. Wiggle Subsequence](#_3-wiggle-subsequence)
    * [Longest Common Subsequence](#longest-common-subsequence)
        * [1. Longest Common Subsequence](#_1-longest-common-subsequence)
    * [0-1 Knapsack](#_0-1-knapsack)
        * [1. Partition Equal Subset Sum](#_1-partition-equal-subset-sum)
        * [2. Target Sum](#_2-target-sum)
        * [3. Ones and Zeroes](#_3-ones-and-zeroes)
        * [4. Coin Change](#_4-coin-change)
        * [5. Coin Change 2](#_5-coin-change-2)
        * [6. Word Break](#_6-word-break)
        * [7. Combination Sum IV](#_7-combination-sum-iv)
    * [Stock Trading](#stock-trading)
        * [1. Best Time to Buy and Sell Stock with Cooldown](#_1-best-time-to-buy-and-sell-stock-with-cooldown)
        * [2. Best Time to Buy and Sell Stock with Transaction Fee](#_2-best-time-to-buy-and-sell-stock-with-transaction-fee)
        * [3. Best Time to Buy and Sell Stock III](#_3-best-time-to-buy-and-sell-stock-iii)
        * [4. Best Time to Buy and Sell Stock IV](#_4-best-time-to-buy-and-sell-stock-iv)
    * [String Editing](#string-editing)
        * [1. Delete Operation for Two Strings](#_1-delete-operation-for-two-strings)
        * [2. Edit Distance](#_2-edit-distance)
        * [3. 2 Keys Keyboard](#_3-2-keys-keyboard)
<!-- GFM-TOC -->


Both recursion and dynamic programming split the original problem into multiple subproblems and solve them. The essential difference is that dynamic programming stores subproblem results to avoid repeated computation.

## Fibonacci Sequence

### 1. Climbing Stairs

70\. Climbing Stairs (Easy)

[Leetcode](https://leetcode.com/problems/climbing-stairs/description/) / [LeetCode CN](https://leetcode-cn.com/problems/climbing-stairs/description/)

Problem description: There are N stairs. Each time you can climb one or two stairs. Find the number of ways to climb to the top.

Define an array dp to store the number of ways to climb stairs. For easier discussion, array indexing starts from 1. dp[i] represents the number of ways to reach the i-th stair.

The i-th stair can be reached from the (i-1)-th or (i-2)-th stair by taking one more step. Therefore, the number of ways to reach the i-th stair is the sum of the numbers of ways to reach the (i-1)-th and (i-2)-th stairs.

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[i]=dp[i-1]+dp[i-2]" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/14fe1e71-8518-458f-a220-116003061a83.png" width="200px"> </div><br>

Since dp[i] is related only to dp[i - 1] and dp[i - 2], two variables can store dp[i - 1] and dp[i - 2], optimizing the original O(N) space complexity to O(1).

```java
public int climbStairs(int n) {
    if (n <= 2) {
        return n;
    }
    int pre2 = 1, pre1 = 2;
    for (int i = 2; i < n; i++) {
        int cur = pre1 + pre2;
        pre2 = pre1;
        pre1 = cur;
    }
    return pre1;
}
```

### 2. House Robber

198\. House Robber (Easy)

[Leetcode](https://leetcode.com/problems/house-robber/description/) / [LeetCode CN](https://leetcode-cn.com/problems/house-robber/description/)

Problem description: Rob a row of houses, but adjacent houses cannot both be robbed. Find the maximum amount that can be robbed.

Define a dp array to store the maximum robbery amount, where dp[i] represents the maximum amount when considering houses up to the i-th house.

Because adjacent houses cannot both be robbed, if the (i-1)-th house is robbed, the i-th house cannot be robbed, so:

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[i]=max(dp[i-2]+nums[i],dp[i-1])" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2de794ca-aa7b-48f3-a556-a0e2708cb976.jpg" width="350px"> </div><br>

```java
public int rob(int[] nums) {
    int pre2 = 0, pre1 = 0;
    for (int i = 0; i < nums.length; i++) {
        int cur = Math.max(pre2 + nums[i], pre1);
        pre2 = pre1;
        pre1 = cur;
    }
    return pre1;
}
```

### 3. House Robber II

213\. House Robber II (Medium)

[Leetcode](https://leetcode.com/problems/house-robber-ii/description/) / [LeetCode CN](https://leetcode-cn.com/problems/house-robber-ii/description/)

```java
public int rob(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }
    int n = nums.length;
    if (n == 1) {
        return nums[0];
    }
    return Math.max(rob(nums, 0, n - 2), rob(nums, 1, n - 1));
}

private int rob(int[] nums, int first, int last) {
    int pre2 = 0, pre1 = 0;
    for (int i = first; i <= last; i++) {
        int cur = Math.max(pre1, pre2 + nums[i]);
        pre2 = pre1;
        pre1 = cur;
    }
    return pre1;
}
```

### 4. Derangements

Problem description: There are N letters and N envelopes. They are shuffled. Find the number of ways to place every letter in the wrong envelope.

Define an array dp to store the number of derangements, where dp[i] represents the number of wrong placements for the first i letters and envelopes. Suppose the i-th letter is placed in the j-th envelope, and the j-th letter is placed in the k-th envelope. Based on whether i equals k, there are two cases:

- i==k: after swapping the letters i and j, those two letters and envelopes are in the correct positions, while the remaining i-2 letters have dp[i-2] wrong-placement ways. Since j has i-1 possible values, there are (i-1)\*dp[i-2] wrong-placement ways.
- i != k: after swapping the letters i and j, the i-th letter and envelope are in the correct position, while the remaining i-1 letters have dp[i-1] wrong-placement ways. Since j has i-1 possible values, there are (i-1)\*dp[i-1] wrong-placement ways.

Therefore, the number of derangements is:

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[i]=(i-1)*dp[i-2]+(i-1)*dp[i-1]" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/da1f96b9-fd4d-44ca-8925-fb14c5733388.png" width="350px"> </div><br>

### 5. Cow Reproduction

[Programmer Code Interview Guide, p. 181](#)

Problem description: Suppose every mature cow on a farm gives birth to one calf each year and never dies. In the first year there is one calf. Starting in the second year, mature cows begin giving birth. Each calf matures after three years and can then give birth. Given integer N, find the number of cows after N years.

The number of mature cows in year i is:

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[i]=dp[i-1]+dp[i-3]" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/879814ee-48b5-4bcb-86f5-dcc400cb81ad.png" width="250px"> </div><br>

## Matrix Paths

### 1. Minimum Path Sum

64\. Minimum Path Sum (Medium)

[Leetcode](https://leetcode.com/problems/minimum-path-sum/description/) / [LeetCode CN](https://leetcode-cn.com/problems/minimum-path-sum/description/)

```html
[[1,3,1],
 [1,5,1],
 [4,2,1]]
Given the above grid map, return 7. Because the path 1→3→1→1→1 minimizes the sum.
```

Problem description: Find the minimum path sum from the top-left corner to the bottom-right corner of a matrix. Each move can only go right or down.

```java
public int minPathSum(int[][] grid) {
    if (grid.length == 0 || grid[0].length == 0) {
        return 0;
    }
    int m = grid.length, n = grid[0].length;
    int[] dp = new int[n];
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (j == 0) {
                dp[j] = dp[j];        // can only reach this position from above
            } else if (i == 0) {
                dp[j] = dp[j - 1];    // can only reach this position from the left
            } else {
                dp[j] = Math.min(dp[j - 1], dp[j]);
            }
            dp[j] += grid[i][j];
        }
    }
    return dp[n - 1];
}
```

### 2. Unique Paths

62\. Unique Paths (Medium)

[Leetcode](https://leetcode.com/problems/unique-paths/description/) / [LeetCode CN](https://leetcode-cn.com/problems/unique-paths/description/)

Problem description: Count the number of paths from the top-left corner to the bottom-right corner of a matrix. Each move can only go right or down.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/dc82f0f3-c1d4-4ac8-90ac-d5b32a9bd75a.jpg" width=""> </div><br>

```java
public int uniquePaths(int m, int n) {
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[j] = dp[j] + dp[j - 1];
        }
    }
    return dp[n - 1];
}
```

It can also be solved directly with a mathematical formula. This is a combinatorics problem. The robot moves S=m+n-2 times in total, and moves down D=m-1 times. The problem can be viewed as choosing D positions from S moves, so the solution is C(S, D).

```java
public int uniquePaths(int m, int n) {
    int S = m + n - 2;  // total number of moves
    int D = m - 1;      // number of downward moves
    long ret = 1;
    for (int i = 1; i <= D; i++) {
        ret = ret * (S - D + i) / i;
    }
    return (int) ret;
}
```

## Array Ranges

### 1. Range Sum Query - Immutable

303\. Range Sum Query - Immutable (Easy)

[Leetcode](https://leetcode.com/problems/range-sum-query-immutable/description/) / [LeetCode CN](https://leetcode-cn.com/problems/range-sum-query-immutable/description/)

```html
Given nums = [-2, 0, 3, -5, 2, -1]

sumRange(0, 2) -> 1
sumRange(2, 5) -> -1
sumRange(0, 5) -> -3
```

The sum of interval i \~ j can be converted to sum[j + 1] - sum[i], where sum[i] is the sum of elements from 0 through i - 1.

```java
class NumArray {

    private int[] sums;

    public NumArray(int[] nums) {
        sums = new int[nums.length + 1];
        for (int i = 1; i <= nums.length; i++) {
            sums[i] = sums[i - 1] + nums[i - 1];
        }
    }

    public int sumRange(int i, int j) {
        return sums[j + 1] - sums[i];
    }
}
```

### 2. Arithmetic Slices

413\. Arithmetic Slices (Medium)

[Leetcode](https://leetcode.com/problems/arithmetic-slices/description/) / [LeetCode CN](https://leetcode-cn.com/problems/arithmetic-slices/description/)

```html
A = [0, 1, 2, 3, 4]

return: 6, for 3 arithmetic slices in A:

[0, 1, 2],
[1, 2, 3],
[0, 1, 2, 3],
[0, 1, 2, 3, 4],
[ 1, 2, 3, 4],
[2, 3, 4]
```

dp[i] represents the number of arithmetic increasing subarrays ending at A[i].

When A[i] - A[i-1] == A[i-1] - A[i-2], [A[i-2], A[i-1], A[i]] forms an arithmetic increasing subarray. Also, adding A[i] to the end of any increasing subarray that ends at A[i-1] forms a new increasing subarray.

```html
dp[2] = 1
    [0, 1, 2]
dp[3] = dp[2] + 1 = 2
    [0, 1, 2, 3], // add 3 after [0, 1, 2]
    [1, 2, 3]     // new increasing subarray
dp[4] = dp[3] + 1 = 3
    [0, 1, 2, 3, 4], // add 4 after [0, 1, 2, 3]
    [1, 2, 3, 4],    // add 4 after [1, 2, 3]
    [2, 3, 4]        // new increasing subarray
```

Therefore, when A[i] - A[i-1] == A[i-1] - A[i-2], dp[i] = dp[i-1] + 1.

Because an increasing subarray does not necessarily end at the last element and can end at any element, return the sum of the dp array.

```java
public int numberOfArithmeticSlices(int[] A) {
    if (A == null || A.length == 0) {
        return 0;
    }
    int n = A.length;
    int[] dp = new int[n];
    for (int i = 2; i < n; i++) {
        if (A[i] - A[i - 1] == A[i - 1] - A[i - 2]) {
            dp[i] = dp[i - 1] + 1;
        }
    }
    int total = 0;
    for (int cnt : dp) {
        total += cnt;
    }
    return total;
}
```

## Integer Partition

### 1. Integer Break

343\. Integer Break (Medim)

[Leetcode](https://leetcode.com/problems/integer-break/description/) / [LeetCode CN](https://leetcode-cn.com/problems/integer-break/description/)

Problem description: For example, given n = 2, return 1 (2 = 1 + 1); given n = 10, return 36 (10 = 3 + 3 + 4).

```java
public int integerBreak(int n) {
    int[] dp = new int[n + 1];
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        for (int j = 1; j <= i - 1; j++) {
            dp[i] = Math.max(dp[i], Math.max(j * dp[i - j], j * (i - j)));
        }
    }
    return dp[n];
}
```

### 2. Perfect Squares

279\. Perfect Squares(Medium)

[Leetcode](https://leetcode.com/problems/perfect-squares/description/) / [LeetCode CN](https://leetcode-cn.com/problems/perfect-squares/description/)

Problem description: For example, given n = 12, return 3 because 12 = 4 + 4 + 4; given n = 13, return 2 because 13 = 4 + 9.

```java
public int numSquares(int n) {
    List<Integer> squareList = generateSquareList(n);
    int[] dp = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        int min = Integer.MAX_VALUE;
        for (int square : squareList) {
            if (square > i) {
                break;
            }
            min = Math.min(min, dp[i - square] + 1);
        }
        dp[i] = min;
    }
    return dp[n];
}

private List<Integer> generateSquareList(int n) {
    List<Integer> squareList = new ArrayList<>();
    int diff = 3;
    int square = 1;
    while (square <= n) {
        squareList.add(square);
        square += diff;
        diff += 2;
    }
    return squareList;
}
```

### 3. Decode Ways

91\. Decode Ways (Medium)

[Leetcode](https://leetcode.com/problems/decode-ways/description/) / [LeetCode CN](https://leetcode-cn.com/problems/decode-ways/description/)

Problem description: Given encoded message "12", it could be decoded as "AB" (1 2) or "L" (12).

```java
public int numDecodings(String s) {
    if (s == null || s.length() == 0) {
        return 0;
    }
    int n = s.length();
    int[] dp = new int[n + 1];
    dp[0] = 1;
    dp[1] = s.charAt(0) == '0' ? 0 : 1;
    for (int i = 2; i <= n; i++) {
        int one = Integer.valueOf(s.substring(i - 1, i));
        if (one != 0) {
            dp[i] += dp[i - 1];
        }
        if (s.charAt(i - 2) == '0') {
            continue;
        }
        int two = Integer.valueOf(s.substring(i - 2, i));
        if (two <= 26) {
            dp[i] += dp[i - 2];
        }
    }
    return dp[n];
}
```

## Longest Increasing Subsequence

Given a sequence {S<sub>1</sub>, S<sub>2</sub>,...,S<sub>n</sub>}, take several numbers to form a new sequence {S<sub>i1</sub>, S<sub>i2</sub>,..., S<sub>im</sub>}, where i1, i2, ..., im remain increasing. That is, every number in the new sequence keeps its original relative order. The new sequence is called a **subsequence** of the original sequence.

If, in a subsequence, S<sub>ix</sub> > S<sub>iy</sub> whenever index ix > iy, the subsequence is called an **increasing subsequence** of the original sequence.

Define an array dp to store the length of the longest increasing subsequence. dp[n] represents the length of the longest increasing subsequence ending at S<sub>n</sub>. For an increasing subsequence {S<sub>i1</sub>, S<sub>i2</sub>,...,S<sub>im</sub>}, if im < n and S<sub>im</sub> < S<sub>n</sub>, then {S<sub>i1</sub>, S<sub>i2</sub>,..., S<sub>im</sub>, S<sub>n</sub>} is an increasing subsequence, and its length increases by 1. Among all increasing subsequences satisfying these conditions, the longest one is the one we need. Adding S<sub>n</sub> to that longest increasing subsequence forms the longest increasing subsequence ending at S<sub>n</sub>. Therefore, dp[n] = max{ dp[i]+1 | S<sub>i</sub> < S<sub>n</sub> && i < n}.

When computing dp[n], it may be impossible to find an increasing subsequence that satisfies the condition. In that case, {S<sub>n</sub>} itself forms an increasing subsequence, so the recurrence must be adjusted to make the minimum value of dp[n] equal to 1:

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[n]=max\{1,dp[i]+1|S_i<S_n\&\&i<n\}" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ee994da4-0fc7-443d-ac56-c08caf00a204.jpg" width="350px"> </div><br>

For a sequence of length N, the longest increasing subsequence does not necessarily end at S<sub>N</sub>, so dp[N] is not necessarily the length of the sequence's longest increasing subsequence. Traverse the dp array to find the maximum value; max{ dp[i] | 1 <= i <= N} is the desired result.

### 1. Longest Increasing Subsequence

300\. Longest Increasing Subsequence (Medium)

[Leetcode](https://leetcode.com/problems/longest-increasing-subsequence/description/) / [LeetCode CN](https://leetcode-cn.com/problems/longest-increasing-subsequence/description/)

```java
public int lengthOfLIS(int[] nums) {
    int n = nums.length;
    int[] dp = new int[n];
    for (int i = 0; i < n; i++) {
        int max = 1;
        for (int j = 0; j < i; j++) {
            if (nums[i] > nums[j]) {
                max = Math.max(max, dp[j] + 1);
            }
        }
        dp[i] = max;
    }
    return Arrays.stream(dp).max().orElse(0);
}
```

Using Stream to find the maximum value causes excessive runtime, so it can be rewritten as:

```java
int ret = 0;
for (int i = 0; i < n; i++) {
    ret = Math.max(ret, dp[i]);
}
return ret;
```

The time complexity of the solution above is O(N<sup>2</sup>). Binary search can reduce it to O(NlogN).

Define a tails array, where tails[i] stores the last element of the longest increasing subsequence with length i + 1. For an element x:

- If it is greater than every value in tails, append it to tails, indicating that the length of the longest increasing subsequence increases by 1.
- If tails[i-1] \< x \<= tails[i], update tails[i] = x.

For example, for the array [4,3,6,5]:

```html
tails      len      num
[]         0        4
[4]        1        3
[3]        1        6
[3,6]      2        5
[3,5]      2        null
```

The tails array remains ordered, so binary search can be used to find the position of S<sub>i</sub> in tails.

```java
public int lengthOfLIS(int[] nums) {
    int n = nums.length;
    int[] tails = new int[n];
    int len = 0;
    for (int num : nums) {
        int index = binarySearch(tails, len, num);
        tails[index] = num;
        if (index == len) {
            len++;
        }
    }
    return len;
}

private int binarySearch(int[] tails, int len, int key) {
    int l = 0, h = len;
    while (l < h) {
        int mid = l + (h - l) / 2;
        if (tails[mid] == key) {
            return mid;
        } else if (tails[mid] > key) {
            h = mid;
        } else {
            l = mid + 1;
        }
    }
    return l;
}
```

### 2. Maximum Length of Pair Chain

646\. Maximum Length of Pair Chain (Medium)

[Leetcode](https://leetcode.com/problems/maximum-length-of-pair-chain/description/) / [LeetCode CN](https://leetcode-cn.com/problems/maximum-length-of-pair-chain/description/)

```html
Input: [[1,2], [2,3], [3,4]]
Output: 2
Explanation: The longest chain is [1,2] -> [3,4]
```

Problem description: For (a, b) and (c, d), if b \< c, they can form a chain.

```java
public int findLongestChain(int[][] pairs) {
    if (pairs == null || pairs.length == 0) {
        return 0;
    }
    Arrays.sort(pairs, (a, b) -> (a[0] - b[0]));
    int n = pairs.length;
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (pairs[j][1] < pairs[i][0]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
    }
    return Arrays.stream(dp).max().orElse(0);
}
```

### 3. Wiggle Subsequence

376\. Wiggle Subsequence (Medium)

[Leetcode](https://leetcode.com/problems/wiggle-subsequence/description/) / [LeetCode CN](https://leetcode-cn.com/problems/wiggle-subsequence/description/)

```html
Input: [1,7,4,9,2,5]
Output: 6
The entire sequence is a wiggle sequence.

Input: [1,17,5,10,13,15,10,5,16,8]
Output: 7
There are several subsequences that achieve this length. One is [1,17,10,13,10,16,8].

Input: [1,2,3,4,5,6,7,8,9]
Output: 2
```

Requirement: solve it in O(N) time.

```java
public int wiggleMaxLength(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }
    int up = 1, down = 1;
    for (int i = 1; i < nums.length; i++) {
        if (nums[i] > nums[i - 1]) {
            up = down + 1;
        } else if (nums[i] < nums[i - 1]) {
            down = up + 1;
        }
    }
    return Math.max(up, down);
}
```

## Longest Common Subsequence

For two subsequences S1 and S2, find their longest common subsequence.

Define a two-dimensional array dp to store the length of the longest common subsequence, where dp[i][j] represents the length of the longest common subsequence between the first i characters of S1 and the first j characters of S2. Considering whether S1<sub>i</sub> equals S2<sub>j</sub>, there are two cases:

- When S1<sub>i</sub>==S2<sub>j</sub>, S1<sub>i</sub> can be added to the longest common subsequence of the first i-1 characters of S1 and the first j-1 characters of S2, increasing the length by 1: dp[i][j] = dp[i-1][j-1] + 1.
- When S1<sub>i</sub> != S2<sub>j</sub>, the longest common subsequence is either the LCS of the first i-1 characters of S1 and the first j characters of S2, or the LCS of the first i characters of S1 and the first j-1 characters of S2. Take the maximum: dp[i][j] = max{ dp[i-1][j], dp[i][j-1] }.

Therefore, the state transition equation for the longest common subsequence is:

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[i][j]=\left\{\begin{array}{rcl}dp[i-1][j-1]&&{S1_i==S2_j}\\max(dp[i-1][j],dp[i][j-1])&&{S1_i<>S2_j}\end{array}\right." class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ecd89a22-c075-4716-8423-e0ba89230e9a.jpg" width="450px"> </div><br>

For sequence S<sub>1</sub> of length N and sequence S<sub>2</sub> of length M, dp[N][M] is the length of the longest common subsequence of S<sub>1</sub> and S<sub>2</sub>.

Compared with the longest increasing subsequence, the longest common subsequence has the following differences:

- It targets two sequences and finds their longest common subsequence.
- In the longest increasing subsequence, dp[i] represents the length of the longest increasing subsequence ending at S<sub>i</sub>, and the subsequence must include S<sub>i</sub>. In the longest common subsequence, dp[i][j] represents the length of the longest common subsequence between the first i characters of S1 and the first j characters of S2, and it does not necessarily include S1<sub>i</sub> or S2<sub>j</sub>.
- When finding the final answer, dp[N][M] is the final answer for the longest common subsequence. For the longest increasing subsequence, dp[N] is not the final answer, because the longest increasing subsequence ending at S<sub>N</sub> is not necessarily the longest increasing subsequence of the entire sequence; the dp array must be traversed to find the maximum.

### 1. Longest Common Subsequence

1143\. Longest Common Subsequence

[Leetcode](https://leetcode.com/problems/longest-common-subsequence/) / [LeetCode CN](https://leetcode-cn.com/problems/longest-common-subsequence/)

```java
    public int longestCommonSubsequence(String text1, String text2) {
        int n1 = text1.length(), n2 = text2.length();
        int[][] dp = new int[n1 + 1][n2 + 1];
        for (int i = 1; i <= n1; i++) {
            for (int j = 1; j <= n2; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        return dp[n1][n2];
    }
```

## 0-1 Knapsack

There is a knapsack with capacity N. The goal is to maximize the value of items placed in the knapsack. Each item has two attributes: weight w and value v.

Define a two-dimensional array dp to store the maximum value, where dp[i][j] represents the maximum value achievable using the first i items with total weight not exceeding j. Suppose the i-th item has weight w and value v. Based on whether the i-th item is added to the knapsack, there are two cases:

- If the i-th item is not added to the knapsack, the maximum value of the first i items with total weight not exceeding j is the maximum value of the first i-1 items with total weight not exceeding j: dp[i][j] = dp[i-1][j].
- If the i-th item is added to the knapsack, dp[i][j] = dp[i-1][j-w] + v.

The i-th item may or may not be added, depending on which case gives the larger maximum value. Therefore, the state transition equation for the 0-1 knapsack is:

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[i][j]=max(dp[i-1][j],dp[i-1][j-w]+v)" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/8cb2be66-3d47-41ba-b55b-319fc68940d4.png" width="400px"> </div><br>

```java
// W is the total knapsack capacity
// N is the number of items
// weights stores the weights of N items
// values stores the values of N items
public int knapsack(int W, int N, int[] weights, int[] values) {
    int[][] dp = new int[N + 1][W + 1];
    for (int i = 1; i <= N; i++) {
        int w = weights[i - 1], v = values[i - 1];
        for (int j = 1; j <= W; j++) {
            if (j >= w) {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i - 1][j - w] + v);
            } else {
                dp[i][j] = dp[i - 1][j];
            }
        }
    }
    return dp[N][W];
}
```

**Space Optimization**  

The 0-1 knapsack can be optimized in implementation. From the state transition equation, the state of the first i items depends only on the state of the first i-1 items. Therefore, dp can be defined as a one-dimensional array, where dp[j] can represent either dp[i-1][j] or dp[i][j]. At this point:

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[j]=max(dp[j],dp[j-w]+v)" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/9ae89f16-7905-4a6f-88a2-874b4cac91f4.jpg" width="300px"> </div><br>

Because dp[j-w] represents dp[i-1][j-w], dp[i][j-w] cannot be computed first, or dp[i-1][j-w] would be overwritten. In other words, compute dp[i][j] before dp[i][j-w]. In implementation, iterate in reverse order.

```java
public int knapsack(int W, int N, int[] weights, int[] values) {
    int[] dp = new int[W + 1];
    for (int i = 1; i <= N; i++) {
        int w = weights[i - 1], v = values[i - 1];
        for (int j = W; j >= 1; j--) {
            if (j >= w) {
                dp[j] = Math.max(dp[j], dp[j - w] + v);
            }
        }
    }
    return dp[W];
}
```

**Why Greedy Does Not Work**  

The 0-1 knapsack problem cannot be solved with a greedy algorithm. That is, adding the item with the highest value-to-weight ratio first does not necessarily reach the optimum, because this approach may waste knapsack space. Consider the following items and a knapsack with capacity 5. If item 0 is added first and then item 1, the stored value is only 16, wasting 2 units of space. The optimal choice is to store item 1 and item 2, with value 22.

| id | w | v | v/w |
| --- | --- | --- | --- |
| 0 | 1 | 6 | 6 |
| 1 | 2 | 10 | 5 |
| 2 | 3 | 12 | 4 |

**Variants**  

- Complete knapsack: each item has unlimited copies

- Multiple knapsack: each item has a limited number of copies

- Multidimensional-cost knapsack: items have not only weight but also volume, and both constraints are considered

- Others: items have mutual constraints or dependencies

### 1. Partition Equal Subset Sum

416\. Partition Equal Subset Sum (Medium)

[Leetcode](https://leetcode.com/problems/partition-equal-subset-sum/description/) / [LeetCode CN](https://leetcode-cn.com/problems/partition-equal-subset-sum/description/)

```html
Input: [1, 5, 11, 5]

Output: true

Explanation: The array can be partitioned as [1, 5, 5] and [11].
```

It can be treated as a 0-1 knapsack problem with knapsack size sum/2.

```java
public boolean canPartition(int[] nums) {
    int sum = computeArraySum(nums);
    if (sum % 2 != 0) {
        return false;
    }
    int W = sum / 2;
    boolean[] dp = new boolean[W + 1];
    dp[0] = true;
    for (int num : nums) {                 // in 0-1 knapsack, each item can be used only once
        for (int i = W; i >= num; i--) {   // iterate backward: compute dp[i] before dp[i-num]
            dp[i] = dp[i] || dp[i - num];
        }
    }
    return dp[W];
}

private int computeArraySum(int[] nums) {
    int sum = 0;
    for (int num : nums) {
        sum += num;
    }
    return sum;
}
```

### 2. Target Sum

494\. Target Sum (Medium)

[Leetcode](https://leetcode.com/problems/target-sum/description/) / [LeetCode CN](https://leetcode-cn.com/problems/target-sum/description/)

```html
Input: nums is [1, 1, 1, 1, 1], S is 3.
Output: 5
Explanation:

-1+1+1+1+1 = 3
+1-1+1+1+1 = 3
+1+1-1+1+1 = 3
+1+1+1-1+1 = 3
+1+1+1+1-1 = 3

There are 5 ways to assign symbols to make the sum of nums be target 3.
```

This problem can be converted into a Subset Sum problem and solved using the 0-1 knapsack method.

This set of numbers can be viewed as two parts, P and N, where P uses positive signs and N uses negative signs. The derivation is:

```html
                  sum(P) - sum(N) = target
sum(P) + sum(N) + sum(P) - sum(N) = target + sum(P) + sum(N)
                       2 * sum(P) = target + sum(nums)
```

Therefore, as long as we find a subset whose elements all take positive signs and whose sum equals (target + sum(nums))/2, a solution exists.

```java
public int findTargetSumWays(int[] nums, int S) {
    int sum = computeArraySum(nums);
    if (sum < S || (sum + S) % 2 == 1) {
        return 0;
    }
    int W = (sum + S) / 2;
    int[] dp = new int[W + 1];
    dp[0] = 1;
    for (int num : nums) {
        for (int i = W; i >= num; i--) {
            dp[i] = dp[i] + dp[i - num];
        }
    }
    return dp[W];
}

private int computeArraySum(int[] nums) {
    int sum = 0;
    for (int num : nums) {
        sum += num;
    }
    return sum;
}
```

DFS solution:

```java
public int findTargetSumWays(int[] nums, int S) {
    return findTargetSumWays(nums, 0, S);
}

private int findTargetSumWays(int[] nums, int start, int S) {
    if (start == nums.length) {
        return S == 0 ? 1 : 0;
    }
    return findTargetSumWays(nums, start + 1, S + nums[start])
            + findTargetSumWays(nums, start + 1, S - nums[start]);
}
```

### 3. Ones and Zeroes

474\. Ones and Zeroes (Medium)

[Leetcode](https://leetcode.com/problems/ones-and-zeroes/description/) / [LeetCode CN](https://leetcode-cn.com/problems/ones-and-zeroes/description/)

```html
Input: Array = {"10", "0001", "111001", "1", "0"}, m = 5, n = 3
Output: 4

Explanation: There are totally 4 strings can be formed by the using of 5 0s and 3 1s, which are "10","0001","1","0"
```

This is a multidimensional-cost 0-1 knapsack problem with two capacities: the number of 0s and the number of 1s.

```java
public int findMaxForm(String[] strs, int m, int n) {
    if (strs == null || strs.length == 0) {
        return 0;
    }
    int[][] dp = new int[m + 1][n + 1];
    for (String s : strs) {    // each string can be used only once
        int ones = 0, zeros = 0;
        for (char c : s.toCharArray()) {
            if (c == '0') {
                zeros++;
            } else {
                ones++;
            }
        }
        for (int i = m; i >= zeros; i--) {
            for (int j = n; j >= ones; j--) {
                dp[i][j] = Math.max(dp[i][j], dp[i - zeros][j - ones] + 1);
            }
        }
    }
    return dp[m][n];
}
```

### 4. Coin Change

322\. Coin Change (Medium)

[Leetcode](https://leetcode.com/problems/coin-change/description/) / [LeetCode CN](https://leetcode-cn.com/problems/coin-change/description/)

```html
Example 1:
coins = [1, 2, 5], amount = 11
return 3 (11 = 5 + 5 + 1)

Example 2:
coins = [2], amount = 3
return -1.
```

Problem description: Given coins of several denominations, use them to make up a given amount while minimizing the number of coins. Coins can be used repeatedly.

- Item: coin
- Item size: denomination
- Item value: count

Because coins can be used repeatedly, this is a complete knapsack problem. Complete knapsack only needs to change the reverse traversal of the dp array in 0-1 knapsack to forward traversal.

```java
public int coinChange(int[] coins, int amount) {
    if (amount == 0 || coins == null) return 0;
    int[] dp = new int[amount + 1];
    for (int coin : coins) {
        for (int i = coin; i <= amount; i++) { // change reverse traversal to forward traversal
            if (i == coin) {
                dp[i] = 1;
            } else if (dp[i] == 0 && dp[i - coin] != 0) {
                dp[i] = dp[i - coin] + 1;

            } else if (dp[i - coin] != 0) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    return dp[amount] == 0 ? -1 : dp[amount];
}
```

### 5. Coin Change 2

518\. Coin Change 2 (Medium)

[Leetcode](https://leetcode.com/problems/coin-change-2/description/) / [LeetCode CN](https://leetcode-cn.com/problems/coin-change-2/description/)

```text-html-basic
Input: amount = 5, coins = [1, 2, 5]
Output: 4
Explanation: there are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1
```

This is a complete knapsack problem. Use dp to record the number of combinations that can reach the target.

```java
public int change(int amount, int[] coins) {
    if (coins == null) {
        return 0;
    }
    int[] dp = new int[amount + 1];
    dp[0] = 1;
    for (int coin : coins) {
        for (int i = coin; i <= amount; i++) {
            dp[i] += dp[i - coin];
        }
    }
    return dp[amount];
}
```

### 6. Word Break

139\. Word Break (Medium)

[Leetcode](https://leetcode.com/problems/word-break/description/) / [LeetCode CN](https://leetcode-cn.com/problems/word-break/description/)

```html
s = "leetcode",
dict = ["leet", "code"].
Return true because "leetcode" can be segmented as "leet code".
```

Words in dict have no usage limit, so this is a complete knapsack problem.

This problem involves the usage order of words in the dictionary. In other words, items must be placed into the knapsack in a certain order. For example, the following dict is not enough to form the string "leetcode":

```html
["lee", "tc", "cod"]
```

When solving an ordered complete knapsack problem, item iteration should be placed in the innermost loop and knapsack iteration in the outer loop. Only then can items be placed into the knapsack in a specific order.

```java
public boolean wordBreak(String s, List<String> wordDict) {
    int n = s.length();
    boolean[] dp = new boolean[n + 1];
    dp[0] = true;
    for (int i = 1; i <= n; i++) {
        for (String word : wordDict) {   // item iteration should be in the innermost loop
            int len = word.length();
            if (len <= i && word.equals(s.substring(i - len, i))) {
                dp[i] = dp[i] || dp[i - len];
            }
        }
    }
    return dp[n];
}
```

### 7. Combination Sum IV

377\. Combination Sum IV (Medium)

[Leetcode](https://leetcode.com/problems/combination-sum-iv/description/) / [LeetCode CN](https://leetcode-cn.com/problems/combination-sum-iv/description/)

```html
nums = [1, 2, 3]
target = 4

The possible combination ways are:
(1, 1, 1, 1)
(1, 1, 2)
(1, 2, 1)
(1, 3)
(2, 1, 1)
(2, 2)
(3, 1)

Note that different sequences are counted as different combinations.

Therefore the output is 7.
```

This is an ordered complete knapsack problem.

```java
public int combinationSum4(int[] nums, int target) {
    if (nums == null || nums.length == 0) {
        return 0;
    }
    int[] maximum = new int[target + 1];
    maximum[0] = 1;
    Arrays.sort(nums);
    for (int i = 1; i <= target; i++) {
        for (int j = 0; j < nums.length && nums[j] <= i; j++) {
            maximum[i] += maximum[i - nums[j]];
        }
    }
    return maximum[target];
}
```

## Stock Trading

### 1. Best Time to Buy and Sell Stock with Cooldown

309\. Best Time to Buy and Sell Stock with Cooldown(Medium)

[Leetcode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/description/) / [LeetCode CN](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/description/)

Problem description: There must be a one-day cooldown after each transaction.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ffd96b99-8009-487c-8e98-11c9d44ef14f.png" width="300px"> </div><br>

```java
public int maxProfit(int[] prices) {
    if (prices == null || prices.length == 0) {
        return 0;
    }
    int N = prices.length;
    int[] buy = new int[N];
    int[] s1 = new int[N];
    int[] sell = new int[N];
    int[] s2 = new int[N];
    s1[0] = buy[0] = -prices[0];
    sell[0] = s2[0] = 0;
    for (int i = 1; i < N; i++) {
        buy[i] = s2[i - 1] - prices[i];
        s1[i] = Math.max(buy[i - 1], s1[i - 1]);
        sell[i] = Math.max(buy[i - 1], s1[i - 1]) + prices[i];
        s2[i] = Math.max(s2[i - 1], sell[i - 1]);
    }
    return Math.max(sell[N - 1], s2[N - 1]);
}
```

### 2. Best Time to Buy and Sell Stock with Transaction Fee

714\. Best Time to Buy and Sell Stock with Transaction Fee (Medium)

[Leetcode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/description/) / [LeetCode CN](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/description/)

```html
Input: prices = [1, 3, 2, 8, 4, 9], fee = 2
Output: 8
Explanation: The maximum profit can be achieved by:
Buying at prices[0] = 1
Selling at prices[3] = 8
Buying at prices[4] = 4
Selling at prices[5] = 9
The total profit is ((8 - 1) - 2) + ((9 - 4) - 2) = 8.
```

Problem description: Each transaction requires paying a certain fee.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1e2c588c-72b7-445e-aacb-d55dc8a88c29.png" width="300px"> </div><br>

```java
public int maxProfit(int[] prices, int fee) {
    int N = prices.length;
    int[] buy = new int[N];
    int[] s1 = new int[N];
    int[] sell = new int[N];
    int[] s2 = new int[N];
    s1[0] = buy[0] = -prices[0];
    sell[0] = s2[0] = 0;
    for (int i = 1; i < N; i++) {
        buy[i] = Math.max(sell[i - 1], s2[i - 1]) - prices[i];
        s1[i] = Math.max(buy[i - 1], s1[i - 1]);
        sell[i] = Math.max(buy[i - 1], s1[i - 1]) - fee + prices[i];
        s2[i] = Math.max(s2[i - 1], sell[i - 1]);
    }
    return Math.max(sell[N - 1], s2[N - 1]);
}
```


### 3. Best Time to Buy and Sell Stock III

123\. Best Time to Buy and Sell Stock III (Hard)

[Leetcode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/description/) / [LeetCode CN](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iii/description/)

```java
public int maxProfit(int[] prices) {
    int firstBuy = Integer.MIN_VALUE, firstSell = 0;
    int secondBuy = Integer.MIN_VALUE, secondSell = 0;
    for (int curPrice : prices) {
        if (firstBuy < -curPrice) {
            firstBuy = -curPrice;
        }
        if (firstSell < firstBuy + curPrice) {
            firstSell = firstBuy + curPrice;
        }
        if (secondBuy < firstSell - curPrice) {
            secondBuy = firstSell - curPrice;
        }
        if (secondSell < secondBuy + curPrice) {
            secondSell = secondBuy + curPrice;
        }
    }
    return secondSell;
}
```

### 4. Best Time to Buy and Sell Stock IV

188\. Best Time to Buy and Sell Stock IV (Hard)

[Leetcode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/description/) / [LeetCode CN](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iv/description/)

```java
public int maxProfit(int k, int[] prices) {
    int n = prices.length;
    if (k >= n / 2) {   // in this case, the problem degrades to the regular stock trading problem
        int maxProfit = 0;
        for (int i = 1; i < n; i++) {
            if (prices[i] > prices[i - 1]) {
                maxProfit += prices[i] - prices[i - 1];
            }
        }
        return maxProfit;
    }
    int[][] maxProfit = new int[k + 1][n];
    for (int i = 1; i <= k; i++) {
        int localMax = maxProfit[i - 1][0] - prices[0];
        for (int j = 1; j < n; j++) {
            maxProfit[i][j] = Math.max(maxProfit[i][j - 1], prices[j] + localMax);
            localMax = Math.max(localMax, maxProfit[i - 1][j] - prices[j]);
        }
    }
    return maxProfit[k][n - 1];
}
```

## String Editing

### 1. Delete Operation for Two Strings

583\. Delete Operation for Two Strings (Medium)

[Leetcode](https://leetcode.com/problems/delete-operation-for-two-strings/description/) / [LeetCode CN](https://leetcode-cn.com/problems/delete-operation-for-two-strings/description/)

```html
Input: "sea", "eat"
Output: 2
Explanation: You need one step to make "sea" to "ea" and another step to make "eat" to "ea".
```

It can be converted into a problem of finding the longest common subsequence of two strings.

```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i][j - 1], dp[i - 1][j]);
            }
        }
    }
    return m + n - 2 * dp[m][n];
}
```

### 2. Edit Distance

72\. Edit Distance (Hard)

[Leetcode](https://leetcode.com/problems/edit-distance/description/) / [LeetCode CN](https://leetcode-cn.com/problems/edit-distance/description/)

```html
Example 1:

Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation:
horse -> rorse (replace 'h' with 'r')
rorse -> rose (remove 'r')
rose -> ros (remove 'e')
Example 2:

Input: word1 = "intention", word2 = "execution"
Output: 5
Explanation:
intention -> inention (remove 't')
inention -> enention (replace 'i' with 'e')
enention -> exention (replace 'n' with 'x')
exention -> exection (replace 'n' with 'c')
exection -> execution (insert 'u')
```

Problem description: Modify one string into another string with the fewest operations. One edit operation can insert a character, delete a character, or replace a character.

```java
public int minDistance(String word1, String word2) {
    if (word1 == null || word2 == null) {
        return 0;
    }
    int m = word1.length(), n = word2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i++) {
        dp[i][0] = i;
    }
    for (int i = 1; i <= n; i++) {
        dp[0][i] = i;
    }
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = Math.min(dp[i - 1][j - 1], Math.min(dp[i][j - 1], dp[i - 1][j])) + 1;
            }
        }
    }
    return dp[m][n];
}
```

### 3. 2 Keys Keyboard

650\. 2 Keys Keyboard (Medium)

[Leetcode](https://leetcode.com/problems/2-keys-keyboard/description/) / [LeetCode CN](https://leetcode-cn.com/problems/2-keys-keyboard/description/)

Problem description: Initially there is only one character A. Find how many operations are needed to obtain n characters A. Each operation can either copy all current characters or paste.

```
Input: 3
Output: 3
Explanation:
Intitally, we have one character 'A'.
In step 1, we use Copy All operation.
In step 2, we use Paste operation to get 'AA'.
In step 3, we use Paste operation to get 'AAA'.
```

```java
public int minSteps(int n) {
    if (n == 1) return 0;
    for (int i = 2; i <= Math.sqrt(n); i++) {
        if (n % i == 0) return i + minSteps(n / i);
    }
    return n;
}
```

```java
public int minSteps(int n) {
    int[] dp = new int[n + 1];
    int h = (int) Math.sqrt(n);
    for (int i = 2; i <= n; i++) {
        dp[i] = i;
        for (int j = 2; j <= h; j++) {
            if (i % j == 0) {
                dp[i] = dp[j] + dp[i / j];
                break;
            }
        }
    }
    return dp[n];
}
```
