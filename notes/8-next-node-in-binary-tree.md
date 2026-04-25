# 8. Next Node in Binary Tree

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/9023a0c988684a53960365b889ceaf5e?tpId=13&tqId=11210&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Given a binary tree and one node in it, find and return the next node in inorder traversal order. Note that nodes in the tree contain not only left and right child nodes, but also a pointer to the parent node.

```java
public class TreeLinkNode {

    int val;
    TreeLinkNode left = null;
    TreeLinkNode right = null;
    TreeLinkNode next = null; // Pointer to the parent node

    TreeLinkNode(int val) {
        this.val = val;
    }
}
```

## Solution

First review inorder traversal: traverse the left subtree, then the root node, and finally the right subtree. Therefore, the leftmost node is the first node in inorder traversal.

```java
void traverse(TreeNode root) {
    if (root == null) return;
    traverse(root.left);
    visit(root);
    traverse(root.right);
}
```

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ad5cc8fc-d59b-45ce-8899-63a18320d97e.gif" width="300px"/> </div><br>



① If a node has a non-empty right subtree, then its next node is the leftmost node of the right subtree;

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7008dc2b-6f13-4174-a516-28b2d75b0152.gif" width="300px"/> </div><br>

② Otherwise, move upward to find the first ancestor whose left link points to a tree containing this node.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/094e3ac8-e080-4e94-9f0a-64c25abc695e.gif" width="300px"/> </div><br>

```java
public TreeLinkNode GetNext(TreeLinkNode pNode) {
    if (pNode.right != null) {
        TreeLinkNode node = pNode.right;
        while (node.left != null)
            node = node.left;
        return node;
    } else {
        while (pNode.next != null) {
            TreeLinkNode parent = pNode.next;
            if (parent.left == pNode)
                return parent;
            pNode = pNode.next;
        }
    }
    return null;
}
```
