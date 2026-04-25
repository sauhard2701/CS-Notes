# 17. Print 1 to Max n-Digit Number

## Problem Description

Given a number n, print the decimal numbers from 1 to the largest n-digit number in order. For example, if the input is 3, print 1, 2, 3, up to the largest 3-digit number, 999.

## Solution

Because n may be very large, the numbers cannot be represented directly with int; instead, store them in a char array.

Use backtracking to generate all numbers.

```java
public void print1ToMaxOfNDigits(int n) {
    if (n <= 0)
        return;
    char[] number = new char[n];
    print1ToMaxOfNDigits(number, 0);
}

private void print1ToMaxOfNDigits(char[] number, int digit) {
    if (digit == number.length) {
        printNumber(number);
        return;
    }
    for (int i = 0; i < 10; i++) {
        number[digit] = (char) (i + '0');
        print1ToMaxOfNDigits(number, digit + 1);
    }
}

private void printNumber(char[] number) {
    int index = 0;
    while (index < number.length && number[index] == '0')
        index++;
    while (index < number.length)
        System.out.print(number[index++]);
    System.out.println();
}
```
