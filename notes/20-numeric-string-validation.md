# 20. Numeric String Validation

[NowCoder](https://www.nowcoder.com/practice/e69148f8528c4039ad89bb2546fd4ff8?tpId=13&tqId=11206&tab=answerKey&from=cyc_github)

## Problem Description

```
true

"+100"
"5e2"
"-123"
"3.1416"
"-1E-16"
```

```
false

"12e"
"1a3.14"
"1.2.3"
"+-5"
"12e+4.3"
```


## Solution

Use a regular expression for matching.

```html
[]  : character set
()  : grouping
?   : repeat 0 to 1 time
+   : repeat 1 to n times
*   : repeat 0 to n times
.   : any character
\\. : escaped .
\\d : digit
```

```java
public boolean isNumeric (String str) {
    if (str == null || str.length() == 0)
        return false;
    return new String(str).matches("[+-]?\\d*(\\.\\d+)?([eE][+-]?\\d+)?");
}
```
