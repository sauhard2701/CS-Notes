# LeetCode Solutions - Two Pointers
<!-- GFM-TOC -->
* [LeetCode Solutions - Two Pointers](#leetcode-solutions---two-pointers)
    * [1. Two Sum II: Input Array Is Sorted](#1-two-sum-ii-input-array-is-sorted)
    * [2. Sum of Square Numbers](#2-sum-of-square-numbers)
    * [3. Reverse Vowels of a String](#3-reverse-vowels-of-a-string)
    * [4. Valid Palindrome II](#4-valid-palindrome-ii)
    * [5. Merge Sorted Array](#5-merge-sorted-array)
    * [6. Linked List Cycle](#6-linked-list-cycle)
    * [7. Longest Word in Dictionary through Deleting](#7-longest-word-in-dictionary-through-deleting)
<!-- GFM-TOC -->


Two pointers are mainly used to traverse arrays. The two pointers point to different elements and work together to complete the task.

## 1. Two Sum II: Input Array Is Sorted

167\. Two Sum II - Input array is sorted (Easy)

[Leetcode](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/) / [LeetCode China](https://leetcode-cn.com/problems/two-sum-ii-input-array-is-sorted/description/)

```html
Input: numbers={2, 7, 11, 15}, target=9
Output: index1=1, index2=2
```

Problem description: find two numbers in a sorted array whose sum equals `target`.

Use two pointers: one points to the smaller element, and the other points to the larger element. The pointer to the smaller element traverses from front to back, while the pointer to the larger element traverses from back to front.

- If the sum of the two pointed elements is `sum == target`, the required result has been found.
- If `sum \> target`, move the larger element so `sum` becomes smaller.
- If `sum \< target`, move the smaller element so `sum` becomes larger.

Each array element is traversed at most once, so the time complexity is O(N). Only two extra variables are used, so the space complexity is O(1).

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/437cb54c-5970-4ba9-b2ef-2541f7d6c81e.gif" width="200px"> </div><br>

```java
public int[] twoSum(int[] numbers, int target) {
    if (numbers == null) return null;
    int i = 0, j = numbers.length - 1;
    while (i < j) {
        int sum = numbers[i] + numbers[j];
        if (sum == target) {
            return new int[]{i + 1, j + 1};
        } else if (sum < target) {
            i++;
        } else {
            j--;
        }
    }
    return null;
}
```

## 2. Sum of Square Numbers

633\. Sum of Square Numbers (Easy)

[Leetcode](https://leetcode.com/problems/sum-of-square-numbers/description/) / [LeetCode China](https://leetcode-cn.com/problems/sum-of-square-numbers/description/)

```html
Input: 5
Output: True
Explanation: 1 * 1 + 2 * 2 = 5
```

Problem description: determine whether a non-negative integer is the sum of squares of two integers.

This can be viewed as searching for two numbers in the sorted array 0\~target such that the sum of their squares is `target`. If such numbers are found, return `true`, meaning `target` is the sum of squares of two integers.

This problem is similar to 167. Two Sum II - Input array is sorted, with one clear difference: one asks for a sum of `target`, while this one asks for a square sum of `target`. Two pointers can likewise be used to find the two numbers.

The key is initializing the right pointer to prune the search and reduce time complexity. Let the right pointer be `x` and the left pointer be fixed at 0. To make 0<sup>2</sup> + x<sup>2</sup> as close to `target` as possible, choose `x` as sqrt(target).

Because only 0\~sqrt(target) needs to be traversed at most once, the time complexity is O(sqrt(target)). Since only two extra variables are used, the space complexity is O(1).

```java
 public boolean judgeSquareSum(int target) {
     if (target < 0) return false;
     int i = 0, j = (int) Math.sqrt(target);
     while (i <= j) {
         int powSum = i * i + j * j;
         if (powSum == target) {
             return true;
         } else if (powSum > target) {
             j--;
         } else {
             i++;
         }
     }
     return false;
 }
```

## 3. Reverse Vowels of a String

345\. Reverse Vowels of a String (Easy)

[Leetcode](https://leetcode.com/problems/reverse-vowels-of-a-string/description/) / [LeetCode China](https://leetcode-cn.com/problems/reverse-vowels-of-a-string/description/)

```html
Given s = "leetcode", return "leotcede".
```

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a7cb8423-895d-4975-8ef8-662a0029c772.png" width="400px"> </div><br>

Use two pointers: one traverses from front to back, and the other traverses from back to front. When both pointers reach vowels, swap the two vowels.

To quickly determine whether a character is a vowel, add all vowels to a `HashSet`, allowing the check to run in O(1) time.

- Time complexity is O(N): all elements are traversed only once.
- Space complexity is O(1): only two extra variables are used.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ef25ff7c-0f63-420d-8b30-eafbeea35d11.gif" width="400px"> </div><br>

```java
private final static HashSet<Character> vowels = new HashSet<>(
        Arrays.asList('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'));

public String reverseVowels(String s) {
    if (s == null) return null;
    int i = 0, j = s.length() - 1;
    char[] result = new char[s.length()];
    while (i <= j) {
        char ci = s.charAt(i);
        char cj = s.charAt(j);
        if (!vowels.contains(ci)) {
            result[i++] = ci;
        } else if (!vowels.contains(cj)) {
            result[j--] = cj;
        } else {
            result[i++] = cj;
            result[j--] = ci;
        }
    }
    return new String(result);
}
```

## 4. Valid Palindrome II

680\. Valid Palindrome II (Easy)

[Leetcode](https://leetcode.com/problems/valid-palindrome-ii/description/) / [LeetCode China](https://leetcode-cn.com/problems/valid-palindrome-ii/description/)

```html
Input: "abca"
Output: True
Explanation: You could delete the character 'c'.
```

Problem description: determine whether a palindrome can be formed by deleting one character.

A palindrome is a string with left-right symmetry; for example, `"abcba"` is a palindrome.

Two pointers can easily determine whether a string is a palindrome: one pointer traverses from left to right, and the other from right to left. The two pointers move one position at a time, checking whether the characters they point to are the same. Only if all pairs match does the string have palindrome symmetry.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/fcc941ec-134b-4dcd-bc86-1702fd305300.gif" width="250px"> </div><br>

The key is handling the deletion of one character. When using two pointers to traverse the string, if the two pointed characters differ, try deleting one character and then check whether the remaining string is a palindrome.

When checking whether it is a palindrome, there is no need to check the entire string, because the characters to the left of the left pointer and to the right of the right pointer have already been verified as symmetric. Only the middle substring needs to be checked.

When trying to delete a character, either the character pointed to by the left pointer or the character pointed to by the right pointer can be deleted.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/db5f30a7-8bfa-4ecc-ab5d-747c77818964.gif" width="300px"> </div><br>

```java
public boolean validPalindrome(String s) {
    for (int i = 0, j = s.length() - 1; i < j; i++, j--) {
        if (s.charAt(i) != s.charAt(j)) {
            return isPalindrome(s, i, j - 1) || isPalindrome(s, i + 1, j);
        }
    }
    return true;
}

private boolean isPalindrome(String s, int i, int j) {
    while (i < j) {
        if (s.charAt(i++) != s.charAt(j--)) {
            return false;
        }
    }
    return true;
}
```

## 5. Merge Sorted Array

88\. Merge Sorted Array (Easy)

[Leetcode](https://leetcode.com/problems/merge-sorted-array/description/) / [LeetCode China](https://leetcode-cn.com/problems/merge-sorted-array/description/)

```html
Input:
nums1 = [1,2,3,0,0,0], m = 3
nums2 = [2,5,6],       n = 3

Output: [1,2,2,3,5,6]
```

Problem description: store the merged result in the first array.

Traverse from the end; otherwise, values merged into `nums1` may overwrite values that have not yet been compared.

```java
public void merge(int[] nums1, int m, int[] nums2, int n) {
    int index1 = m - 1, index2 = n - 1;
    int indexMerge = m + n - 1;
    while (index2 >= 0) {
        if (index1 < 0) {
            nums1[indexMerge--] = nums2[index2--];
        } else if (index2 < 0) {
            nums1[indexMerge--] = nums1[index1--];
        } else if (nums1[index1] > nums2[index2]) {
            nums1[indexMerge--] = nums1[index1--];
        } else {
            nums1[indexMerge--] = nums2[index2--];
        }
    }
}
```

## 6. Linked List Cycle

141\. Linked List Cycle (Easy)

[Leetcode](https://leetcode.com/problems/linked-list-cycle/description/) / [LeetCode China](https://leetcode-cn.com/problems/linked-list-cycle/description/)

Use two pointers: one moves one node at a time, and the other moves two nodes at a time. If a cycle exists, the two pointers will eventually meet.

```java
public boolean hasCycle(ListNode head) {
    if (head == null) {
        return false;
    }
    ListNode l1 = head, l2 = head.next;
    while (l1 != null && l2 != null && l2.next != null) {
        if (l1 == l2) {
            return true;
        }
        l1 = l1.next;
        l2 = l2.next.next;
    }
    return false;
}
```

## 7. Longest Word in Dictionary through Deleting

524\. Longest Word in Dictionary through Deleting (Medium)

[Leetcode](https://leetcode.com/problems/longest-word-in-dictionary-through-deleting/description/) / [LeetCode China](https://leetcode-cn.com/problems/longest-word-in-dictionary-through-deleting/description/)

```
Input:
s = "abpcplea", d = ["ale","apple","monkey","plea"]

Output:
"apple"
```

Problem description: delete some characters from `s` so it becomes a string in list `d`, and find the longest string that can be formed. If multiple results have the same length, return the lexicographically smallest one.

If string `t` can be obtained by deleting characters from string `s`, then `t` is a subsequence of `s`. Two pointers can be used to determine whether one string is a subsequence of another.

```java
public String findLongestWord(String s, List<String> d) {
    String longestWord = "";
    for (String target : d) {
        int l1 = longestWord.length(), l2 = target.length();
        if (l1 > l2 || (l1 == l2 && longestWord.compareTo(target) < 0)) {
            continue;
        }
        if (isSubstr(s, target)) {
            longestWord = target;
        }
    }
    return longestWord;
}

private boolean isSubstr(String s, String target) {
    int i = 0, j = 0;
    while (i < s.length() && j < target.length()) {
        if (s.charAt(i) == target.charAt(j)) {
            j++;
        }
        i++;
    }
    return j == target.length();
}
```
