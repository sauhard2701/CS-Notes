# 46. Translate Number to String

[Leetcode](https://leetcode.com/problems/decode-ways/description/)

## Problem Description

Given a number, translate it into a string according to the following rules: 1 translates to "a", 2 translates to "b"... and 26 translates to "z". A number may have multiple possible translations. For example, 12258 has 5 translations: abbeh, lbeh, aveh, abyh, and lyh. Implement a function to count how many different translation methods a number has.

## Solution

```java
public int numDecodings(String s) {
    if (s == null || s.length() == 0)
        return 0;
    int n = s.length();
    int[] dp = new int[n + 1];
    dp[0] = 1;
    dp[1] = s.charAt(0) == '0' ? 0 : 1;
    for (int i = 2; i <= n; i++) {
        int one = Integer.valueOf(s.substring(i - 1, i));
        if (one != 0)
            dp[i] += dp[i - 1];
        if (s.charAt(i - 2) == '0')
            continue;
        int two = Integer.valueOf(s.substring(i - 2, i));
        if (two <= 26)
            dp[i] += dp[i - 2];
    }
    return dp[n];
}
```
