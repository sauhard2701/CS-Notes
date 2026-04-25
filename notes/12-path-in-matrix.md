# 12. Path in Matrix

[NowCoder](https://www.nowcoder.com/practice/69fe7a584f0a445da1b6652978de5c38?tpId=13&tqId=11218&tab=answerKey&from=cyc_github)

## Problem Description

Determine whether a path exists in a matrix that contains all characters of a given string. The path can start from any cell in the matrix, and each step can move one cell up, down, left, or right. If a path has visited a cell, it cannot enter that cell again.

For example, the following matrix contains a path bfce.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1db1c7ea-0443-478b-8df9-7e33b1336cc4.png" width="200px"> </div><br>

## Solution

Use backtracking to solve this. It is a brute-force search method that solves a problem by searching all possible results. When one search finishes, backtracking needs to roll back and clear the state set during that search, then start a new search. In the example below, starting from f gives 4 possible next searches. If b is searched first, b must be marked as used to prevent reuse. After that search finishes, b must be cleared from the used state, and c is searched next.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/dc964b86-7a08-4bde-a3d9-e6ddceb29f98.png" width="200px"> </div><br>

The input for this problem is an array rather than a matrix (two-dimensional array), so the array must first be converted into a matrix.

```java
public class Solution {
    private final static int[][] next = {{0, -1}, {0, 1}, {-1, 0}, {1, 0}};
    private int rows;
    private int cols;

    public boolean hasPath (String val, int rows, int cols, String path) {
        if (rows == 0 || cols == 0) return false;
        this.rows = rows;
        this.cols = cols;
        char[] array = val.toCharArray();
        char[][] matrix = buildMatrix(array);
        char[] pathList = path.toCharArray();
        boolean[][] marked = new boolean[rows][cols];
        for (int i = 0; i < rows; i++)
            for (int j = 0; j < cols; j++)
                if (backtracking(matrix, pathList, marked, 0, i, j))
                    return true;

        return false;
    }

    private boolean backtracking(char[][] matrix, char[] pathList,
                                 boolean[][] marked, int pathLen, int r, int c) {

        if (pathLen == pathList.length) return true;
        if (r < 0 || r >= rows || c < 0 || c >= cols
                || matrix[r][c] != pathList[pathLen] || marked[r][c]) {

            return false;
        }
        marked[r][c] = true;
        for (int[] n : next)
            if (backtracking(matrix, pathList, marked, pathLen + 1, r + n[0], c + n[1]))
                return true;
        marked[r][c] = false;
        return false;
    }

    private char[][] buildMatrix(char[] array) {
        char[][] matrix = new char[rows][cols];
        for (int r = 0, idx = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                matrix[r][c] = array[idx++];
        return matrix;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        String val = "ABCESFCSADEE";
        int rows = 3;
        int cols = 4;
        String path = "ABCCED";
        boolean res = solution.hasPath(val, rows, cols, path);
        System.out.println(res);
    }
}
```
