# 14. Cutting Rope

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/57d85990ba5b440ab888fc72b0751bf8?tpId=13&tqId=33257&tab=answerKey&from=cyc_github)

## Problem Description

Cut a rope into multiple segments so that the product of the segment lengths is maximized.

```html
n = 2
return 1 (2 = 1 + 1)

n = 10
return 36 (10 = 3 + 3 + 4)
```

## Solution

### Greedy

Cut as many segments of length 3 as possible, and do not allow a segment of length 1. If a length-1 segment appears, take one existing length-3 segment and combine it with the length-1 segment, then cut them into two length-2 segments. The proof is as follows.

If the rope is split into 1 and n-1, then 1(n-1)-n=-1\<0, so the product after splitting is always smaller. Therefore, a length-1 segment should not appear.

If the rope is split into 2 and n-2, then 2(n-2)-n = n-4. When n\>=4, this split gives a larger product than not splitting.

If the rope is split into 3 and n-3, then 3(n-3)-n = 2n-9, which is better when n\>=5.

If the rope is split into 4 and n-4, since 4=2\*2, the effect is the same as splitting off 2.

If the rope is split into 5 and n-5, since 5=2+3 and 5\<2\*3, a length-5 segment should not appear; it should be split into 2 and 3 as much as possible.

If the rope is split into 6 and n-6, since 6=3+3 and 6\<3\*3, a length-6 segment should not appear; it should be split into 3 and 3. Here, 6 can also be split as 6=2+2+2, but 3(n - 3) - 2(n - 2) = n - 5 \>= 0, so when n\>=5, splitting off 3 is better than splitting off 2.

Continuing to split into larger segments shows that they are all worse than splitting into 2 and 3. Therefore, only splits into 2 and 3 are considered, with priority given to 3. When the remaining rope length n is 4, meaning 3+1 would occur, it must be split into 2+2.

```java
public int cutRope(int n) {
    if (n < 2)
        return 0;
    if (n == 2)
        return 1;
    if (n == 3)
        return 2;
    int timesOf3 = n / 3;
    if (n - timesOf3 * 3 == 1)
        timesOf3--;
    int timesOf2 = (n - timesOf3 * 3) / 2;
    return (int) (Math.pow(3, timesOf3)) * (int) (Math.pow(2, timesOf2));
}
```

### Dynamic Programming

```java
public int cutRope(int n) {
    int[] dp = new int[n + 1];
    dp[1] = 1;
    for (int i = 2; i <= n; i++)
        for (int j = 1; j < i; j++)
            dp[i] = Math.max(dp[i], Math.max(j * (i - j), dp[j] * (i - j)));
    return dp[n];
}
```

