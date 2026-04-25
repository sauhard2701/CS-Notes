# 29. Print Matrix Clockwise

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/9b4c81a02cd34f76be2659fa0d54342a?tpId=13&tqId=11172&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Print the matrix values clockwise from the outside to the inside. The matrix below prints as: 1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20201104010349296.png" width="300px"> </div><br>



## Solution

Print layer by layer from the outside to the inside. Each layer follows the same processing steps; only the top, bottom, left, and right boundaries differ. Therefore, use four variables r1, r2, c1, and c2 to store the top, bottom, left, and right boundaries and define the current outermost layer. The print order for the current outermost layer is: print the top row from left to right -\> print the right column from top to bottom -\> print the bottom row from right to left -\> print the left column from bottom to top. Note that the bottom row should be printed only when r1 != r2, meaning the current outermost layer has more than one row. If the current outermost layer has only one row, printing the bottom row again would cause duplicate output. The left column needs the same treatment.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20201104010609223.png" width="500px"> </div><br>

```java
public ArrayList<Integer> printMatrix(int[][] matrix) {
    ArrayList<Integer> ret = new ArrayList<>();
    int r1 = 0, r2 = matrix.length - 1, c1 = 0, c2 = matrix[0].length - 1;
    while (r1 <= r2 && c1 <= c2) {
        // Top
        for (int i = c1; i <= c2; i++)
            ret.add(matrix[r1][i]);
        // Right
        for (int i = r1 + 1; i <= r2; i++)
            ret.add(matrix[i][c2]);
        if (r1 != r2)
            // Bottom
            for (int i = c2 - 1; i >= c1; i--)
                ret.add(matrix[r2][i]);
        if (c1 != c2)
            // Left
            for (int i = r2 - 1; i > r1; i--)
                ret.add(matrix[i][c1]);
        r1++; r2--; c1++; c2--;
    }
    return ret;
}
```
