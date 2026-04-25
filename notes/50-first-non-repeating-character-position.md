# 50. First Non-Repeating Character Position

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/1c82e8cf713b4bbeb2a5b31cf5b0417c?tpId=13&tqId=11187&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Find the first character that appears only once in a string and return its position. The string contains only ASCII characters.

```
Input: abacc
Output: b
```

## Solution

The most intuitive solution is to use a HashMap to count occurrences: the character is the key, and the occurrence count is the value. Each time the string is traversed, increment the value corresponding to the key by 1. Finally, traverse the HashMap again to find the character whose occurrence count is 1.

Because the range of characters to count is limited, an integer array can also be used instead of a HashMap. ASCII has only 128 characters, so an integer array of length 128 can store the occurrence count of each character.

```java
public int FirstNotRepeatingChar(String str) {
    int[] cnts = new int[128];
    for (int i = 0; i < str.length(); i++)
        cnts[str.charAt(i)]++;
    for (int i = 0; i < str.length(); i++)
        if (cnts[str.charAt(i)] == 1)
            return i;
    return -1;
}
```

The space complexity of the implementation above is not optimal. Since only the character that appears once needs to be found, the required count information is only 0, 1, or greater, and two bits are enough to store this information.

```java
public int FirstNotRepeatingChar2(String str) {
    BitSet bs1 = new BitSet(128);
    BitSet bs2 = new BitSet(128);
    for (char c : str.toCharArray()) {
        if (!bs1.get(c) && !bs2.get(c))
            bs1.set(c);     // 0 0 -> 0 1
        else if (bs1.get(c) && !bs2.get(c))
            bs2.set(c);     // 0 1 -> 1 1
    }
    for (int i = 0; i < str.length(); i++) {
        char c = str.charAt(i);
        if (bs1.get(c) && !bs2.get(c))  // 0 1
            return i;
    }
    return -1;
}
```
