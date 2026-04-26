# LeetCode Solutions - Bit Manipulation
<!-- GFM-TOC -->
* [LeetCode Solutions - Bit Manipulation](#leetcode-solutions---bit-manipulation)
    * [0. Principles](#_0-principles)
    * [1. Hamming Distance](#_1-hamming-distance)
    * [2. Single Number](#_2-single-number)
    * [3. Missing Number](#_3-missing-number)
    * [4. Single Number III](#_4-single-number-iii)
    * [5. Reverse Bits](#_5-reverse-bits)
    * [6. Swap Two Integers Without Extra Variable](#_6-swap-two-integers-without-extra-variable)
    * [7. Power of Two](#_7-power-of-two)
    * [8. Power of Four](#_8-power-of-four)
    * [9. Binary Number with Alternating Bits](#_9-binary-number-with-alternating-bits)
    * [10. Number Complement](#_10-number-complement)
    * [11. Sum of Two Integers](#_11-sum-of-two-integers)
    * [12. Maximum Product of Word Lengths](#_12-maximum-product-of-word-lengths)
    * [13. Counting Bits](#_13-counting-bits)
<!-- GFM-TOC -->


## 0. Principles

**Basic Principles** 

0s represents a sequence of 0s, and 1s represents a sequence of 1s.

```
x ^ 0s = x      x & 0s = 0      x | 0s = x
x ^ 1s = ~x     x & 1s = x      x | 1s = 1s
x ^ x = 0       x & x = x       x | x = x
```

Using the property `x ^ 1s = \~x`, the bit-level representation of a number can be flipped. Using the property `x ^ x = 0`, two duplicate numbers among three numbers can be removed, leaving only the other number.

```
1^1^2 = 2
```

Using `x & 0s = 0` and `x & 1s = x`, mask operations can be implemented. When a number `num` is ANDed with mask `00111100`, only the bits in `num` corresponding to the 1 bits of the mask are kept.

```
01011011 &
00111100
--------
00011000
```

Using `x | 0s = x` and `x | 1s = 1s`, setting operations can be implemented. When a number `num` is ORed with mask `00111100`, the bits in `num` corresponding to the 1 bits of the mask are set to 1.

```
01011011 |
00111100
--------
01111111
```

**Bitwise AND Tricks** 

`n & (n - 1)` removes the lowest 1 bit in `n`'s bit-level representation. For example, for binary representation `01011011`, subtracting 1 gives `01011010`; ANDing the two numbers gives `01011010`.

```
01011011 &
01011010
--------
01011010
```

`n & (-n)` obtains the lowest 1 bit in `n`'s bit-level representation. `-n` is the one's complement of `n` plus 1, namely `-n = \~n + 1`. For example, for binary representation `10110100`, `-n` gives `01001100`, and ANDing them gives `00000100`.

```
10110100 &
01001100
--------
00000100
```

`n - (n & (-n))` can also remove the lowest 1 bit in `n`'s bit-level representation, with the same effect as `n & (n - 1)`.

**Shift Operations** 

`\\>\\> n` is arithmetic right shift, equivalent to dividing by 2<sup>n</sup>. For example, `-7 \\>\\> 2 = -2`.

```
11111111111111111111111111111001  >> 2
--------
11111111111111111111111111111110
```

`\\>\\>\\> n` is unsigned right shift, filling the left side with 0. For example, `-7 \\>\\>\\> 2 = 1073741822`.

```
11111111111111111111111111111001  >>> 2
--------
00111111111111111111111111111111
```

`\<\< n` is arithmetic left shift, equivalent to multiplying by 2<sup>n</sup>. `-7 \<\< 2 = -28`.

```
11111111111111111111111111111001  << 2
--------
11111111111111111111111111100100
```

**Mask Calculation** 

To get `111111111`, invert 0: `\~0`.

To get a mask where only bit `i` is 1, shift 1 left by `i - 1` bits: `1 \<\< (i - 1)`. For example, `1 \<\< 4` gets a mask where only the 5th bit is 1: `00010000`.

To get a mask where bits 1 through `i` are 1, use `(1 \<\< i) - 1`. For example, `(1 \<\< 4) - 1 = 00010000 - 1 = 00001111`.

To get a mask where bits 1 through `i` are 0, invert the mask where bits 1 through `i` are 1: `\~((1 \<\< i) - 1)`.

**Bit Operations in Java**  

```html
static int Integer.bitCount();           // count the number of 1s
static int Integer.highestOneBit();      // get the highest bit
static String toBinaryString(int i);     // convert to a binary string
```

## 1. Hamming Distance

461. Hamming Distance (Easy)

[Leetcode](https://leetcode.com/problems/hamming-distance/) / [LeetCode China](https://leetcode-cn.com/problems/hamming-distance/)

```html
Input: x = 1, y = 4

Output: 2

Explanation:
1   (0 0 0 1)
4   (0 1 0 0)
       ↑   ↑

The above arrows point to positions where the corresponding bits are different.
```

XOR the two numbers. Bits that differ in their bit-level representation become 1, so just count how many 1s there are.

```java
public int hammingDistance(int x, int y) {
    int z = x ^ y;
    int cnt = 0;
    while(z != 0) {
        if ((z & 1) == 1) cnt++;
        z = z >> 1;
    }
    return cnt;
}
```

Use `z & (z - 1)` to remove the lowest 1 bit in `z`'s bit-level representation.

```java
public int hammingDistance(int x, int y) {
    int z = x ^ y;
    int cnt = 0;
    while (z != 0) {
        z &= (z - 1);
        cnt++;
    }
    return cnt;
}
```

`Integer.bitCount()` can be used to count the number of 1s.

```java
public int hammingDistance(int x, int y) {
    return Integer.bitCount(x ^ y);
}
```

## 2. Single Number

136\. Single Number (Easy)

[Leetcode](https://leetcode.com/problems/single-number/description/) / [LeetCode China](https://leetcode-cn.com/problems/single-number/description/)

```html
Input: [4,1,2,1,2]
Output: 4
```

The XOR result of two identical numbers is 0. XOR all numbers, and the final result is the number that appears only once.

```java
public int singleNumber(int[] nums) {
    int ret = 0;
    for (int n : nums) ret = ret ^ n;
    return ret;
}
```

## 3. Missing Number

268\. Missing Number (Easy)

[Leetcode](https://leetcode.com/problems/missing-number/description/) / [LeetCode China](https://leetcode-cn.com/problems/missing-number/description/)

```html
Input: [3,0,1]
Output: 2
```

Problem description: array elements are between 0 and n, but one number is missing. Find the missing number.

```java
public int missingNumber(int[] nums) {
    int ret = 0;
    for (int i = 0; i < nums.length; i++) {
        ret = ret ^ i ^ nums[i];
    }
    return ret ^ nums.length;
}
```

## 4. Single Number III

260\. Single Number III (Medium)

[Leetcode](https://leetcode.com/problems/single-number-iii/description/) / [LeetCode China](https://leetcode-cn.com/problems/single-number-iii/description/)

Two unequal elements must differ in at least one bit in their bit-level representations.

XORing all elements in the array gives the XOR result of the two non-duplicate elements.

`diff &= -diff` obtains the rightmost non-zero bit of `diff`, which is the rightmost bit where the two non-duplicate elements differ. This bit can be used to distinguish the two elements.

```java
public int[] singleNumber(int[] nums) {
    int diff = 0;
    for (int num : nums) diff ^= num;
    diff &= -diff;  // get the rightmost bit
    int[] ret = new int[2];
    for (int num : nums) {
        if ((num & diff) == 0) ret[0] ^= num;
        else ret[1] ^= num;
    }
    return ret;
}
```

## 5. Reverse Bits

190\. Reverse Bits (Easy)

[Leetcode](https://leetcode.com/problems/reverse-bits/description/) / [LeetCode China](https://leetcode-cn.com/problems/reverse-bits/description/)

```java
public int reverseBits(int n) {
    int ret = 0;
    for (int i = 0; i < 32; i++) {
        ret <<= 1;
        ret |= (n & 1);
        n >>>= 1;
    }
    return ret;
}
```

If this function needs to be called many times, split the `int` into 4 bytes, cache the bit reversal corresponding to each byte, and finally concatenate the results.

```java
private static Map<Byte, Integer> cache = new HashMap<>();

public int reverseBits(int n) {
    int ret = 0;
    for (int i = 0; i < 4; i++) {
        ret <<= 8;
        ret |= reverseByte((byte) (n & 0b11111111));
        n >>= 8;
    }
    return ret;
}

private int reverseByte(byte b) {
    if (cache.containsKey(b)) return cache.get(b);
    int ret = 0;
    byte t = b;
    for (int i = 0; i < 8; i++) {
        ret <<= 1;
        ret |= t & 1;
        t >>= 1;
    }
    cache.put(b, ret);
    return ret;
}
```

## 6. Swap Two Integers Without Extra Variable

[Programmer Code Interview Guide: P317](#)

```java
a = a ^ b;
b = a ^ b;
a = a ^ b;
```

## 7. Power of Two

231\. Power of Two (Easy)

[Leetcode](https://leetcode.com/problems/power-of-two/description/) / [LeetCode China](https://leetcode-cn.com/problems/power-of-two/description/)

The binary representation contains exactly one 1.

```java
public boolean isPowerOfTwo(int n) {
    return n > 0 && Integer.bitCount(n) == 1;
}
```

Using the property `1000 & 0111 == 0`, we get the following solution:

```java
public boolean isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```

## 8. Power of Four

342\. Power of Four (Easy)

[Leetcode](https://leetcode.com/problems/power-of-four/) / [LeetCode China](https://leetcode-cn.com/problems/power-of-four/)

Such a number has exactly one odd-position bit equal to 1 in its binary representation, such as 16 (`10000`).

```java
public boolean isPowerOfFour(int num) {
    return num > 0 && (num & (num - 1)) == 0 && (num & 0b01010101010101010101010101010101) != 0;
}
```

It can also be matched with a regular expression.

```java
public boolean isPowerOfFour(int num) {
    return Integer.toString(num, 4).matches("10*");
}
```

## 9. Binary Number with Alternating Bits

693\. Binary Number with Alternating Bits (Easy)

[Leetcode](https://leetcode.com/problems/binary-number-with-alternating-bits/description/) / [LeetCode China](https://leetcode-cn.com/problems/binary-number-with-alternating-bits/description/)

```html
Input: 10
Output: True
Explanation:
The binary representation of 10 is: 1010.

Input: 11
Output: False
Explanation:
The binary representation of 11 is: 1011.
```

For a number with bit-level representation like `1010`, shifting it right by 1 bit gives `101`. Every bit differs between the two numbers, so XORing them gives `1111`.

```java
public boolean hasAlternatingBits(int n) {
    int a = (n ^ (n >> 1));
    return (a & (a + 1)) == 0;
}
```

## 10. Number Complement

476\. Number Complement (Easy)

[Leetcode](https://leetcode.com/problems/number-complement/description/) / [LeetCode China](https://leetcode-cn.com/problems/number-complement/description/)

```html
Input: 5
Output: 2
Explanation: The binary representation of 5 is 101 (no leading zero bits), and its complement is 010. So you need to output 2.
```

Problem description: ignore the leading 0s in the binary representation.

For `00000101`, its complement can be obtained by XORing it with `00000111`. The problem is therefore converted into finding mask `00000111`.

```java
public int findComplement(int num) {
    if (num == 0) return 1;
    int mask = 1 << 30;
    while ((num & mask) == 0) mask >>= 1;
    mask = (mask << 1) - 1;
    return num ^ mask;
}
```

Java's `Integer.highestOneBit()` method can be used to get the number containing the leading 1.

```java
public int findComplement(int num) {
    if (num == 0) return 1;
    int mask = Integer.highestOneBit(num);
    mask = (mask << 1) - 1;
    return num ^ mask;
}
```

To expand a number such as `10000000` into `11111111`, use the following method:

```html
mask |= mask >> 1    11000000
mask |= mask >> 2    11110000
mask |= mask >> 4    11111111
```

```java
public int findComplement(int num) {
    int mask = num;
    mask |= mask >> 1;
    mask |= mask >> 2;
    mask |= mask >> 4;
    mask |= mask >> 8;
    mask |= mask >> 16;
    return (mask ^ num);
}
```

## 11. Sum of Two Integers

371\. Sum of Two Integers (Easy)

[Leetcode](https://leetcode.com/problems/sum-of-two-integers/description/) / [LeetCode China](https://leetcode-cn.com/problems/sum-of-two-integers/description/)

`a ^ b` represents the sum of two numbers without considering carry, and `(a & b) \<\< 1` is the carry.

The recursion terminates because `(a & b) \<\< 1` adds one more 0 on the right. As recursion continues, the number of trailing 0s in the carry gradually increases, and eventually the carry becomes 0, ending the recursion.

```java
public int getSum(int a, int b) {
    return b == 0 ? a : getSum((a ^ b), (a & b) << 1);
}
```

## 12. Maximum Product of Word Lengths

318\. Maximum Product of Word Lengths (Medium)

[Leetcode](https://leetcode.com/problems/maximum-product-of-word-lengths/description/) / [LeetCode China](https://leetcode-cn.com/problems/maximum-product-of-word-lengths/description/)

```html
Given ["abcw", "baz", "foo", "bar", "xtfn", "abcdef"]
Return 16
The two words can be "abcw", "xtfn".
```

Problem description: strings in the string array contain only lowercase characters. Find the maximum product of the lengths of two strings such that the two strings do not contain any common characters.

The main issue is determining whether two strings contain common characters. Since the strings contain only lowercase characters, there are 26 possible letters, so a 32-bit integer can store whether each character appears.

```java
public int maxProduct(String[] words) {
    int n = words.length;
    int[] val = new int[n];
    for (int i = 0; i < n; i++) {
        for (char c : words[i].toCharArray()) {
            val[i] |= 1 << (c - 'a');
        }
    }
    int ret = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if ((val[i] & val[j]) == 0) {
                ret = Math.max(ret, words[i].length() * words[j].length());
            }
        }
    }
    return ret;
}
```

## 13. Counting Bits

338\. Counting Bits (Medium)

[Leetcode](https://leetcode.com/problems/counting-bits/description/) / [LeetCode China](https://leetcode-cn.com/problems/counting-bits/description/)

For number 6 (`110`), it can be viewed as 4 (`100`) plus 2 (`10`), so `dp[i] = dp[i & (i - 1)] + 1`.

```java
public int[] countBits(int num) {
    int[] ret = new int[num + 1];
    for(int i = 1; i <= num; i++){
        ret[i] = ret[i&(i-1)] + 1;
    }
    return ret;
}
```
