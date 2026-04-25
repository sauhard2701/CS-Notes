# 19. Regular Expression Matching

[NowCoder](https://www.nowcoder.com/practice/28970c15befb4ff3a264189087b99ad4?tpId=13&tqId=11205&tab=answerKey&from=cyc_github)

## Problem Description

Implement a function to match regular expressions that include '.' and '\*'. In the pattern, '.' represents any single character, and '\*' means the preceding character can appear any number of times, including 0.

In this problem, matching means all characters in the string match the entire pattern. For example, the string "aaa" matches the patterns "a.a" and "ab\*ac\*a", but does not match either "aa.a" or "ab\*a".

## Solution

Note that '.' is used as any single character, while '\*' repeats the preceding character. They have different roles; do not compare '.' with '\*' and treat it as repeating the preceding character once.

```java
public boolean match(String str, String pattern) {

    int m = str.length(), n = pattern.length();
    boolean[][] dp = new boolean[m + 1][n + 1];

    dp[0][0] = true;
    for (int i = 1; i <= n; i++)
        if (pattern.charAt(i - 1) == '*')
            dp[0][i] = dp[0][i - 2];

    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
            if (str.charAt(i - 1) == pattern.charAt(j - 1) || pattern.charAt(j - 1) == '.')
                dp[i][j] = dp[i - 1][j - 1];
            else if (pattern.charAt(j - 1) == '*')
                if (pattern.charAt(j - 2) == str.charAt(i - 1) || pattern.charAt(j - 2) == '.') {
                    dp[i][j] |= dp[i][j - 1]; // a* counts as single a
                    dp[i][j] |= dp[i - 1][j]; // a* counts as multiple a
                    dp[i][j] |= dp[i][j - 2]; // a* counts as empty
                } else
                    dp[i][j] = dp[i][j - 2];   // a* only counts as empty

    return dp[m][n];
}
```
