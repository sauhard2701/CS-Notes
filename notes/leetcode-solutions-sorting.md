# LeetCode Solutions - Sorting
<!-- GFM-TOC -->
* [LeetCode Solutions - Sorting](#leetcode-solutions---sorting)
    * [Quickselect](#quickselect)
    * [Heap](#heap)
        * [1. Kth Element](#1-kth-element)
    * [Bucket Sort](#bucket-sort)
        * [1. Top K Frequent Elements](#1-top-k-frequent-elements)
        * [2. Sort Characters by Frequency](#2-sort-characters-by-frequency)
    * [Dutch National Flag Problem](#dutch-national-flag-problem)
        * [1. Sort Colors](#1-sort-colors)
<!-- GFM-TOC -->


## Quickselect

Used to solve the **Kth Element** problem, that is, finding the Kth element.

It can be implemented with quicksort's `partition()`. The array must be shuffled first; otherwise, the worst-case time complexity is O(N<sup>2</sup>).

## Heap

Used to solve the **TopK Elements** problem, that is, finding the K smallest elements. To solve TopK with a heap, use a max heap. The heap top is the largest element in the current heap. Continuously insert new elements into the max heap; when the number of elements exceeds `k`, remove the heap top, which is the largest element in the current heap. The remaining elements are the K smallest among the elements added so far. Both insertion and removing the heap top take log<sub>2</sub>N time.

A heap can also solve the Kth Element problem. After obtaining a heap of size K, because it is implemented as a max heap, the heap top is the Kth largest element.

Quickselect can also solve the TopK Elements problem. After finding the Kth Element, traverse the array once more; all elements less than or equal to the Kth Element are TopK Elements.

So both quickselect and heap-based approaches can solve Kth Element and TopK Elements problems.

### 1. Kth Element

215\. Kth Largest Element in an Array (Medium)

[Leetcode](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) / [LeetCode China](https://leetcode-cn.com/problems/kth-largest-element-in-an-array/description/)

```text
Input: [3,2,1,5,6,4] and k = 2
Output: 5
```

Problem description: find the kth element from the end.

**Sorting**  : time complexity O(NlogN), space complexity O(1).

```java
public int findKthLargest(int[] nums, int k) {
    Arrays.sort(nums);
    return nums[nums.length - k];
}
```

**Heap**  : time complexity O(NlogK), space complexity O(K).

```java
public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> pq = new PriorityQueue<>(); // min heap
    for (int val : nums) {
        pq.add(val);
        if (pq.size() > k)  // maintain heap size K
            pq.poll();
    }
    return pq.peek();
}
```

**Quickselect**  : time complexity O(N), space complexity O(1).

```java
public int findKthLargest(int[] nums, int k) {
    k = nums.length - k;
    int l = 0, h = nums.length - 1;
    while (l < h) {
        int j = partition(nums, l, h);
        if (j == k) {
            break;
        } else if (j < k) {
            l = j + 1;
        } else {
            h = j - 1;
        }
    }
    return nums[k];
}

private int partition(int[] a, int l, int h) {
    int i = l, j = h + 1;
    while (true) {
        while (a[++i] < a[l] && i < h) ;
        while (a[--j] > a[l] && j > l) ;
        if (i >= j) {
            break;
        }
        swap(a, i, j);
    }
    swap(a, l, j);
    return j;
}

private void swap(int[] a, int i, int j) {
    int t = a[i];
    a[i] = a[j];
    a[j] = t;
}
```

## Bucket Sort

### 1. Top K Frequent Elements

347\. Top K Frequent Elements (Medium)

[Leetcode](https://leetcode.com/problems/top-k-frequent-elements/description/) / [LeetCode China](https://leetcode-cn.com/problems/top-k-frequent-elements/description/)

```html
Given [1,1,1,2,2,3] and k = 2, return [1,2].
```

Create several buckets. Each bucket stores numbers with the same frequency. The bucket index represents the frequency, so numbers stored in bucket `i` appear `i` times.

After placing all numbers into buckets, scan the buckets from back to front. The first `k` numbers obtained are the `k` most frequent numbers.

```java
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> frequencyForNum = new HashMap<>();
    for (int num : nums) {
        frequencyForNum.put(num, frequencyForNum.getOrDefault(num, 0) + 1);
    }
    List<Integer>[] buckets = new ArrayList[nums.length + 1];
    for (int key : frequencyForNum.keySet()) {
        int frequency = frequencyForNum.get(key);
        if (buckets[frequency] == null) {
            buckets[frequency] = new ArrayList<>();
        }
        buckets[frequency].add(key);
    }
    List<Integer> topK = new ArrayList<>();
    for (int i = buckets.length - 1; i >= 0 && topK.size() < k; i--) {
        if (buckets[i] == null) {
            continue;
        }
        if (buckets[i].size() <= (k - topK.size())) {
            topK.addAll(buckets[i]);
        } else {
            topK.addAll(buckets[i].subList(0, k - topK.size()));
        }
    }
    int[] res = new int[k];
    for (int i = 0; i < k; i++) {
        res[i] = topK.get(i);
    }
    return res;
}
```

### 2. Sort Characters by Frequency

451\. Sort Characters By Frequency (Medium)

[Leetcode](https://leetcode.com/problems/sort-characters-by-frequency/description/) / [LeetCode China](https://leetcode-cn.com/problems/sort-characters-by-frequency/description/)

```html
Input:
"tree"

Output:
"eert"

Explanation:
'e' appears twice while 'r' and 't' both appear once.
So 'e' must appear before both 'r' and 't'. Therefore "eetr" is also a valid answer.
```

```java
public String frequencySort(String s) {
    Map<Character, Integer> frequencyForNum = new HashMap<>();
    for (char c : s.toCharArray())
        frequencyForNum.put(c, frequencyForNum.getOrDefault(c, 0) + 1);

    List<Character>[] frequencyBucket = new ArrayList[s.length() + 1];
    for (char c : frequencyForNum.keySet()) {
        int f = frequencyForNum.get(c);
        if (frequencyBucket[f] == null) {
            frequencyBucket[f] = new ArrayList<>();
        }
        frequencyBucket[f].add(c);
    }
    StringBuilder str = new StringBuilder();
    for (int i = frequencyBucket.length - 1; i >= 0; i--) {
        if (frequencyBucket[i] == null) {
            continue;
        }
        for (char c : frequencyBucket[i]) {
            for (int j = 0; j < i; j++) {
                str.append(c);
            }
        }
    }
    return str.toString();
}
```

## Dutch National Flag Problem

The Dutch flag has three colors: red, white, and blue.

Given balls of three colors, the algorithm's goal is to arrange the balls in color order. It is essentially a variant of three-way partition quicksort. In three-way partition quicksort, each partition divides the array into three regions: less than the pivot, equal to the pivot, and greater than the pivot. This algorithm divides the array into three regions: red, white, and blue.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7a3215ec-6fb7-4935-8b0d-cb408208f7cb.png"/> </div><br>


### 1. Sort Colors

75\. Sort Colors (Medium)

[Leetcode](https://leetcode.com/problems/sort-colors/description/) / [LeetCode China](https://leetcode-cn.com/problems/sort-colors/description/)

```html
Input: [2,0,2,1,1,0]
Output: [0,0,1,1,2,2]
```

Problem description: there are only three colors, represented by 0, 1, and 2.

```java
public void sortColors(int[] nums) {
    int zero = -1, one = 0, two = nums.length;
    while (one < two) {
        if (nums[one] == 0) {
            swap(nums, ++zero, one++);
        } else if (nums[one] == 2) {
            swap(nums, --two, one);
        } else {
            ++one;
        }
    }
}

private void swap(int[] nums, int i, int j) {
    int t = nums[i];
    nums[i] = nums[j];
    nums[j] = t;
}
```
