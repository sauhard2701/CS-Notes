# LeetCode Solutions - Hash Table
<!-- GFM-TOC -->
* [LeetCode Solutions - Hash Table](#leetcode-solutions---hash-table)
    * [1. Two Sum](#_1-two-sum)
    * [2. Contains Duplicate](#_2-contains-duplicate)
    * [3. Longest Harmonious Subsequence](#_3-longest-harmonious-subsequence)
    * [4. Longest Consecutive Sequence](#_4-longest-consecutive-sequence)
<!-- GFM-TOC -->


Hash tables store data with O(N) space complexity and solve problems with O(1) time complexity.

- In Java,   **HashSet**   is used to store a set and can check whether an element is in the set. If the elements are finite and the range is not large, a boolean array can be used to store whether an element exists. For example, for elements containing only lowercase letters, a boolean array of length 26 can store a character set, reducing space complexity to O(1).

 In Java,   **HashMap**   is mainly used for mappings, linking two elements together. HashMap can also be used to count elements, where the key is the element and the value is the count. Similar to HashSet, if the elements are finite and the range is not large, an integer array can be used for counting. When compressing or otherwise transforming content, HashMap can link the original content and the transformed content. For example, in a URL shortening system:

[Leetcode](https://leetcode.com/problems/encode-and-decode-tinyurl/description/) / [LeetCode China](https://leetcode-cn.com/problems/encode-and-decode-tinyurl/description/) uses HashMap to store mappings from shortened URLs to original URLs, so the system can display shortened URLs and retrieve the original URL from a shortened URL to locate the correct resource.


## 1. Two Sum

1\. Two Sum (Easy)

[Leetcode](https://leetcode.com/problems/two-sum/description/) / [LeetCode China](https://leetcode-cn.com/problems/two-sum/description/)

You can first sort the array, then use the two-pointer method or binary search. This gives O(NlogN) time complexity and O(1) space complexity.

Use a HashMap to store the mapping from array elements to indices. When visiting nums[i], check whether target - nums[i] exists in the HashMap. If it does, the index of target - nums[i] and i are the two numbers to find. This method has O(N) time complexity and O(N) space complexity, trading space for time.

```java
public int[] twoSum(int[] nums, int target) {
    HashMap<Integer, Integer> indexForNum = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        if (indexForNum.containsKey(target - nums[i])) {
            return new int[]{indexForNum.get(target - nums[i]), i};
        } else {
            indexForNum.put(nums[i], i);
        }
    }
    return null;
}
```

## 2. Contains Duplicate

217\. Contains Duplicate (Easy)

[Leetcode](https://leetcode.com/problems/contains-duplicate/description/) / [LeetCode China](https://leetcode-cn.com/problems/contains-duplicate/description/)

```java
public boolean containsDuplicate(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int num : nums) {
        set.add(num);
    }
    return set.size() < nums.length;
}
```

## 3. Longest Harmonious Subsequence

594\. Longest Harmonious Subsequence (Easy)

[Leetcode](https://leetcode.com/problems/longest-harmonious-subsequence/description/) / [LeetCode China](https://leetcode-cn.com/problems/longest-harmonious-subsequence/description/)

```html
Input: [1,3,2,2,5,2,3,7]
Output: 5
Explanation: The longest harmonious subsequence is [3,2,2,2,3].
```

In a harmonious subsequence, the difference between the maximum and minimum values is exactly 1. Note that the elements of the subsequence do not have to be contiguous elements in the array.

```java
public int findLHS(int[] nums) {
    Map<Integer, Integer> countForNum = new HashMap<>();
    for (int num : nums) {
        countForNum.put(num, countForNum.getOrDefault(num, 0) + 1);
    }
    int longest = 0;
    for (int num : countForNum.keySet()) {
        if (countForNum.containsKey(num + 1)) {
            longest = Math.max(longest, countForNum.get(num + 1) + countForNum.get(num));
        }
    }
    return longest;
}
```

## 4. Longest Consecutive Sequence

128\. Longest Consecutive Sequence (Hard)

[Leetcode](https://leetcode.com/problems/longest-consecutive-sequence/description/) / [LeetCode China](https://leetcode-cn.com/problems/longest-consecutive-sequence/description/)

```html
Given [100, 4, 200, 1, 3, 2],
The longest consecutive elements sequence is [1, 2, 3, 4]. Return its length: 4.
```

The problem requires an O(N) time complexity solution.

```java
public int longestConsecutive(int[] nums) {
    Map<Integer, Integer> countForNum = new HashMap<>();
    for (int num : nums) {
        countForNum.put(num, 1);
    }
    for (int num : nums) {
        forward(countForNum, num);
    }
    return maxCount(countForNum);
}

private int forward(Map<Integer, Integer> countForNum, int num) {
    if (!countForNum.containsKey(num)) {
        return 0;
    }
    int cnt = countForNum.get(num);
    if (cnt > 1) {
        return cnt;
    }
    cnt = forward(countForNum, num + 1) + 1;
    countForNum.put(num, cnt);
    return cnt;
}

private int maxCount(Map<Integer, Integer> countForNum) {
    int max = 0;
    for (int num : countForNum.keySet()) {
        max = Math.max(max, countForNum.get(num));
    }
    return max;
}
```
