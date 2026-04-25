# 5. Replace Spaces

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/0e26e5551f2b489b9f58bc83aa4b6c68?tpId=13&tqId=11155&tab=answerKey&from=cyc_github)

## Problem Description


Replace every space in a string with "%20".

```text
Input:
"A B"

Output:
"A%20B"
```

## Solution

① Append arbitrary characters to the end of the string so that its length equals the length after replacement. Because one space is replaced by three characters (%20), two arbitrary characters need to be appended for each space encountered.

② Let P1 point to the original end of the string, and P2 point to the current end of the string. Traverse P1 and P2 from back to front. When P1 reaches a space, fill the positions pointed to by P2 with 02% in order, noting that this is reversed; otherwise, fill in the character pointed to by P1. Traversing from back to front prevents changes at P2 from affecting the original string content being traversed by P1.

③ Exit when P2 meets P1 (P2 \<= P1), or when traversal ends (P1 \< 0).



<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f7c1fea2-c1e7-4d31-94b5-0d9df85e093c.gif" width="350px"> </div><br>

```java
public String replaceSpace(StringBuffer str) {
    int P1 = str.length() - 1;
    for (int i = 0; i <= P1; i++)
        if (str.charAt(i) == ' ')
            str.append("  ");

    int P2 = str.length() - 1;
    while (P1 >= 0 && P2 > P1) {
        char c = str.charAt(P1--);
        if (c == ' ') {
            str.setCharAt(P2--, '0');
            str.setCharAt(P2--, '2');
            str.setCharAt(P2--, '%');
        } else {
            str.setCharAt(P2--, c);
        }
    }
    return str.toString();
}
```
