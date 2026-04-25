# LeetCode Solutions - Math
<!-- GFM-TOC -->
* [LeetCode Solutions - Math](#leetcode-solutions---math)
    * [Prime Factorization](#prime-factorization)
    * [Divisibility](#divisibility)
    * [GCD and LCM](#gcd-and-lcm)
        * [1. Count Primes](#1-count-primes)
        * [2. Greatest Common Divisor](#2-greatest-common-divisor)
        * [3. GCD with Bit Operations and Subtraction](#3-gcd-with-bit-operations-and-subtraction)
    * [Base Conversion](#base-conversion)
        * [1. Base 7](#1-base-7)
        * [2. Hexadecimal](#2-hexadecimal)
        * [3. Base 26](#3-base-26)
    * [Factorial](#factorial)
        * [1. Factorial Trailing Zeroes](#1-factorial-trailing-zeroes)
    * [String Addition and Subtraction](#string-addition-and-subtraction)
        * [1. Add Binary](#1-add-binary)
        * [2. Add Strings](#2-add-strings)
    * [Meeting Problems](#meeting-problems)
        * [1. Minimum Moves to Equal Array Elements II](#1-minimum-moves-to-equal-array-elements-ii)
    * [Majority Voting](#majority-voting)
        * [1. Majority Element](#1-majority-element)
    * [Miscellaneous](#miscellaneous)
        * [1. Valid Perfect Square](#1-valid-perfect-square)
        * [2. Power of Three](#2-power-of-three)
        * [3. Product of Array Except Self](#3-product-of-array-except-self)
        * [4. Maximum Product of Three Numbers](#4-maximum-product-of-three-numbers)
<!-- GFM-TOC -->


## Prime Factorization

Every number can be decomposed into a product of prime numbers, for example: 84 = 2<sup>2</sup> \* 3<sup>1</sup> \* 5<sup>0</sup> \* 7<sup>1</sup> \* 11<sup>0</sup> \* 13<sup>0</sup> \* 17<sup>0</sup> \* ...

## Divisibility

Let x = 2<sup>m0</sup> \* 3<sup>m1</sup> \* 5<sup>m2</sup> \* 7<sup>m3</sup> \* 11<sup>m4</sup> \* ...

Let y = 2<sup>n0</sup> \* 3<sup>n1</sup> \* 5<sup>n2</sup> \* 7<sup>n3</sup> \* 11<sup>n4</sup> \* ...

If x divides y (`y mod x == 0`), then for every i, mi \<= ni.

## GCD and LCM

The greatest common divisor of x and y is: gcd(x,y) =  2<sup>min(m0,n0)</sup> \* 3<sup>min(m1,n1)</sup> \* 5<sup>min(m2,n2)</sup> \* ...

The least common multiple of x and y is: lcm(x,y) =  2<sup>max(m0,n0)</sup> \* 3<sup>max(m1,n1)</sup> \* 5<sup>max(m2,n2)</sup> \* ...

### 1. Count Primes

204\. Count Primes (Easy)

[Leetcode](https://leetcode.com/problems/count-primes/description/) / [LeetCode China](https://leetcode-cn.com/problems/count-primes/description/)

The Sieve of Eratosthenes eliminates numbers divisible by each prime whenever a prime is found.

```java
public int countPrimes(int n) {
    boolean[] notPrimes = new boolean[n + 1];
    int count = 0;
    for (int i = 2; i < n; i++) {
        if (notPrimes[i]) {
            continue;
        }
        count++;
        // start from i * i, because if k < i, then k * i was already removed earlier
        for (long j = (long) (i) * i; j < n; j += i) {
            notPrimes[(int) j] = true;
        }
    }
    return count;
}
```

### 2. Greatest Common Divisor

```java
int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}
```

The least common multiple is the product of the two numbers divided by their greatest common divisor.

```java
int lcm(int a, int b) {
    return a * b / gcd(a, b);
}
```

### 3. GCD with Bit Operations and Subtraction

[The Beauty of Programming: 2.7](#)

For the greatest common divisor f(a, b) of a and b:

- If both a and b are even, f(a, b) = 2\*f(a/2, b/2).
- If a is even and b is odd, f(a, b) = f(a/2, b).
- If b is even and a is odd, f(a, b) = f(a, b/2).
- If both a and b are odd, f(a, b) = f(b, a-b).

Multiplication by 2 and division by 2 can both be converted into shift operations.

```java
public int gcd(int a, int b) {
    if (a < b) {
        return gcd(b, a);
    }
    if (b == 0) {
        return a;
    }
    boolean isAEven = isEven(a), isBEven = isEven(b);
    if (isAEven && isBEven) {
        return 2 * gcd(a >> 1, b >> 1);
    } else if (isAEven && !isBEven) {
        return gcd(a >> 1, b);
    } else if (!isAEven && isBEven) {
        return gcd(a, b >> 1);
    } else {
        return gcd(b, a - b);
    }
}
```

## Base Conversion

### 1. Base 7

504\. Base 7 (Easy)

[Leetcode](https://leetcode.com/problems/base-7/description/) / [LeetCode China](https://leetcode-cn.com/problems/base-7/description/)

```java
public String convertToBase7(int num) {
    if (num == 0) {
        return "0";
    }
    StringBuilder sb = new StringBuilder();
    boolean isNegative = num < 0;
    if (isNegative) {
        num = -num;
    }
    while (num > 0) {
        sb.append(num % 7);
        num /= 7;
    }
    String ret = sb.reverse().toString();
    return isNegative ? "-" + ret : ret;
}
```

In Java, `static String toString(int num, int radix)` can convert an integer into a string representation in base `radix`.

```java
public String convertToBase7(int num) {
    return Integer.toString(num, 7);
}
```

### 2. Hexadecimal

405\. Convert a Number to Hexadecimal (Easy)

[Leetcode](https://leetcode.com/problems/convert-a-number-to-hexadecimal/description/) / [LeetCode China](https://leetcode-cn.com/problems/convert-a-number-to-hexadecimal/description/)

```html
Input:
26

Output:
"1a"

Input:
-1

Output:
"ffffffff"
```

Negative numbers must use their two's-complement form.

```java
public String toHex(int num) {
    char[] map = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
    if (num == 0) return "0";
    StringBuilder sb = new StringBuilder();
    while (num != 0) {
        sb.append(map[num & 0b1111]);
        num >>>= 4; // because two's-complement form is considered, the sign bit has no special meaning; use unsigned right shift and fill the left side with 0
    }
    return sb.reverse().toString();
}
```

### 3. Base 26

168\. Excel Sheet Column Title (Easy)

[Leetcode](https://leetcode.com/problems/excel-sheet-column-title/description/) / [LeetCode China](https://leetcode-cn.com/problems/excel-sheet-column-title/description/)

```html
1 -> A
2 -> B
3 -> C
...
26 -> Z
27 -> AA
28 -> AB
```

Because counting starts from 1 rather than 0, `n` must be decremented by 1.

```java
public String convertToTitle(int n) {
    if (n == 0) {
        return "";
    }
    n--;
    return convertToTitle(n / 26) + (char) (n % 26 + 'A');
}
```

## Factorial

### 1. Factorial Trailing Zeroes

172\. Factorial Trailing Zeroes (Easy)

[Leetcode](https://leetcode.com/problems/factorial-trailing-zeroes/description/) / [LeetCode China](https://leetcode-cn.com/problems/factorial-trailing-zeroes/description/)

Trailing zeroes come from 2 * 5. Since there are clearly more 2s than 5s, only the number of 5s needs to be counted.

For a number N, the number of 5s it contains is: N/5 + N/5<sup>2</sup> + N/5<sup>3</sup> + ... Here, N/5 means multiples of 5 not greater than N contribute one 5, and N/5<sup>2</sup> means multiples of 5<sup>2</sup> not greater than N contribute one additional 5, and so on.

```java
public int trailingZeroes(int n) {
    return n == 0 ? 0 : n / 5 + trailingZeroes(n / 5);
}
```

If counting the position of the lowest 1 bit in the binary representation of N!, just count how many 2s there are. This problem comes from [The Beauty of Programming: 2.2](#). As with counting 5s, the number of 2s is N/2 + N/2<sup>2</sup> + N/2<sup>3</sup> + ...

## String Addition and Subtraction

### 1. Add Binary

67\. Add Binary (Easy)

[Leetcode](https://leetcode.com/problems/add-binary/description/) / [LeetCode China](https://leetcode-cn.com/problems/add-binary/description/)

```html
a = "11"
b = "1"
Return "100".
```

```java
public String addBinary(String a, String b) {
    int i = a.length() - 1, j = b.length() - 1, carry = 0;
    StringBuilder str = new StringBuilder();
    while (carry == 1 || i >= 0 || j >= 0) {
        if (i >= 0 && a.charAt(i--) == '1') {
            carry++;
        }
        if (j >= 0 && b.charAt(j--) == '1') {
            carry++;
        }
        str.append(carry % 2);
        carry /= 2;
    }
    return str.reverse().toString();
}
```

### 2. Add Strings

415\. Add Strings (Easy)

[Leetcode](https://leetcode.com/problems/add-strings/description/) / [LeetCode China](https://leetcode-cn.com/problems/add-strings/description/)

The string values are non-negative integers.

```java
public String addStrings(String num1, String num2) {
    StringBuilder str = new StringBuilder();
    int carry = 0, i = num1.length() - 1, j = num2.length() - 1;
    while (carry == 1 || i >= 0 || j >= 0) {
        int x = i < 0 ? 0 : num1.charAt(i--) - '0';
        int y = j < 0 ? 0 : num2.charAt(j--) - '0';
        str.append((x + y + carry) % 10);
        carry = (x + y + carry) / 10;
    }
    return str.reverse().toString();
}
```

## Meeting Problems

### 1. Minimum Moves to Equal Array Elements II

462\. Minimum Moves to Equal Array Elements II (Medium)

[Leetcode](https://leetcode.com/problems/minimum-moves-to-equal-array-elements-ii/description/) / [LeetCode China](https://leetcode-cn.com/problems/minimum-moves-to-equal-array-elements-ii/description/)

```html
Input:
[1,2,3]

Output:
2

Explanation:
Only two moves are needed (remember each move increments or decrements one element):

[1,2,3]  =>  [2,2,3]  =>  [2,2,2]
```

Each move can increment or decrement one array element by one. Find the minimum number of moves.

This is a typical meeting problem. The minimum total movement is achieved by moving all elements to the median. The reason is:

Let m be the median. Let a and b be two elements on opposite sides of m, with b \> a. To make a and b equal, the total number of moves is b - a, which equals (b - m) + (m - a), the number of moves needed to move both numbers to the median.

If the array length is N, N/2 pairs of a and b can be found and moved to position m.

**Solution 1**  

Sort first. Time complexity: O(NlogN).

```java
public int minMoves2(int[] nums) {
    Arrays.sort(nums);
    int move = 0;
    int l = 0, h = nums.length - 1;
    while (l <= h) {
        move += nums[h] - nums[l];
        l++;
        h--;
    }
    return move;
}
```

**Solution 2**  

Use quickselect to find the median. Time complexity: O(N).

```java
public int minMoves2(int[] nums) {
    int move = 0;
    int median = findKthSmallest(nums, nums.length / 2);
    for (int num : nums) {
        move += Math.abs(num - median);
    }
    return move;
}

private int findKthSmallest(int[] nums, int k) {
    int l = 0, h = nums.length - 1;
    while (l < h) {
        int j = partition(nums, l, h);
        if (j == k) {
            break;
        }
        if (j < k) {
            l = j + 1;
        } else {
            h = j - 1;
        }
    }
    return nums[k];
}

private int partition(int[] nums, int l, int h) {
    int i = l, j = h + 1;
    while (true) {
        while (nums[++i] < nums[l] && i < h) ;
        while (nums[--j] > nums[l] && j > l) ;
        if (i >= j) {
            break;
        }
        swap(nums, i, j);
    }
    swap(nums, l, j);
    return j;
}

private void swap(int[] nums, int i, int j) {
    int tmp = nums[i];
    nums[i] = nums[j];
    nums[j] = tmp;
}
```

## Majority Voting

### 1. Majority Element

169\. Majority Element (Easy)

[Leetcode](https://leetcode.com/problems/majority-element/description/) / [LeetCode China](https://leetcode-cn.com/problems/majority-element/description/)

Sort the array first; the middle number must appear more than n / 2 times.

```java
public int majorityElement(int[] nums) {
    Arrays.sort(nums);
    return nums[nums.length / 2];
}
```

The Boyer-Moore Majority Vote Algorithm can solve this problem in O(N) time. One way to understand it is: use `cnt` to count occurrences of one element. When the traversed element differs from the counted element, decrement `cnt`. If the first `i` elements have been searched and `cnt == 0`, then the first `i` elements have no majority, or they have a majority that appears fewer than i / 2 times, because if it appeared more than i / 2 times, `cnt` would not be 0. At this point, in the remaining n - i elements, the majority still appears more than (n - i) / 2 times, so continuing the search will find the majority.

```java
public int majorityElement(int[] nums) {
    int cnt = 0, majority = nums[0];
    for (int num : nums) {
        majority = (cnt == 0) ? num : majority;
        cnt = (majority == num) ? cnt + 1 : cnt - 1;
    }
    return majority;
}
```

## Miscellaneous

### 1. Valid Perfect Square

367\. Valid Perfect Square (Easy)

[Leetcode](https://leetcode.com/problems/valid-perfect-square/description/) / [LeetCode China](https://leetcode-cn.com/problems/valid-perfect-square/description/)

```html
Input: 16
Returns: True
```

Square sequence: 1, 4, 9, 16, ...

Gaps: 3, 5, 7, ...

The gaps form an arithmetic sequence. This property can be used to generate the square sequence starting from 1.

```java
public boolean isPerfectSquare(int num) {
    int subNum = 1;
    while (num > 0) {
        num -= subNum;
        subNum += 2;
    }
    return num == 0;
}
```

### 2. Power of Three

326\. Power of Three (Easy)

[Leetcode](https://leetcode.com/problems/power-of-three/description/) / [LeetCode China](https://leetcode-cn.com/problems/power-of-three/description/)

```java
public boolean isPowerOfThree(int n) {
    return n > 0 && (1162261467 % n == 0);
}
```

### 3. Product of Array Except Self

238\. Product of Array Except Self (Medium)

[Leetcode](https://leetcode.com/problems/product-of-array-except-self/description/) / [LeetCode China](https://leetcode-cn.com/problems/product-of-array-except-self/description/)

```html
For example, given [1,2,3,4], return [24,12,8,6].
```

Given an array, create a new array where each element is the product of all elements in the original array except the element at that position.

The required time complexity is O(N), and division cannot be used.

```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] products = new int[n];
    Arrays.fill(products, 1);
    int left = 1;
    for (int i = 1; i < n; i++) {
        left *= nums[i - 1];
        products[i] *= left;
    }
    int right = 1;
    for (int i = n - 2; i >= 0; i--) {
        right *= nums[i + 1];
        products[i] *= right;
    }
    return products;
}
```

### 4. Maximum Product of Three Numbers

628\. Maximum Product of Three Numbers (Easy)

[Leetcode](https://leetcode.com/problems/maximum-product-of-three-numbers/description/) / [LeetCode China](https://leetcode-cn.com/problems/maximum-product-of-three-numbers/description/)

```html
Input: [1,2,3,4]
Output: 24
```

```java
public int maximumProduct(int[] nums) {
    int max1 = Integer.MIN_VALUE, max2 = Integer.MIN_VALUE, max3 = Integer.MIN_VALUE, min1 = Integer.MAX_VALUE, min2 = Integer.MAX_VALUE;
    for (int n : nums) {
        if (n > max1) {
            max3 = max2;
            max2 = max1;
            max1 = n;
        } else if (n > max2) {
            max3 = max2;
            max2 = n;
        } else if (n > max3) {
            max3 = n;
        }

        if (n < min1) {
            min2 = min1;
            min1 = n;
        } else if (n < min2) {
            min2 = n;
        }
    }
    return Math.max(max1*max2*max3, max1*min1*min2);
}
```
