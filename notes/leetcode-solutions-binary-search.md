# LeetCode Solutions - Binary Search
<!-- GFM-TOC -->
* [LeetCode Solutions - Binary Search](#leetcode-solutions---binary-search)
    * [1. Sqrt](#_1-sqrt)
    * [2. Smallest Letter Greater Than Target](#_2-smallest-letter-greater-than-target)
    * [3. Single Element in a Sorted Array](#_3-single-element-in-a-sorted-array)
    * [4. First Bad Version](#_4-first-bad-version)
    * [5. Minimum in Rotated Sorted Array](#_5-minimum-in-rotated-sorted-array)
    * [6. Search Range](#_6-search-range)
<!-- GFM-TOC -->


**Normal implementation**  

```text
Input : [1,2,3,4,5]
key : 3
return the index : 2
```

```java
public int binarySearch(int[] nums, int key) {
    int l = 0, h = nums.length - 1;
    while (l <= h) {
        int m = l + (h - l) / 2;
        if (nums[m] == key) {
            return m;
        } else if (nums[m] > key) {
            h = m - 1;
        } else {
            l = m + 1;
        }
    }
    return -1;
}
```

**Time Complexity**  

Binary search is also called half-interval search. It halves the search interval each time, so an algorithm with this halving property has time complexity O(logN).

**Calculating m**  

There are two ways to calculate the midpoint `m`:

- m = (l + h) / 2
- m = l + (h - l) / 2

`l + h` may overflow, meaning the sum exceeds the range representable by an integer. Since `l` and `h` are both positive, `h - l` does not have this overflow problem. Therefore, the second calculation method is preferred.

**Return Value for an Unsuccessful Search**  

If `key` still has not been found when the loop exits, the search has failed. There can be two return values:

- `-1`: use an error code to indicate that `key` was not found.
- `l`: the correct position to insert `key` into `nums`.

**Variants**  

Binary search has many variants. When implementing a variant, pay attention to boundary conditions. For example, the following implementation finds the leftmost position of `key` in an array with duplicate elements:

```java
public int binarySearch(int[] nums, int key) {
    int l = 0, h = nums.length;
    while (l < h) {
        int m = l + (h - l) / 2;
        if (nums[m] >= key) {
            h = m;
        } else {
            l = m + 1;
        }
    }
    return l;
}
```

This implementation differs from the normal implementation in the following ways:

- The assignment expression for `h` is `h = m`.
- The loop condition is `l \< h`.
- It returns `l` instead of `-1`.

When `nums[m] \>= key`, the leftmost `key` must be in the closed interval [l, m]. Therefore, `h` is assigned with `h = m`, because position `m` may also be the answer.

When `h` is assigned with `h = m`, using `l \<= h` as the loop condition can make the loop unable to exit, so the loop condition must be `l \< h`. The following example shows how the loop cannot exit when the condition is `l \<= h`:

```text
nums = {0, 1, 2}, key = 1
l   m   h
0   1   2  nums[m] >= key
0   0   1  nums[m] < key
1   1   1  nums[m] >= key
1   1   1  nums[m] >= key
...
```

When the loop exits, it does not mean `key` was not found, so the final result should not be `-1`. To verify whether it was found, the caller should check whether the value at the returned position equals `key`.

## 1. Sqrt

69\. Sqrt(x) (Easy)

[Leetcode](https://leetcode.com/problems/sqrtx/description/) / [LeetCode China](https://leetcode-cn.com/problems/sqrtx/description/)

```html
Input: 4
Output: 2

Input: 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since we want to return an integer, the decimal part will be truncated.
```

The square root `sqrt` of a number `x` must be between 0 and x, and satisfies `sqrt == x / sqrt`. Binary search can be used to search for `sqrt` between 0 and x.

For x = 8, its square root is 2.82842..., so the final result should be 2 rather than 3. When the loop condition is `l \<= h` and the loop exits, `h` is always 1 less than `l`; here `h = 2` and `l = 3`, so the final return value should be `h`, not `l`.

```java
public int mySqrt(int x) {
    if (x <= 1) {
        return x;
    }
    int l = 1, h = x;
    while (l <= h) {
        int mid = l + (h - l) / 2;
        int sqrt = x / mid;
        if (sqrt == mid) {
            return mid;
        } else if (mid > sqrt) {
            h = mid - 1;
        } else {
            l = mid + 1;
        }
    }
    return h;
}
```

## 2. Smallest Letter Greater Than Target

744\. Find Smallest Letter Greater Than Target (Easy)

[Leetcode](https://leetcode.com/problems/find-smallest-letter-greater-than-target/description/) / [LeetCode China](https://leetcode-cn.com/problems/find-smallest-letter-greater-than-target/description/)

```html
Input:
letters = ["c", "f", "j"]
target = "d"
Output: "f"

Input:
letters = ["c", "f", "j"]
target = "k"
Output: "c"
```

Problem description: given a sorted character array `letters` and a character `target`, find the smallest character in `letters` greater than `target`; if none exists, return the first character.

```java
public char nextGreatestLetter(char[] letters, char target) {
    int n = letters.length;
    int l = 0, h = n - 1;
    while (l <= h) {
        int m = l + (h - l) / 2;
        if (letters[m] <= target) {
            l = m + 1;
        } else {
            h = m - 1;
        }
    }
    return l < n ? letters[l] : letters[0];
}
```

## 3. Single Element in a Sorted Array

540\. Single Element in a Sorted Array (Medium)

[Leetcode](https://leetcode.com/problems/single-element-in-a-sorted-array/description/) / [LeetCode China](https://leetcode-cn.com/problems/single-element-in-a-sorted-array/description/)

```html
Input: [1, 1, 2, 3, 3, 4, 4, 8, 8]
Output: 2
```

Problem description: in a sorted array, only one number does not appear twice. Find that number.

The required time complexity is O(logN), so traversing the array and using XOR is not allowed because that would take O(N) time.

Let `index` be the position of the Single Element in the array. After `index`, the original paired pattern in the array changes. If `m` is even and `m + 1 \< index`, then `nums[m] == nums[m + 1]`; if `m + 1 \>= index`, then `nums[m] != nums[m + 1]`.

From this pattern, if `nums[m] == nums[m + 1]`, then `index` lies in [m + 2, h], so set `l = m + 2`. If `nums[m] != nums[m + 1]`, then `index` lies in [l, m], so set `h = m`.

Because `h` is assigned with `h = m`, the loop condition must use the form `l \< h`.

```java
public int singleNonDuplicate(int[] nums) {
    int l = 0, h = nums.length - 1;
    while (l < h) {
        int m = l + (h - l) / 2;
        if (m % 2 == 1) {
            m--;   // keep l/h/m on even positions so the search interval size is always odd
        }
        if (nums[m] == nums[m + 1]) {
            l = m + 2;
        } else {
            h = m;
        }
    }
    return nums[l];
}
```

## 4. First Bad Version

278\. First Bad Version (Easy)

[Leetcode](https://leetcode.com/problems/first-bad-version/description/) / [LeetCode China](https://leetcode-cn.com/problems/first-bad-version/description/)

Problem description: given an element `n` representing versions [1, 2, ..., n], bad versions start at position `x`, causing all later versions to be bad. You can call `isBadVersion(int x)` to determine whether a version is bad. Find the first bad version.

If version `m` is bad, the first bad version is between [l, m], so set `h = m`; otherwise, the first bad version is between [m + 1, h], so set `l = m + 1`.

Because `h` is assigned with `h = m`, the loop condition is `l \< h`.

```java
public int firstBadVersion(int n) {
    int l = 1, h = n;
    while (l < h) {
        int mid = l + (h - l) / 2;
        if (isBadVersion(mid)) {
            h = mid;
        } else {
            l = mid + 1;
        }
    }
    return l;
}
```

## 5. Minimum in Rotated Sorted Array

153\. Find Minimum in Rotated Sorted Array (Medium)

[Leetcode](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/) / [LeetCode China](https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array/description/)

```html
Input: [3,4,5,1,2],
Output: 1
```

```java
public int findMin(int[] nums) {
    int l = 0, h = nums.length - 1;
    while (l < h) {
        int m = l + (h - l) / 2;
        if (nums[m] <= nums[h]) {
            h = m;
        } else {
            l = m + 1;
        }
    }
    return nums[l];
}
```

## 6. Search Range

34\. Find First and Last Position of Element in Sorted Array

[Leetcode](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) / [LeetCode China](https://leetcode-cn.com/problems/find-first-and-last-position-of-element-in-sorted-array/)

```html
Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]

Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]
```

Problem description: given a sorted array `nums` and a target `target`, find the first and last positions of `target` in `nums`.

Binary search can find the first and last positions, but the search methods differ and would normally require two binary searches. Convert finding the last position of `target` into finding the first position of `target + 1`, then move one position backward. This way, only one binary-search implementation is needed.

```java
public int[] searchRange(int[] nums, int target) {
    int first = findFirst(nums, target);
    int last = findFirst(nums, target + 1) - 1;
    if (first == nums.length || nums[first] != target) {
        return new int[]{-1, -1};
    } else {
        return new int[]{first, Math.max(first, last)};
    }
}

private int findFirst(int[] nums, int target) {
    int l = 0, h = nums.length; // note the initial value of h
    while (l < h) {
        int m = l + (h - l) / 2;
        if (nums[m] >= target) {
            h = m;
        } else {
            l = m + 1;
        }
    }
    return l;
}
```

In the binary-search code for finding the first position, note that `h` is `nums.length`, not `nums.length - 1`. Consider the following example:

```
nums = [2,2], target = 2
```

If `h` is `nums.length - 1`, then `last = findFirst(nums, target + 1) - 1 = 1 - 1 = 0`. This is because `findLeft` only returns values in the range [0, nums.length - 1]. For `findFirst([2,2], 3)`, we want to return the position where 3 would be inserted into `nums`, which is one position after the last array element, namely `nums.length`. Therefore, `h` must be `nums.length`, making the return range of `findFirst` larger enough to cover the case where `target` is greater than the last element of `nums`.
