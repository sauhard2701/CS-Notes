# Algorithms - Union Find
<!-- GFM-TOC -->
* [Algorithms - Union Find](#algorithms---union-find)
    * [Preface](#preface)
    * [Quick Find](#quick-find)
    * [Quick Union](#quick-union)
    * [Weighted Quick Union](#weighted-quick-union)
    * [Weighted Quick Union with Path Compression](#weighted-quick-union-with-path-compression)
    * [Comparison](#comparison)
<!-- GFM-TOC -->


## Preface

Used to solve dynamic connectivity problems. It can dynamically connect two points and determine whether two points are connected.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/02943a90-7dd4-4e9a-9325-f8217d3cc54d.jpg" width="350"/> </div><br>

| Method | Description |
| :---: | :---: |
| UF(int N) | Construct a union-find set of size N |
| void union(int p, int q) | Connect nodes p and q |
| int find(int p) | Find the connected component ID containing p |
| boolean connected(int p, int q) | Determine whether p and q are connected |

```java
public abstract class UF {

    protected int[] id;

    public UF(int N) {
        id = new int[N];
        for (int i = 0; i < N; i++) {
            id[i] = i;
        }
    }

    public boolean connected(int p, int q) {
        return find(p) == find(q);
    }

    public abstract int find(int p);

    public abstract void union(int p, int q);
}
```

## Quick Find

find operations are fast, meaning connectivity between two nodes can be determined quickly.

Ensure that all nodes in the same connected component have the same id value, then connectivity can be determined by checking whether two nodes have equal id values.

However, union operations are costly because the id values of all nodes in one connected component must be changed to the id value of another node.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/0972501d-f854-4d26-8fce-babb27c267f6.jpg" width="320"/> </div><br>

```java
public class QuickFindUF extends UF {

    public QuickFindUF(int N) {
        super(N);
    }


    @Override
    public int find(int p) {
        return id[p];
    }


    @Override
    public void union(int p, int q) {
        int pID = find(p);
        int qID = find(q);

        if (pID == qID) {
            return;
        }

        for (int i = 0; i < id.length; i++) {
            if (id[i] == pID) {
                id[i] = qID;
            }
        }
    }
}
```

## Quick Union

union operations are fast because only one node's id value needs to be changed.

However, find operations are expensive because nodes in the same connected component have different id values, and an id value only points to another node. Therefore, the search must keep moving upward until it reaches the top node.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/11b27de5-5a9d-45e4-95cc-417fa3ad1d38.jpg" width="280"/> </div><br>

```java
public class QuickUnionUF extends UF {

    public QuickUnionUF(int N) {
        super(N);
    }


    @Override
    public int find(int p) {
        while (p != id[p]) {
            p = id[p];
        }
        return p;
    }


    @Override
    public void union(int p, int q) {
        int pRoot = find(p);
        int qRoot = find(q);

        if (pRoot != qRoot) {
            id[pRoot] = qRoot;
        }
    }
}
```

This method makes union operations fast, but find operations are proportional to tree height. In the worst case, the tree height equals the number of nodes.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/23e4462b-263f-4d15-8805-529e0ca7a4d1.jpg" width="100"/> </div><br>

## Weighted Quick Union

To solve the problem that quick-union trees are often tall, weighted quick-union connects the smaller tree to the larger tree during union operations.

Theoretical research proves that the tree depth built by weighted quick-union is at most logN.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a9f18f8a-c1ea-422e-aa56-d91716b0f755.jpg" width="150"/> </div><br>

```java
public class WeightedQuickUnionUF extends UF {

    // Store node count information
    private int[] sz;


    public WeightedQuickUnionUF(int N) {
        super(N);
        this.sz = new int[N];
        for (int i = 0; i < N; i++) {
            this.sz[i] = 1;
        }
    }


    @Override
    public int find(int p) {
        while (p != id[p]) {
            p = id[p];
        }
        return p;
    }


    @Override
    public void union(int p, int q) {

        int i = find(p);
        int j = find(q);

        if (i == j) return;

        if (sz[i] < sz[j]) {
            id[i] = j;
            sz[j] += sz[i];
        } else {
            id[j] = i;
            sz[i] += sz[j];
        }
    }
}
```

## Weighted Quick Union with Path Compression

While checking nodes, link them directly to the root node. This only requires adding one loop in find.

## Comparison

| Algorithm | union | find |
| :---: | :---: | :---: |
| Quick Find | N | 1 |
| Quick Union | Tree height | Tree height |
| Weighted Quick Union | logN | logN |
| Weighted Quick Union with Path Compression | Very close to 1 | Very close to 1 |
