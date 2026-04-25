# 67. String to Integer

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/1277c681251b4372bdef344468e4f26e?tpId=13&tqId=11202&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Convert a string to an integer. If the string is not a valid numeric value, return 0. Library functions for converting strings to integers must not be used.

```html
Iuput:
+2147483647
1a33

Output:
2147483647
0
```

## Solution

```java
public int StrToInt(String str) {
    if (str == null || str.length() == 0)
        return 0;
    boolean isNegative = str.charAt(0) == '-';
    int ret = 0;
    for (int i = 0; i < str.length(); i++) {
        char c = str.charAt(i);
        if (i == 0 && (c == '+' || c == '-'))  /* Sign check */
            continue;
        if (c < '0' || c > '9')                /* Invalid input */
            return 0;
        ret = ret * 10 + (c - '0');
    }
    return isNegative ? -ret : ret;
}
```
