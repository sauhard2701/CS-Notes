# Algorithms - Sorting
## Conventions

Elements to be sorted need to implement Java's Comparable interface. This interface provides compareTo(), which can be used to compare two elements.

Use helper functions less() and swap() for comparison and exchange operations, making the code more readable and portable.

The cost model for sorting algorithms is the number of comparisons and exchanges.

```java
public abstract class Sort<T extends Comparable<T>> {

    public abstract void sort(T[] nums);

    protected boolean less(T v, T w) {
        return v.compareTo(w) < 0;
    }

    protected void swap(T[] a, int i, int j) {
        T t = a[i];
        a[i] = a[j];
        a[j] = t;
    }
}
```

## Selection Sort

Select the smallest element from the array and swap it with the first element. Then select the smallest element from the remaining elements and swap it with the second element. Repeat this process until the entire array is sorted.

Selection sort requires about \~N<sup>2</sup>/2 comparisons and \~N exchanges. Its running time is independent of the input, which means it performs the same number of comparisons and exchanges even on an already sorted array.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/bc6be2d0-ed5e-4def-89e5-3ada9afa811a.gif" width="230px"> </div><br>

```java
public class Selection<T extends Comparable<T>> extends Sort<T> {

    @Override
    public void sort(T[] nums) {
        int N = nums.length;
        for (int i = 0; i < N - 1; i++) {
            int min = i;
            for (int j = i + 1; j < N; j++) {
                if (less(nums[j], nums[min])) {
                    min = j;
                }
            }
            swap(nums, i, min);
        }
    }
}
```

## Bubble Sort

Repeatedly swap adjacent inverted elements from left to right. After one pass, the largest unsorted element bubbles up to the right side.

If no exchange occurs in one pass, the array is already sorted and the algorithm can exit directly.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/0f8d178b-52d8-491b-9dfd-41e05a952578.gif" width="200px"> </div><br>

```java
public class Bubble<T extends Comparable<T>> extends Sort<T> {

    @Override
    public void sort(T[] nums) {
        int N = nums.length;
        boolean isSorted = false;
        for (int i = N - 1; i > 0 && !isSorted; i--) {
            isSorted = true;
            for (int j = 0; j < i; j++) {
                if (less(nums[j + 1], nums[j])) {
                    isSorted = false;
                    swap(nums, j, j + 1);
                }
            }
        }
    }
}
```

## Insertion Sort

Each time, insert the current element into the already sorted array on the left, keeping the left-side array sorted after insertion.

For the array {3, 5, 2, 4, 1}, the inversions are: (3, 2), (3, 1), (5, 2), (5, 4), (5, 1), (2, 1), and (4, 1). Insertion sort can only swap adjacent elements each time, reducing the number of inversions by 1, so the number of exchanges required by insertion sort equals the number of inversions.

The time complexity of insertion sort depends on the initial order of the array. If the array is already partially ordered, there are fewer inversions, fewer exchanges are needed, and the time complexity is lower.

- On average, insertion sort requires \~N<sup>2</sup>/4 comparisons and \~N<sup>2</sup>/4 exchanges;
- In the worst case, it requires \~N<sup>2</sup>/2 comparisons and \~N<sup>2</sup>/2 exchanges. The worst case is when the array is in reverse order;
- In the best case, it requires N-1 comparisons and 0 exchanges. The best case is when the array is already sorted.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/35253fa4-f60a-4e3b-aaec-8fc835aabdac.gif" width="200px"> </div><br>

```java
public class Insertion<T extends Comparable<T>> extends Sort<T> {

    @Override
    public void sort(T[] nums) {
        int N = nums.length;
        for (int i = 1; i < N; i++) {
            for (int j = i; j > 0 && less(nums[j], nums[j - 1]); j--) {
                swap(nums, j, j - 1);
            }
        }
    }
}
```

## Shell Sort

For large arrays, insertion sort is slow because it can only swap adjacent elements, reducing the inversion count by only 1 each time. Shell sort addresses this limitation by swapping non-adjacent elements, reducing the inversion count by more than 1 each time.

Shell sort uses insertion sort to sort sequences with interval h. By continually decreasing h until h=1, the entire array becomes sorted.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7818c574-97a8-48db-8e62-8bfb030b02ba.png" width="450px"> </div><br>

```java
public class Shell<T extends Comparable<T>> extends Sort<T> {

    @Override
    public void sort(T[] nums) {

        int N = nums.length;
        int h = 1;

        while (h < N / 3) {
            h = 3 * h + 1; // 1, 4, 13, 40, ...
        }

        while (h >= 1) {
            for (int i = h; i < N; i++) {
                for (int j = i; j >= h && less(nums[j], nums[j - h]); j -= h) {
                    swap(nums, j, j - h);
                }
            }
            h = h / 3;
        }
    }
}

```

Shell sort's running time does not reach quadratic complexity. With the increment sequence 1, 4, 13, 40, ..., the number of comparisons does not exceed a small multiple of N times the length of the increment sequence. The advanced sorting algorithms introduced later are only about twice as fast as Shell sort.

## Merge Sort

The idea of merge sort is to divide the array into two parts, sort each part separately, and then merge them.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ec840967-d127-4da3-b6bb-186996c56746.png" width="300px"> </div><br>

### 1. Merge Procedure

The merge procedure merges two already sorted parts of an array into one.

```java
public abstract class MergeSort<T extends Comparable<T>> extends Sort<T> {

    protected T[] aux;


    protected void merge(T[] nums, int l, int m, int h) {

        int i = l, j = m + 1;

        for (int k = l; k <= h; k++) {
            aux[k] = nums[k]; // copy data to the auxiliary array
        }

        for (int k = l; k <= h; k++) {
            if (i > m) {
                nums[k] = aux[j++];

            } else if (j > h) {
                nums[k] = aux[i++];

            } else if (aux[i].compareTo(aux[j]) <= 0) {
                nums[k] = aux[i++]; // do this first to preserve stability

            } else {
                nums[k] = aux[j++];
            }
        }
    }
}
```

### 2. Top-Down Merge Sort

Divide a large array into two smaller arrays and solve them.

Because the problem is split in half into two subproblems each time, this divide-in-half algorithm usually has complexity O(NlogN).

```java
public class Up2DownMergeSort<T extends Comparable<T>> extends MergeSort<T> {

    @Override
    public void sort(T[] nums) {
        aux = (T[]) new Comparable[nums.length];
        sort(nums, 0, nums.length - 1);
    }

    private void sort(T[] nums, int l, int h) {
        if (h <= l) {
            return;
        }
        int mid = l + (h - l) / 2;
        sort(nums, l, mid);
        sort(nums, mid + 1, h);
        merge(nums, l, mid, h);
    }
}
```


### 3. Bottom-Up Merge Sort

First merge tiny arrays, then merge the resulting tiny arrays pairwise.

```java
public class Down2UpMergeSort<T extends Comparable<T>> extends MergeSort<T> {

    @Override
    public void sort(T[] nums) {

        int N = nums.length;
        aux = (T[]) new Comparable[N];

        for (int sz = 1; sz < N; sz += sz) {
            for (int lo = 0; lo < N - sz; lo += sz + sz) {
                merge(nums, lo, lo + sz - 1, Math.min(lo + sz + sz - 1, N - 1));
            }
        }
    }
}

```

## Quicksort

### 1. Basic Algorithm

- Merge sort divides the array into two subarrays, sorts them separately, and merges the ordered subarrays so the entire array is sorted;
- Quicksort divides the array into two subarrays using a pivot element. The left subarray is less than or equal to the pivot, and the right subarray is greater than or equal to the pivot. Sorting these two subarrays sorts the entire array.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/6234eb3d-ccf2-4987-a724-235aef6957b1.png" width="280px"> </div><br>

```java
public class QuickSort<T extends Comparable<T>> extends Sort<T> {

    @Override
    public void sort(T[] nums) {
        shuffle(nums);
        sort(nums, 0, nums.length - 1);
    }

    private void sort(T[] nums, int l, int h) {
        if (h <= l)
            return;
        int j = partition(nums, l, h);
        sort(nums, l, j - 1);
        sort(nums, j + 1, h);
    }

    private void shuffle(T[] nums) {
        List<Comparable> list = Arrays.asList(nums);
        Collections.shuffle(list);
        list.toArray(nums);
    }
}
```

### 2. Partitioning

Use a[l] as the pivot. Scan from the left end of the array to the right until finding the first element greater than or equal to it, then scan from the right end to the left until finding the first element smaller than it, and swap these two elements. Repeating this process ensures that elements to the left of pointer i are not greater than the pivot and elements to the right of pointer j are not smaller than the pivot. When the two pointers meet, swap the pivot a[l] with a[j].

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/c4859290-e27d-4f12-becf-e2a5c1f3a275.gif" width="320px"> </div><br>

```java
private int partition(T[] nums, int l, int h) {
    int i = l, j = h + 1;
    T v = nums[l];
    while (true) {
        while (less(nums[++i], v) && i != h) ;
        while (less(v, nums[--j]) && j != l) ;
        if (i >= j)
            break;
        swap(nums, i, j);
    }
    swap(nums, l, j);
    return j;
}
```

### 3. Performance Analysis

Quicksort is an in-place sort and does not need an auxiliary array, but recursive calls require an auxiliary stack.

In the best case, quicksort divides the array exactly in half every time, minimizing the number of recursive calls. In this case, the number of comparisons is C<sub>N</sub>=2C<sub>N/2</sub>+N, and the complexity is O(NlogN).

In the worst case, the first partition uses the smallest element, the second partition uses the second smallest element, and so on. Therefore, the worst case requires N<sup>2</sup>/2 comparisons. To avoid the array being initially ordered, shuffle the array randomly before quicksort.

### 4. Algorithm Improvements

##### 4.1 Switch to Insertion Sort

Because quicksort recursively calls itself even on small arrays, and insertion sort performs better on small arrays, the algorithm can switch to insertion sort for small arrays.

##### 4.2 Median-of-Three

The best case is choosing the median of the array as the pivot each time, but computing the median is expensive. A compromise is to take 3 elements and use the median among them as the pivot.

##### 4.3 3-Way Partitioning

For arrays with many duplicate elements, partition the array into three parts corresponding to elements less than, equal to, and greater than the pivot.

Three-way partitioning quicksort can sort random arrays with many duplicate elements in linear time.

```java
public class ThreeWayQuickSort<T extends Comparable<T>> extends QuickSort<T> {

    @Override
    protected void sort(T[] nums, int l, int h) {
        if (h <= l) {
            return;
        }
        int lt = l, i = l + 1, gt = h;
        T v = nums[l];
        while (i <= gt) {
            int cmp = nums[i].compareTo(v);
            if (cmp < 0) {
                swap(nums, lt++, i++);
            } else if (cmp > 0) {
                swap(nums, i, gt--);
            } else {
                i++;
            }
        }
        sort(nums, l, lt - 1);
        sort(nums, gt + 1, h);
    }
}
```

### 5. Partition-Based Quickselect

The partition() method in quicksort returns an integer j such that a[l..j-1] is less than or equal to a[j] and a[j+1..h] is greater than or equal to a[j]. At this point, a[j] is the jth largest element in the array.

This property can be used to find the kth element of the array.

This algorithm is linear. Assuming the array can be split in half each time, the total number of comparisons is (N+N/2+N/4+...) until the kth element is found, and this sum is clearly less than 2N.

```java
public T select(T[] nums, int k) {
    int l = 0, h = nums.length - 1;
    while (h > l) {
        int j = partition(nums, l, h);

        if (j == k) {
            return nums[k];

        } else if (j > k) {
            h = j - 1;

        } else {
            l = j + 1;
        }
    }
    return nums[k];
}
```

## Heap Sort

### 1. Heap

In a heap, the value of a node is always greater than or equal to, or less than or equal to, the values of its child nodes, and the heap is a complete binary tree.

A heap can be represented with an array because it is a complete binary tree, and complete binary trees are easy to store in arrays. The parent of the node at position k is at k/2, and its two children are at 2k and 2k+1. Array index 0 is not used here to make the node position relationship clearer.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f48883c8-9d8a-494e-99a4-317d8ddb8552.png" width="170px"> </div><br>

```java
public class Heap<T extends Comparable<T>> {

    private T[] heap;
    private int N = 0;

    public Heap(int maxN) {
        this.heap = (T[]) new Comparable[maxN + 1];
    }

    public boolean isEmpty() {
        return N == 0;
    }

    public int size() {
        return N;
    }

    private boolean less(int i, int j) {
        return heap[i].compareTo(heap[j]) < 0;
    }

    private void swap(int i, int j) {
        T t = heap[i];
        heap[i] = heap[j];
        heap[j] = t;
    }
}
```

### 2. Swim and Sink

In a heap, when a node is larger than its parent, the two nodes need to be swapped. After the swap, it may still be larger than its new parent, so comparison and exchange continue. This operation is called swim.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/99d5e84e-fc2a-49a3-8259-8de274617756.gif" width="270px"> </div><br>

```java
private void swim(int k) {
    while (k > 1 && less(k / 2, k)) {
        swap(k / 2, k);
        k = k / 2;
    }
}
```

Similarly, when a node is smaller than its child, it needs to continue comparing and exchanging downward. This operation is called sink. If a node has two children, it should be swapped with the larger child.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/4bf5e3fb-a285-4138-b3b6-780956eb1df1.gif" width="270px"> </div><br>

```java
private void sink(int k) {
    while (2 * k <= N) {
        int j = 2 * k;
        if (j < N && less(j, j + 1))
            j++;
        if (!less(k, j))
            break;
        swap(k, j);
        k = j;
    }
}
```

### 3. Insert Element

Place the new element at the end of the array and swim it to the appropriate position.

```java
public void insert(Comparable v) {
    heap[++N] = v;
    swim(N);
}
```

### 4. Delete Maximum

Delete the largest element from the top of the array, move the last element to the top, and sink this element to the appropriate position.

```java
public T delMax() {
    T max = heap[1];
    swap(1, N--);
    heap[N + 1] = null;
    sink(1);
    return max;
}
```

### 5. Heap Sort

Swap the largest element with the last element in the current heap array without deleting it. This produces a decreasing sequence from back to front, which is an increasing sequence when viewed from front to back. This is heap sort.

##### 5.1 Build Heap

The most direct way to build a heap from an unordered array is to traverse the array from left to right and perform swim operations. A more efficient approach is to traverse from right to left and perform sink operations. If a node's two children are already heap-ordered, sinking that node can make the heap rooted at that node heap-ordered. Leaf nodes do not need sinking, so leaf elements can be ignored and only half the elements need to be traversed.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/c2ca8dd2-8d00-4a3e-bece-db7849ac9cfd.gif" width="210px"> </div><br>

##### 5.2 Swap Root with Last Element

After swapping, a sink operation is needed to maintain heap order.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/d156bcda-ac8d-4324-95e0-0c8df41567c9.gif" width="250px"> </div><br>

```java
public class HeapSort<T extends Comparable<T>> extends Sort<T> {
    /**
     * Array position 0 must not contain an element
     */
    @Override
    public void sort(T[] nums) {
        int N = nums.length - 1;
        for (int k = N / 2; k >= 1; k--)
            sink(nums, k, N);

        while (N > 1) {
            swap(nums, 1, N--);
            sink(nums, 1, N);
        }
    }

    private void sink(T[] nums, int k, int N) {
        while (2 * k <= N) {
            int j = 2 * k;
            if (j < N && less(nums, j, j + 1))
                j++;
            if (!less(nums, k, j))
                break;
            swap(nums, k, j);
            k = j;
        }
    }

    private boolean less(T[] nums, int i, int j) {
        return nums[i].compareTo(nums[j]) < 0;
    }
}
```

### 6. Analysis

The height of a heap is logN, so inserting an element into a heap and deleting the maximum element both have complexity logN.

For heap sort, because N nodes need to be sunk, the complexity is NlogN.

Heap sort is an in-place sort and does not use extra space.

Modern operating systems rarely use heap sort because it cannot take advantage of locality for caching; array elements are rarely compared and exchanged with adjacent elements.

## Summary

### 1. Sorting Algorithm Comparison

| Algorithm | Stability | Time Complexity | Space Complexity | Notes |
| :---: | :---: |:---: | :---: | :---: |
| Selection sort | × | N<sup>2</sup> | 1 | |
| Bubble sort | √ |  N<sup>2</sup> | 1 | |
| Insertion sort | √ |  N \~ N<sup>2</sup> | 1 | Time complexity depends on the initial order |
| Shell sort | ×  |  Several times N multiplied by the length of the increment sequence | 1 | Improved insertion sort |
| Quicksort | ×  | NlogN | logN | |
| Three-way partitioning quicksort | ×  |  N \~ NlogN | logN | Suitable for many duplicate keys |
| Merge sort | √ |  NlogN | N | |
| Heap sort | ×  |  NlogN | 1 | Cannot take advantage of locality |

Quicksort is the fastest general-purpose sorting algorithm. Its inner loop has very few instructions, and it can use the cache because it always accesses data sequentially. Its running time is approximately \~cNlogN, where c is smaller than in other linearithmic sorting algorithms.

With three-way partitioning quicksort, some input distributions that may occur in real applications can be sorted in linear time, while other sorting algorithms still require linearithmic time.

### 2. Java Sorting Implementations

Java's main sorting method is java.util.Arrays.sort(). It uses three-way partitioning quicksort for primitive data types and merge sort for reference types.
