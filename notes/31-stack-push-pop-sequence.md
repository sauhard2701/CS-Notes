# 31. Stack Push/Pop Sequence

## Problem Link

[NowCoder](https://www.nowcoder.com/practice/d77d11405cc7470d82554cb392585106?tpId=13&tqId=11174&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking&from=cyc_github)

## Problem Description

Given two integer sequences, where the first sequence is the push order of a stack, determine whether the second sequence can be a pop order of that stack. Assume all numbers pushed into the stack are distinct.

For example, sequence 1,2,3,4,5 is the push order of a stack, and sequence 4,5,3,2,1 is one possible pop order for that push sequence, but 4,3,5,1,2 cannot be a pop order for it.

## Solution

Use a stack to simulate push and pop operations. After each element is pushed, check whether the stack top is the first element of the current popSequence. If it is, pop it and move popSequence one position forward, then continue checking.

```java
public boolean IsPopOrder(int[] pushSequence, int[] popSequence) {
    int n = pushSequence.length;
    Stack<Integer> stack = new Stack<>();
    for (int pushIndex = 0, popIndex = 0; pushIndex < n; pushIndex++) {
        stack.push(pushSequence[pushIndex]);
        while (popIndex < n && !stack.isEmpty() 
                && stack.peek() == popSequence[popIndex]) {
            stack.pop();
            popIndex++;
        }
    }
    return stack.isEmpty();
}
```

