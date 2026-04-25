# LeetCode Solutions - Strings
<!-- GFM-TOC -->
* [LeetCode Solutions - Strings](#leetcode-solutions---strings)
    * [1. String Rotation Inclusion](#1-string-rotation-inclusion)
    * [2. String Rotation](#2-string-rotation)
    * [3. Reverse Words in a String](#3-reverse-words-in-a-string)
    * [4. Valid Anagram](#4-valid-anagram)
    * [5. Longest Palindrome](#5-longest-palindrome)
    * [6. Isomorphic Strings](#6-isomorphic-strings)
    * [7. Palindromic Substrings](#7-palindromic-substrings)
    * [8. Palindrome Number](#8-palindrome-number)
    * [9. Count Binary Substrings](#9-count-binary-substrings)
<!-- GFM-TOC -->


## 1. String Rotation Inclusion

[The Beauty of Programming 3.1](#)

```html
s1 = AABCD, s2 = CDAA
Return : true
```

Given two strings s1 and s2, determine whether s2 can be contained in a string obtained by cyclically shifting s1.

The result of cyclically shifting s1 is a substring of s1s1, so it is enough to determine whether s2 is a substring of s1s1.

## 2. String Rotation

[The Beauty of Programming 2.17](#)

```html
s = "abcd123" k = 3
Return "123abcd"
```

Cyclically shift the string k positions to the right.

Reverse abcd and 123 in abcd123 separately to get dcba321, then reverse the entire string to get 123abcd.

## 3. Reverse Words in a String

[Programmer Code Interview Guide](#)

```html
s = "I am a student"
Return "student a am I"
```

Reverse each word, then reverse the entire string.

## 4. Valid Anagram

242\. Valid Anagram (Easy)

[Leetcode](https://leetcode.com/problems/valid-anagram/description/) / [LeetCode China](https://leetcode-cn.com/problems/valid-anagram/description/)

```html
s = "anagram", t = "nagaram", return true.
s = "rat", t = "car", return false.
```

Use a HashMap to map characters to occurrence counts, then compare whether the two strings have the same character counts.

Because the strings in this problem contain only 26 lowercase letters, an integer array of length 26 can be used to count character occurrences instead of using a HashMap.

```java
public boolean isAnagram(String s, String t) {
    int[] cnts = new int[26];
    for (char c : s.toCharArray()) {
        cnts[c - 'a']++;
    }
    for (char c : t.toCharArray()) {
        cnts[c - 'a']--;
    }
    for (int cnt : cnts) {
        if (cnt != 0) {
            return false;
        }
    }
    return true;
}
```

## 5. Longest Palindrome

409\. Longest Palindrome (Easy)

[Leetcode](https://leetcode.com/problems/longest-palindrome/description/) / [LeetCode China](https://leetcode-cn.com/problems/longest-palindrome/description/)

```html
Input : "abccccdd"
Output : 7
Explanation : One longest palindrome that can be built is "dccaccd", whose length is 7.
```

Use an integer array of length 256 to count the occurrences of each character. Even counts of each character can be used to form a palindrome.

Because the middle character of a palindrome can appear alone, if there is a single unused character, place it in the middle.

```java
public int longestPalindrome(String s) {
    int[] cnts = new int[256];
    for (char c : s.toCharArray()) {
        cnts[c]++;
    }
    int palindrome = 0;
    for (int cnt : cnts) {
        palindrome += (cnt / 2) * 2;
    }
    if (palindrome < s.length()) {
        palindrome++;   // under this condition, s must contain a single unused character that can be placed in the middle of the palindrome
    }
    return palindrome;
}
```

## 6. Isomorphic Strings

205\. Isomorphic Strings (Easy)

[Leetcode](https://leetcode.com/problems/isomorphic-strings/description/) / [LeetCode China](https://leetcode-cn.com/problems/isomorphic-strings/description/)

```html
Given "egg", "add", return true.
Given "foo", "bar", return false.
Given "paper", "title", return true.
```

Record the previous position of each character. If the previous positions of the corresponding characters in the two strings are the same, the strings are isomorphic.

```java
public boolean isIsomorphic(String s, String t) {
    int[] preIndexOfS = new int[256];
    int[] preIndexOfT = new int[256];
    for (int i = 0; i < s.length(); i++) {
        char sc = s.charAt(i), tc = t.charAt(i);
        if (preIndexOfS[sc] != preIndexOfT[tc]) {
            return false;
        }
        preIndexOfS[sc] = i + 1;
        preIndexOfT[tc] = i + 1;
    }
    return true;
}
```

## 7. Palindromic Substrings

647\. Palindromic Substrings (Medium)

[Leetcode](https://leetcode.com/problems/palindromic-substrings/description/) / [LeetCode China](https://leetcode-cn.com/problems/palindromic-substrings/description/)

```html
Input: "aaa"
Output: 6
Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".
```

Starting from a position in the string, try to expand the substring.

```java
private int cnt = 0;

public int countSubstrings(String s) {
    for (int i = 0; i < s.length(); i++) {
        extendSubstrings(s, i, i);     // odd length
        extendSubstrings(s, i, i + 1); // even length
    }
    return cnt;
}

private void extendSubstrings(String s, int start, int end) {
    while (start >= 0 && end < s.length() && s.charAt(start) == s.charAt(end)) {
        start--;
        end++;
        cnt++;
    }
}
```

## 8. Palindrome Number

9\. Palindrome Number (Easy)

[Leetcode](https://leetcode.com/problems/palindrome-number/description/) / [LeetCode China](https://leetcode-cn.com/problems/palindrome-number/description/)

The problem requires no extra space, so the integer cannot be converted into a string for checking.

Split the integer into left and right parts. The right part needs to be reversed, then the two parts are compared for equality.

```java
public boolean isPalindrome(int x) {
    if (x == 0) {
        return true;
    }
    if (x < 0 || x % 10 == 0) {
        return false;
    }
    int right = 0;
    while (x > right) {
        right = right * 10 + x % 10;
        x /= 10;
    }
    return x == right || x == right / 10;
}
```

## 9. Count Binary Substrings

696\. Count Binary Substrings (Easy)

[Leetcode](https://leetcode.com/problems/count-binary-substrings/description/) / [LeetCode China](https://leetcode-cn.com/problems/count-binary-substrings/description/)

```html
Input: "00110011"
Output: 6
Explanation: There are 6 substrings that have equal number of consecutive 1's and 0's: "0011", "01", "1100", "10", "0011", and "01".
```

```java
public int countBinarySubstrings(String s) {
    int preLen = 0, curLen = 1, count = 0;
    for (int i = 1; i < s.length(); i++) {
        if (s.charAt(i) == s.charAt(i - 1)) {
            curLen++;
        } else {
            preLen = curLen;
            curLen = 1;
        }

        if (preLen >= curLen) {
            count++;
        }
    }
    return count;
}
```
