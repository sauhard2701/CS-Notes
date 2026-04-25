# Algorithms - Symbol Tables
<!-- GFM-TOC -->
* [Algorithms - Symbol Tables](#algorithms---symbol-tables)
    * [Preface](#preface)
    * [Basic Implementations](#basic-implementations)
        * [1. Unordered Symbol Table with Linked List](#1-unordered-symbol-table-with-linked-list)
        * [2. Ordered Symbol Table with Binary Search](#2-ordered-symbol-table-with-binary-search)
    * [Binary Search Trees](#binary-search-trees)
        * [1. get()](#1-get)
        * [2. put()](#2-put)
        * [3. Analysis](#3-analysis)
        * [4. floor()](#4-floor)
        * [5. rank()](#5-rank)
        * [6. min()](#6-min)
        * [7. deleteMin()](#7-deletemin)
        * [8. delete()](#8-delete)
        * [9. keys()](#9-keys)
        * [10. Analysis](#10-analysis)
    * [2-3 Search Trees](#2-3-search-trees)
        * [1. Insertion](#1-insertion)
        * [2. Properties](#2-properties)
    * [Red-Black Trees](#red-black-trees)
        * [1. Left Rotation](#1-left-rotation)
        * [2. Right Rotation](#2-right-rotation)
        * [3. Color Flip](#3-color-flip)
        * [4. Insertion](#4-insertion)
        * [5. Analysis](#5-analysis)
    * [Hash Tables](#hash-tables)
        * [1. Hash Functions](#1-hash-functions)
        * [2. Separate Chaining](#2-separate-chaining)
        * [3. Linear Probing](#3-linear-probing)
    * [Summary](#summary)
        * [1. Symbol Table Algorithm Comparison](#1-symbol-table-algorithm-comparison)
        * [2. Java Symbol Table Implementations](#2-java-symbol-table-implementations)
        * [3. Sparse Vector Multiplication](#3-sparse-vector-multiplication)
<!-- GFM-TOC -->


## Preface

A symbol table is a data structure that stores key-value pairs and supports fast lookup.

Symbol tables are divided into ordered and unordered types. Ordered symbol tables mainly support operations such as min() and max(), which are implemented based on key ordering.

Keys in an ordered symbol table need to implement the Comparable interface.

```java
public interface UnorderedST<Key, Value> {

    int size();

    Value get(Key key);

    void put(Key key, Value value);

    void delete(Key key);
}
```

```java
public interface OrderedST<Key extends Comparable<Key>, Value> {

    int size();

    void put(Key key, Value value);

    Value get(Key key);

    Key min();

    Key max();

    int rank(Key key);

    List<Key> keys(Key l, Key h);
}
```

## Basic Implementations

### 1. Unordered Symbol Table with Linked List

```java
public class ListUnorderedST<Key, Value> implements UnorderedST<Key, Value> {

    private Node first;

    private class Node {
        Key key;
        Value value;
        Node next;

        Node(Key key, Value value, Node next) {
            this.key = key;
            this.value = value;
            this.next = next;
        }
    }

    @Override
    public int size() {
        int cnt = 0;
        Node cur = first;
        while (cur != null) {
            cnt++;
            cur = cur.next;
        }
        return cnt;
    }

    @Override
    public void put(Key key, Value value) {
        Node cur = first;
        // If a node whose key equals key is found in the list, update its value to value
        while (cur != null) {
            if (cur.key.equals(key)) {
                cur.value = value;
                return;
            }
            cur = cur.next;
        }
        // Otherwise, insert a new node at the head
        first = new Node(key, value, first);
    }

    @Override
    public void delete(Key key) {
        if (first == null)
            return;
        if (first.key.equals(key))
            first = first.next;
        Node pre = first, cur = first.next;
        while (cur != null) {
            if (cur.key.equals(key)) {
                pre.next = cur.next;
                return;
            }
            pre = pre.next;
            cur = cur.next;
        }
    }

    @Override
    public Value get(Key key) {
        Node cur = first;
        while (cur != null) {
            if (cur.key.equals(key))
                return cur.value;
            cur = cur.next;
        }
        return null;
    }
}
```

### 2. Ordered Symbol Table with Binary Search

Use a pair of parallel arrays: one stores keys and the other stores values.

The rank() method of binary search is crucial. When a key is in the table, it can determine the key's position; when the key is not in the table, it can determine where to insert the new key.

Binary search requires at most logN+1 comparisons. Lookup in a symbol table implemented with binary search takes at most logarithmic time. However, insertion requires moving array elements and is linear.

```java
public class BinarySearchOrderedST<Key extends Comparable<Key>, Value> implements OrderedST<Key, Value> {

    private Key[] keys;
    private Value[] values;
    private int N = 0;

    public BinarySearchOrderedST(int capacity) {
        keys = (Key[]) new Comparable[capacity];
        values = (Value[]) new Object[capacity];
    }

    @Override
    public int size() {
        return N;
    }

    @Override
    public int rank(Key key) {
        int l = 0, h = N - 1;
        while (l <= h) {
            int m = l + (h - l) / 2;
            int cmp = key.compareTo(keys[m]);
            if (cmp == 0)
                return m;
            else if (cmp < 0)
                h = m - 1;
            else
                l = m + 1;
        }
        return l;
    }

    @Override
    public List<Key> keys(Key l, Key h) {
        int index = rank(l);
        List<Key> list = new ArrayList<>();
        while (keys[index].compareTo(h) <= 0) {
            list.add(keys[index]);
            index++;
        }
        return list;
    }

    @Override
    public void put(Key key, Value value) {
        int index = rank(key);
        // If an existing node whose key is key is found, update its value to value
        if (index < N && keys[index].compareTo(key) == 0) {
            values[index] = value;
            return;
        }
        // Otherwise, insert a new node into the array by first moving all elements after the insertion position one slot back
        for (int j = N; j > index; j--) {
            keys[j] = keys[j - 1];
            values[j] = values[j - 1];
        }
        keys[index] = key;
        values[index] = value;
        N++;
    }

    @Override
    public Value get(Key key) {
        int index = rank(key);
        if (index < N && keys[index].compareTo(key) == 0)
            return values[index];
        return null;
    }

    @Override
    public Key min() {
        return keys[0];
    }

    @Override
    public Key max() {
        return keys[N - 1];
    }
}
```

## Binary Search Trees

A **binary tree**   is either an empty link or a node with left and right links, each pointing to a binary subtree.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/c11528f6-fc71-4a2b-8d2f-51b8954c38f1.jpg" width="180"/> </div><br>

A **binary search tree**   (BST) is a binary tree in which each node's value is greater than or equal to all values in its left subtree and less than or equal to all values in its right subtree.

A BST has an important property: the result of its inorder traversal is sorted in increasing order.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ef552ae3-ae0d-4217-88e6-99cbe8163f0c.jpg" width="200"/> </div><br>

Basic data structure:

```java
public class BST<Key extends Comparable<Key>, Value> implements OrderedST<Key, Value> {

    protected Node root;

    protected class Node {
        Key key;
        Value val;
        Node left;
        Node right;
        // Total number of nodes in the subtree rooted at this node
        int N;
        // Used in red-black trees
        boolean color;

        Node(Key key, Value val, int N) {
            this.key = key;
            this.val = val;
            this.N = N;
        }
    }

    @Override
    public int size() {
        return size(root);
    }

    private int size(Node x) {
        if (x == null)
            return 0;
        return x.N;
    }

    protected void recalculateSize(Node x) {
        x.N = size(x.left) + size(x.right) + 1;
    }
}
```

For easier diagrams, empty links in binary trees are not shown below.

### 1. get()

- If the tree is empty, the lookup misses;
- If the searched key equals the root key, the lookup hits;
- Otherwise, recursively search the subtrees: if the searched key is smaller, search the left subtree; if it is larger, search the right subtree.

```java
@Override
public Value get(Key key) {
    return get(root, key);
}

private Value get(Node x, Key key) {
    if (x == null)
        return null;
    int cmp = key.compareTo(x.key);
    if (cmp == 0)
        return x.val;
    else if (cmp < 0)
        return get(x.left, key);
    else
        return get(x.right, key);
}
```

### 2. put()

When the inserted key does not exist in the tree, create a new node and update the link in the parent node to point to it, so the new node is correctly linked into the tree.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/58b70113-3876-49af-85a9-68eb00a72d59.jpg" width="200"/> </div><br>

```java
 @Override
public void put(Key key, Value value) {
    root = put(root, key, value);
}

private Node put(Node x, Key key, Value value) {
    if (x == null)
        return new Node(key, value, 1);
    int cmp = key.compareTo(x.key);
    if (cmp == 0)
        x.val = value;
    else if (cmp < 0)
        x.left = put(x.left, key, value);
    else
        x.right = put(x.right, key, value);
    recalculateSize(x);
    return x;
}
```

### 3. Analysis

The running time of binary search tree algorithms depends on the shape of the tree, and the tree shape depends on the order in which keys are inserted.

In the best case, the tree is perfectly balanced, and the distance from each empty link to the root is logN.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/c395a428-827c-405b-abd7-8a069316f583.jpg" width="200"/> </div><br>

In the worst case, the tree height is N.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/5ea609cb-8ad4-4c4c-aee6-45a40a81794a.jpg" width="200"/> </div><br>

### 4. floor()

floor(key): the largest key less than or equal to key

- If the key is less than the root key, then floor(key) must be in the left subtree;
- If the key is greater than the root key, first check whether floor(key) exists in the right subtree. If it exists, return it; otherwise, the root is floor(key).

```java
public Key floor(Key key) {
    Node x = floor(root, key);
    if (x == null)
        return null;
    return x.key;
}

private Node floor(Node x, Key key) {
    if (x == null)
        return null;
    int cmp = key.compareTo(x.key);
    if (cmp == 0)
        return x;
    if (cmp < 0)
        return floor(x.left, key);
    Node t = floor(x.right, key);
    return t != null ? t : x;
}
```

### 5. rank()

rank(key) returns the rank of key.

- If the key equals the root key, return the number of nodes in the left subtree;
- If it is smaller, recursively compute the rank in the left subtree;
- If it is larger, recursively compute the rank in the right subtree, plus the number of nodes in the left subtree, plus 1 for the root.

```java
@Override
public int rank(Key key) {
    return rank(key, root);
}

private int rank(Key key, Node x) {
    if (x == null)
        return 0;
    int cmp = key.compareTo(x.key);
    if (cmp == 0)
        return size(x.left);
    else if (cmp < 0)
        return rank(key, x.left);
    else
        return 1 + size(x.left) + rank(key, x.right);
}
```

### 6. min()

```java
@Override
public Key min() {
    return min(root).key;
}

private Node min(Node x) {
    if (x == null)
        return null;
    if (x.left == null)
        return x;
    return min(x.left);
}
```

### 7. deleteMin()

Make the link pointing to the minimum node point to the minimum node's right subtree.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/31b7e8de-ed11-4f69-b5fd-ba454120ac31.jpg" width="450"/> </div><br>

```java
public void deleteMin() {
    root = deleteMin(root);
}

public Node deleteMin(Node x) {
    if (x.left == null)
        return x.right;
    x.left = deleteMin(x.left);
    recalculateSize(x);
    return x;
}
```

### 8. delete()

- If the node to be deleted has only one subtree, simply make the link pointing to the node point to that only subtree;
- Otherwise, replace the node with the minimum node in its right subtree.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/23b9d625-ef28-42b5-bb22-d7aedd007e16.jpg" width="400"/> </div><br>

```java
public void delete(Key key) {
    root = delete(root, key);
}
private Node delete(Node x, Key key) {
    if (x == null)
        return null;
    int cmp = key.compareTo(x.key);
    if (cmp < 0)
        x.left = delete(x.left, key);
    else if (cmp > 0)
        x.right = delete(x.right, key);
    else {
        if (x.right == null)
            return x.left;
        if (x.left == null)
            return x.right;
        Node t = x;
        x = min(t.right);
        x.right = deleteMin(t.right);
        x.left = t.left;
    }
    recalculateSize(x);
    return x;
}
```

### 9. keys()

Use the property that inorder traversal of a binary search tree produces keys in increasing order.

```java
@Override
public List<Key> keys(Key l, Key h) {
    return keys(root, l, h);
}

private List<Key> keys(Node x, Key l, Key h) {
    List<Key> list = new ArrayList<>();
    if (x == null)
        return list;
    int cmpL = l.compareTo(x.key);
    int cmpH = h.compareTo(x.key);
    if (cmpL < 0)
        list.addAll(keys(x.left, l, h));
    if (cmpL <= 0 && cmpH >= 0)
        list.add(x.key);
    if (cmpH > 0)
        list.addAll(keys(x.right, l, h));
    return list;
}
```

### 10. Analysis

In the worst case, all operations on a binary search tree take time proportional to the tree height.

## 2-3 Search Trees

A 2-3 search tree introduces 2-nodes and 3-nodes to keep the tree balanced. In a perfectly balanced 2-3 search tree, all empty links should be the same distance from the root.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1097658b-c0e6-4821-be9b-25304726a11c.jpg" width="160px"/> </div><br>

### 1. Insertion

Insertion differs greatly from BST insertion. BST insertion first performs a missed search, then inserts the node at the corresponding empty link. If a 2-3 search tree did this, it would break balance. Instead, it inserts the new node into a leaf node.

Different cases are handled according to the type of leaf node:

- If inserting into a 2-node, directly combine the new node with the original node to form a 3-node.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/0c6f9930-8704-4a54-af23-19f9ca3e48b0.jpg" width="350"/> </div><br>

- If inserting into a 3-node, a temporary 4-node is created. The 4-node must be split into three 2-nodes, and the middle 2-node is moved up to the parent. If moving up continues to create a temporary 4-node, keep splitting and moving up until no temporary 4-node remains.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7002c01b-1ed5-475a-9e5f-5fc8a4cdbcc0.jpg" width="460"/> </div><br>

### 2. Properties

All transformations during insertion in a 2-3 search tree are local. Apart from the related nodes and links, no other part of the tree needs to be modified or checked, and these local transformations do not affect the tree's global ordering or balance.

The complexity of lookup and insertion in a 2-3 search tree is independent of insertion order. In the worst case, lookup and insertion must visit no more than logN nodes. A 2-3 search tree with 1 billion nodes needs to visit at most 30 nodes for any lookup or insertion.

## Red-Black Trees

A red-black tree is a 2-3 search tree, but it does not define 2-nodes and 3-nodes separately. Instead, it adds colors to nodes on top of an ordinary binary search tree. If the link pointing to a node is red, that node and its parent represent a 3-node; a black link is a normal link.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f1912ba6-6402-4321-9aa8-13d32fd121d1.jpg" width="240"/> </div><br>

Red-black trees have the following properties:

- Red links are all left links;
- Perfect black balance: every path from an empty link to the root has the same number of black links.

When drawing a red-black tree, red links can be drawn horizontally.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f5cb6028-425d-4939-91eb-cca9dd6b6c6c.jpg" width="220"/> </div><br>

```java
public class RedBlackBST<Key extends Comparable<Key>, Value> extends BST<Key, Value> {

    private static final boolean RED = true;
    private static final boolean BLACK = false;

    private boolean isRed(Node x) {
        if (x == null)
            return false;
        return x.color == RED;
    }
}
```

### 1. Left Rotation

Because valid red links are left links, if a right link is red, a left rotation is needed.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f4d534ab-0092-4a81-9e5b-ae889b9a72be.jpg" width="480"/> </div><br>

```java
public Node rotateLeft(Node h) {
    Node x = h.right;
    h.right = x.left;
    x.left = h;
    x.color = h.color;
    h.color = RED;
    x.N = h.N;
    recalculateSize(h);
    return x;
}
```

### 2. Right Rotation

Right rotation is used to transform two consecutive left red links, which will be discussed in the insertion process.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/63c8ffea-a9f2-4ebe-97d1-d71be71246f9.jpg" width="480"/> </div><br>

```java
public Node rotateRight(Node h) {
    Node x = h.left;
    h.left = x.right;
    x.right = h;
    x.color = h.color;
    h.color = RED;
    x.N = h.N;
    recalculateSize(h);
    return x;
}
```

### 3. Color Flip

In a red-black tree, a 4-node appears as a node whose left and right children are both red. Splitting a 4-node requires changing the child nodes from red to black and changing the parent node from black to red. From the perspective of a 2-3 tree, this moves the middle node up to the parent level.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/094b279a-b2db-4be7-87a3-b2a039c7448e.jpg" width="270"/> </div><br>

```java
void flipColors(Node h) {
    h.color = RED;
    h.left.color = BLACK;
    h.right.color = BLACK;
}
```

### 4. Insertion

First insert a node into the correct position using the binary search tree method, then perform the following color operations:

- If the right child is red and the left child is black, perform a left rotation;
- If the left child is red and the left child's left child is also red, perform a right rotation;
- If both left and right children are red, perform a color flip.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/4c457532-550b-4eca-b881-037b84b4934b.jpg" width="430"/> </div><br>

```java
@Override
public void put(Key key, Value value) {
    root = put(root, key, value);
    root.color = BLACK;
}

private Node put(Node x, Key key, Value value) {
    if (x == null) {
        Node node = new Node(key, value, 1);
        node.color = RED;
        return node;
    }
    int cmp = key.compareTo(x.key);
    if (cmp == 0)
        x.val = value;
    else if (cmp < 0)
        x.left = put(x.left, key, value);
    else
        x.right = put(x.right, key, value);

    if (isRed(x.right) && !isRed(x.left))
        x = rotateLeft(x);
    if (isRed(x.left) && isRed(x.left.left))
        x = rotateRight(x);
    if (isRed(x.left) && isRed(x.right))
        flipColors(x);

    recalculateSize(x);
    return x;
}
```

This insertion operation is similar to binary search tree insertion, with rotations and color changes added at the end.

The root node must be black because it has no parent node, so there is no left link from a parent node pointing to it. flipColors() may make the root node red. Each time the root changes from red to black, the tree's black-link height increases by 1.

### 5. Analysis

The height of a red-black tree of size N does not exceed 2logN. The worst case occurs when, in the corresponding 2-3 tree, all nodes on the leftmost path are 3-nodes and the rest are 2-nodes.

Most red-black tree operations take logarithmic time.

## Hash Tables

A hash table is similar to an array. The hash value in a hash table can be viewed as an array index. Accessing a hash table is as fast as accessing array elements, and lookup and insertion can be implemented in constant time.

Because key ordering cannot be determined from hash values, hash tables cannot implement ordered operations.

### 1. Hash Functions

For a hash table of size M, a hash function can convert any key into a positive integer in [0, M-1]. This integer is the hash value.

Hash tables have collisions, meaning two different keys may have the same hash value.

Hash functions should satisfy three conditions:

- Consistency: equal keys should have equal hash values. Two keys are equal when equals() returns true.
- Efficiency: computation should be simple. If necessary, cache the hash value and return it directly when the hash function is called.
- Uniformity: hash values of all keys should be uniformly distributed in [0, M-1]. If this condition is not met, many collisions may occur, reducing hash table performance.

The division method can hash integers into [0, M-1]. For example, for a positive integer k, k%M produces a hash value in [0, M-1]. Note that M is best chosen as a prime number; otherwise, not all information contained in the key can be used. For example, if M is 10<sup>k</sup>, only the last k digits of the key are used.

For other numbers, convert them into integer form and then use the division method. For example, for floating-point numbers, convert their binary representation into an integer.

For composite types with multiple parts, each part needs a hash value, and all of these hash values should have equal importance. To achieve this, treat the type as an R-base integer, where each part has a different weight.

For example, a string hash function is implemented as follows:

```java
int hash = 0;
for (int i = 0; i < s.length(); i++)
    hash = (R * hash + s.charAt(i)) % M;
```

Similarly, the hash function for a custom class with multiple members is:

```java
int hash = (((day * R + month) % M) * R + year) % M;
```

R is usually 31.

Java's hashCode() implements a hash function, but by default it uses the object's memory address. When using hashCode(), combine it with the division method. Because memory addresses are 32-bit integers and we only need a 31-bit nonnegative integer, mask out the sign bit before applying the division method.

```java
int hash = (x.hashCode() & 0x7fffffff) % M;
```

When using Java's built-in hash table implementations such as HashMap, only the hashCode() function for the Key type needs to be implemented. Java requires hashCode() to distribute keys uniformly across all 32-bit integers. hashCode() implementations for objects such as String and Integer satisfy this. The following shows how to implement hashCode() for a custom type:

```java
public class Transaction {

    private final String who;
    private final Date when;
    private final double amount;

    public Transaction(String who, Date when, double amount) {
        this.who = who;
        this.when = when;
        this.amount = amount;
    }

    public int hashCode() {
        int hash = 17;
        int R = 31;
        hash = R * hash + who.hashCode();
        hash = R * hash + when.hashCode();
        hash = R * hash + ((Double) amount).hashCode();
        return hash;
    }
}
```

### 2. Separate Chaining

Separate chaining uses linked lists to store keys with the same hash value, resolving collisions.

Lookup requires two steps: first find the linked list containing the key, then search sequentially within the list.

For N keys and M linked lists (N\>M), if the hash function satisfies uniformity, each linked list tends toward size N/M. Therefore, the number of comparisons required for missed lookups and insertions is about \~N/M.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/cbbfe06c-f0cb-47c4-bf7b-2780aebd98b2.png" width="330px"> </div><br>

### 3. Linear Probing

Linear probing uses empty slots to resolve collisions. When a collision occurs, it probes forward for an empty slot to store the colliding key.

When using linear probing, the array size M should be greater than the number of keys N (M\>N).


<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/0dbc4f7d-05c9-4aae-8065-7b7ea7e9709e.gif" width="350px"> </div><br>

```java
public class LinearProbingHashST<Key, Value> implements UnorderedST<Key, Value> {

    private int N = 0;
    private int M = 16;
    private Key[] keys;
    private Value[] values;

    public LinearProbingHashST() {
        init();
    }

    public LinearProbingHashST(int M) {
        this.M = M;
        init();
    }

    private void init() {
        keys = (Key[]) new Object[M];
        values = (Value[]) new Object[M];
    }

    private int hash(Key key) {
        return (key.hashCode() & 0x7fffffff) % M;
    }
}
```

##### 3.1 Search

```java
public Value get(Key key) {
    for (int i = hash(key); keys[i] != null; i = (i + 1) % M)
        if (keys[i].equals(key))
            return values[i];

    return null;
}
```

##### 3.2 Insertion

```java
public void put(Key key, Value value) {
    resize();
    putInternal(key, value);
}

private void putInternal(Key key, Value value) {
    int i;
    for (i = hash(key); keys[i] != null; i = (i + 1) % M)
        if (keys[i].equals(key)) {
            values[i] = value;
            return;
        }

    keys[i] = key;
    values[i] = value;
    N++;
}
```

##### 3.3 Deletion

Deletion should reinsert all adjacent key-value pairs to the right back into the hash table.

```java
public void delete(Key key) {
    int i = hash(key);
    while (keys[i] != null && !key.equals(keys[i]))
        i = (i + 1) % M;

    // Does not exist, return directly
    if (keys[i] == null)
        return;

    keys[i] = null;
    values[i] = null;

    // Reinsert the following connected key-value pairs
    i = (i + 1) % M;
    while (keys[i] != null) {
        Key keyToRedo = keys[i];
        Value valToRedo = values[i];
        keys[i] = null;
        values[i] = null;
        N--;
        putInternal(keyToRedo, valToRedo);
        i = (i + 1) % M;
    }
    N--;
    resize();
}
```

##### 3.5 Array Resizing

The cost of linear probing depends on the length of contiguous entries, also called clusters. When a cluster is long, lookup and insertion require many probes. For example, positions 2\~4 in the figure below form a cluster.


<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ace20410-f053-4c4a-aca4-2c603ff11bbe.png" width="340px"> </div><br>

α = N/M, and α is called the load factor. Theory shows that when α is less than 1/2, the expected number of probes is only between 1.5 and 2.5. To ensure hash table performance, adjust the array size so that α stays between [1/4, 1/2].

```java
private void resize() {
    if (N >= M / 2)
        resize(2 * M);
    else if (N <= M / 8)
        resize(M / 2);
}

private void resize(int cap) {
    LinearProbingHashST<Key, Value> t = new LinearProbingHashST<Key, Value>(cap);
    for (int i = 0; i < M; i++)
        if (keys[i] != null)
            t.putInternal(keys[i], values[i]);

    keys = t.keys;
    values = t.values;
    M = t.M;
}
```

## Summary

### 1. Symbol Table Algorithm Comparison

| Algorithm | Insert | Search | Ordered |
| :---: | :---: | :---: | :---: |
| Unordered symbol table implemented with linked list | N | N | yes |
| Ordered symbol table implemented with binary search | N | logN | yes |
| Binary search tree | logN | logN | yes |
| 2-3 search tree | logN | logN | yes |
| Hash table implemented with separate chaining | N/M | N/M | no |
| Hash table implemented with linear probing | 1 | 1 | no |

Prefer hash tables first. Use red-black trees when ordered operations are needed.

### 2. Java Symbol Table Implementations

- java.util.TreeMap: red-black tree
- java.util.HashMap: hash table with separate chaining

### 3. Sparse Vector Multiplication

When a vector is sparse, a symbol table can store the nonzero indexes and values in the vector, so multiplication only needs to process the nonzero elements.

```java
public class SparseVector {
    private HashMap<Integer, Double> hashMap;

    public SparseVector(double[] vector) {
        hashMap = new HashMap<>();
        for (int i = 0; i < vector.length; i++)
            if (vector[i] != 0)
                hashMap.put(i, vector[i]);
    }

    public double get(int i) {
        return hashMap.getOrDefault(i, 0.0);
    }

    public double dot(SparseVector other) {
        double sum = 0;
        for (int i : hashMap.keySet())
            sum += this.get(i) * other.get(i);
        return sum;
    }
}
```
