# 40. Smallest K Numbers

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/6a296eb82cf844ca8539b57c23e6e9bf?tpId=13&tqId=11182&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Solution

### Min Heap of Size K

- Complexity: O(NlogK) + O(K)
- Especially suitable for processing massive data sets.

The process of maintaining the smallest K elements is as follows: use a max heap. After adding an element, if the max heap size exceeds K, remove the heap top, which is the largest element in the current heap. This keeps all remaining heap elements smaller than the removed element.

Use a max heap to maintain the smallest elements. Do not directly create a min heap with a fixed size and expect the elements in it to be the smallest ones.

Java's PriorityQueue provides heap functionality. By default, PriorityQueue is a min heap; a max heap can be implemented during initialization with the Lambda expression (o1, o2) -\> o2 - o1. Other languages have similar heap data structures.

```java
public ArrayList<Integer> GetLeastNumbers_Solution(int[] nums, int k) {
    if (k > nums.length || k <= 0)
        return new ArrayList<>();
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>((o1, o2) -> o2 - o1);
    for (int num : nums) {
        maxHeap.add(num);
        if (maxHeap.size() > k)
            maxHeap.poll();
    }
    return new ArrayList<>(maxHeap);
}
```

### Quickselect

- Complexity: O(N) + O(1)
- Can only be used when modifying array elements is allowed.

The partition() method in quicksort returns an integer j such that a[l..j-1] is less than or equal to a[j], and a[j+1..h] is greater than or equal to a[j]. At this point, a[j] is the jth largest element in the array. This property can be used to find the Kth element in the array; this algorithm is called quickselect.

```java
public ArrayList<Integer> GetLeastNumbers_Solution(int[] nums, int k) {
    ArrayList<Integer> ret = new ArrayList<>();
    if (k > nums.length || k <= 0)
        return ret;
    findKthSmallest(nums, k - 1);
    /* findKthSmallest modifies the array so that the first k numbers are the smallest k numbers */
    for (int i = 0; i < k; i++)
        ret.add(nums[i]);
    return ret;
}

public void findKthSmallest(int[] nums, int k) {
    int l = 0, h = nums.length - 1;
    while (l < h) {
        int j = partition(nums, l, h);
        if (j == k)
            break;
        if (j > k)
            h = j - 1;
        else
            l = j + 1;
    }
}

private int partition(int[] nums, int l, int h) {
    int p = nums[l];     /* Partition element */
    int i = l, j = h + 1;
    while (true) {
        while (i != h && nums[++i] < p) ;
        while (j != l && nums[--j] > p) ;
        if (i >= j)
            break;
        swap(nums, i, j);
    }
    swap(nums, l, j);
    return j;
}

private void swap(int[] nums, int i, int j) {
    int t = nums[i];
    nums[i] = nums[j];
    nums[j] = t;
}
```
