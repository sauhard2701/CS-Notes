# 39. Majority Element

[NowCoder](https://www.nowcoder.com/practice/e8a1b01a2df14cb2b228b30ee6a92163?tpId=13&tqId=11181&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Solution

This is a majority voting problem. The Boyer-Moore Majority Vote Algorithm can solve it with O(N) time complexity.

Use cnt to count occurrences of an element. When the traversed element equals the counted element, increment cnt; otherwise, decrement cnt. If the first i elements have been checked and cnt == 0, then the first i elements either have no majority element, or they have one whose count is less than i / 2, because cnt would not be 0 if the count were greater than i / 2. At this point, in the remaining n - i elements, the majority element still appears more than (n - i) / 2 times, so continuing the search can still find the majority element.

```java
public int MoreThanHalfNum_Solution(int[] nums) {
    int majority = nums[0];
    for (int i = 1, cnt = 1; i < nums.length; i++) {
        cnt = nums[i] == majority ? cnt + 1 : cnt - 1;
        if (cnt == 0) {
            majority = nums[i];
            cnt = 1;
        }
    }
    int cnt = 0;
    for (int val : nums)
        if (val == majority)
            cnt++;
    return cnt > nums.length / 2 ? majority : 0;
}
```
