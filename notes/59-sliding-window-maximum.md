# 59. Sliding Window Maximum

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/1624bc35a45c42c0bc17d17fa0cba788?tpId=13&tqId=11217&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Given an array and a sliding window size, find the maximum value in every sliding window.

For example, if the input array is {2, 3, 4, 2, 6, 2, 5, 1} and the sliding window size is 3, there are 6 sliding windows in total, and their maximum values are {4, 4, 6, 6, 6, 5}.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20201104020702453.png" width="500px"> </div><br>

## Solution

Maintain a max heap whose size equals the window size; the heap top is the maximum value in the current window.

Assume the window size is M and the array length is N. When the window moves right, the element leaving the window must first be removed from the heap, and the newly arriving element must be added to the heap. Both operations have time complexity log<sub>2</sub>M, so the algorithm time complexity is O(Nlog<sub>2</sub>M), and the space complexity is O(M).

```java
public ArrayList<Integer> maxInWindows(int[] num, int size) {
    ArrayList<Integer> ret = new ArrayList<>();
    if (size > num.length || size < 1)
        return ret;
    PriorityQueue<Integer> heap = new PriorityQueue<>((o1, o2) -> o2 - o1);  /* Max heap */
    for (int i = 0; i < size; i++)
        heap.add(num[i]);
    ret.add(heap.peek());
    for (int i = 0, j = i + size; j < num.length; i++, j++) {            /* Maintain a max heap of size */
        heap.remove(num[i]);
        heap.add(num[j]);
        ret.add(heap.peek());
    }
    return ret;
}
```
