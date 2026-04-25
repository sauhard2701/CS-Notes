# 4. Search in 2D Array

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/abc3fe2ce8e146608e868a70efebf62e?tpId=13&tqId=11154&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Given a two-dimensional array where each row is sorted increasingly from left to right and each column is sorted increasingly from top to bottom, determine whether a given number exists in the array.

```html
Consider the following matrix:
[
  [1,   4,  7, 11, 15],
  [2,   5,  8, 12, 19],
  [3,   6,  9, 16, 22],
  [10, 13, 14, 17, 24],
  [18, 21, 23, 26, 30]
]

Given target = 5, return true.
Given target = 20, return false.
```

## Solution

The required time complexity is O(M + N), and the space complexity is O(1), where M is the number of rows and N is the number of columns.

For a number in this two-dimensional array, smaller numbers must be to its left, and larger numbers must be below it. Therefore, starting from the top-right corner allows the search range to shrink quickly based on the relationship between target and the current element, removing one row or one column each time. The search range for the current element is all elements in the lower-left area.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/35a8c711-0dc0-4613-95f3-be96c6c6e104.gif" width="400px"> </div><br>

```java
public boolean Find(int target, int[][] matrix) {
    if (matrix == null || matrix.length == 0 || matrix[0].length == 0)
        return false;
    int rows = matrix.length, cols = matrix[0].length;
    int r = 0, c = cols - 1; // Start from the top-right corner
    while (r <= rows - 1 && c >= 0) {
        if (target == matrix[r][c])
            return true;
        else if (target > matrix[r][c])
            r++;
        else
            c--;
    }
    return false;
}
```
