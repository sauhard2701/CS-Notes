# 7. Reconstruct Binary Tree

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/8a19cbe657394eeaac2f6ea9b0f6fcf6?tpId=13&tqId=11157&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Reconstruct a binary tree from its preorder traversal and inorder traversal results. Assume neither traversal contains duplicate numbers.



<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191102210342488.png" width="400"/> </div><br>

## Solution

The first value in preorder traversal is the root node value. Use this value to split the inorder traversal result into two parts: the left part is the inorder traversal result of the left subtree, and the right part is the inorder traversal result of the right subtree. Then recursively solve the left and right subtrees.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/60c4a44c-7829-4242-b3a1-26c3b513aaf0.gif" width="430px"> </div><br>

```java
// Cache the index corresponding to each value in the inorder traversal array
private Map<Integer, Integer> indexForInOrders = new HashMap<>();

public TreeNode reConstructBinaryTree(int[] pre, int[] in) {
    for (int i = 0; i < in.length; i++)
        indexForInOrders.put(in[i], i);
    return reConstructBinaryTree(pre, 0, pre.length - 1, 0);
}

private TreeNode reConstructBinaryTree(int[] pre, int preL, int preR, int inL) {
    if (preL > preR)
        return null;
    TreeNode root = new TreeNode(pre[preL]);
    int inIndex = indexForInOrders.get(root.val);
    int leftTreeSize = inIndex - inL;
    root.left = reConstructBinaryTree(pre, preL + 1, preL + leftTreeSize, inL);
    root.right = reConstructBinaryTree(pre, preL + leftTreeSize + 1, preR, inL + leftTreeSize + 1);
    return root;
}
```
