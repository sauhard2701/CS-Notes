# Algorithms - Algorithm Analysis
<!-- GFM-TOC -->
* [Algorithms - Algorithm Analysis](#algorithms---algorithm-analysis)
    * [Mathematical Model](#mathematical-model)
        * [1. Approximation](#_1-approximation)
        * [2. Order of Growth](#_2-order-of-growth)
        * [3. Inner Loop](#_3-inner-loop)
        * [4. Cost Model](#_4-cost-model)
    * [Considerations](#considerations)
        * [1. Large Constants](#_1-large-constants)
        * [2. Cache](#_2-cache)
        * [3. Worst-Case Performance Guarantees](#_3-worst-case-performance-guarantees)
        * [4. Randomized Algorithms](#_4-randomized-algorithms)
        * [5. Amortized Analysis](#_5-amortized-analysis)
    * [ThreeSum](#threesum)
        * [1. ThreeSumSlow](#_1-threesumslow)
        * [2. ThreeSumBinarySearch](#_2-threesumbinarysearch)
        * [3. ThreeSumTwoPointer](#_3-threesumtwopointer)
    * [Doubling Test](#doubling-test)
<!-- GFM-TOC -->


## Mathematical Model

### 1. Approximation

N<sup>3</sup>/6-N<sup>2</sup>/2+N/3 \~ N<sup>3</sup>/6. Use \~f(N) to denote functions whose result divided by f(N) approaches 1 as N grows.

### 2. Order of Growth

The order of growth of N<sup>3</sup>/6-N<sup>2</sup>/2+N/3 is O(N<sup>3</sup>). Order of growth separates an algorithm from its specific implementation; an algorithm with order of growth O(N<sup>3</sup>) is independent of whether it is implemented in Java or runs on a particular computer.

### 3. Inner Loop

The instructions executed most frequently determine the total running time of a program; these instructions are called the program's inner loop.

### 4. Cost Model

Use a cost model to evaluate algorithms. For example, the number of array accesses is a cost model.

## Considerations

### 1. Large Constants

When approximating, if the constant coefficient of a lower-order term is very large, the approximation can be wrong.

### 2. Cache

Computer systems use caching to organize memory, so accessing adjacent array elements is much faster than accessing non-adjacent elements.

### 3. Worst-Case Performance Guarantees

For software in nuclear reactors, pacemakers, or brake controllers, worst-case performance is very important.

### 4. Randomized Algorithms

Shuffle the input to remove the algorithm's dependence on input order.

### 5. Amortized Analysis

Amortize cost by dividing the total cost of all operations by the number of operations. For example, performing N consecutive push() calls on an empty stack requires N+4+8+16+...+2N=5N-4 array accesses. N is the number of writes to the array, and the rest are array accesses needed for copying during resizing. After amortization, the average number of array accesses is constant.

## ThreeSum

ThreeSum counts the number of triples in an array whose sum is 0.

```java
public interface ThreeSum {
    int count(int[] nums);
}
```

### 1. ThreeSumSlow

The inner loop of this algorithm is the `if (nums[i] + nums[j] + nums[k] == 0)` statement, which executes N(N-1)(N-2) = N<sup>3</sup>/6-N<sup>2</sup>/2+N/3 times in total. Therefore, its approximate execution count is \~N<sup>3</sup>/6, and its order of growth is O(N<sup>3</sup>).

```java
public class ThreeSumSlow implements ThreeSum {
    @Override
    public int count(int[] nums) {
        int N = nums.length;
        int cnt = 0;
        for (int i = 0; i < N; i++) {
            for (int j = i + 1; j < N; j++) {
                for (int k = j + 1; k < N; k++) {
                    if (nums[i] + nums[j] + nums[k] == 0) {
                        cnt++;
                    }
                }
            }
        }
        return cnt;
    }
}
```

### 2. ThreeSumBinarySearch

Sort the array, sum two elements, and use binary search to check whether the opposite of that sum exists. If it does, then there is a triple whose sum is 0.

Note that this solution can only be used when the array contains no duplicate elements; otherwise, the binary search result will be wrong.

This method can reduce the order of growth of ThreeSum to O(N<sup>2</sup>logN).

```java
public class ThreeSumBinarySearch implements ThreeSum {

    @Override
    public int count(int[] nums) {
        Arrays.sort(nums);
        int N = nums.length;
        int cnt = 0;
        for (int i = 0; i < N; i++) {
            for (int j = i + 1; j < N; j++) {
                int target = -nums[i] - nums[j];
                int index = BinarySearch.search(nums, target);
                // Note that the index here must be greater than j, otherwise triples will be counted repeatedly.
                if (index > j) {
                    cnt++;
                }
            }
        }
        return cnt;
    }
}
```

```java
public class BinarySearch {

    public static int search(int[] nums, int target) {
        int l = 0, h = nums.length - 1;
        while (l <= h) {
            int m = l + (h - l) / 2;
            if (target == nums[m]) {
                return m;
            } else if (target > nums[m]) {
                l = m + 1;
            } else {
                h = m - 1;
            }
        }
        return -1;
    }
}
```

### 3. ThreeSumTwoPointer

A more efficient method is to sort the array first, then use two pointers for searching. The time complexity is O(N<sup>2</sup>).

This also does not apply when the array contains duplicate elements.

```java
public class ThreeSumTwoPointer implements ThreeSum {

    @Override
    public int count(int[] nums) {
        int N = nums.length;
        int cnt = 0;
        Arrays.sort(nums);
        for (int i = 0; i < N - 2; i++) {
            int l = i + 1, h = N - 1, target = -nums[i];
            while (l < h) {
                int sum = nums[l] + nums[h];
                if (sum == target) {
                    cnt++;
                    l++;
                    h--;
                } else if (sum < target) {
                    l++;
                } else {
                    h--;
                }
            }
        }
        return cnt;
    }
}
```

## Doubling Test

If T(N) \~ aN<sup>b</sup>logN, then T(2N)/T(N) \~ 2<sup>b</sup>.

For example, for the brute-force ThreeSum algorithm, the approximate time is \~N<sup>3</sup>/6. Run the following experiment: run the algorithm multiple times, doubling N each time, record each running time, and compute the ratio between the current running time and the previous running time. The results are as follows:

| N | Time(ms) | Ratio |
| :---: | :---: | :---: |
| 500 | 48 | / |
| 1000 | 320 | 6.7 |
| 2000 | 555 | 1.7 |
| 4000 | 4105 | 7.4 |
| 8000 | 33575 | 8.2 |
| 16000 | 268909 | 8.0 |

We can see that T(2N)/T(N) \~ 2<sup>3</sup>, so T(N) \~ aN<sup>3</sup>logN can be determined.

```java
public class RatioTest {

    public static void main(String[] args) {
        int N = 500;
        int loopTimes = 7;
        double preTime = -1;
        while (loopTimes-- > 0) {
            int[] nums = new int[N];
            StopWatch.start();
            ThreeSum threeSum = new ThreeSumSlow();
            int cnt = threeSum.count(nums);
            System.out.println(cnt);
            double elapsedTime = StopWatch.elapsedTime();
            double ratio = preTime == -1 ? 0 : elapsedTime / preTime;
            System.out.println(N + "  " + elapsedTime + "  " + ratio);
            preTime = elapsedTime;
            N *= 2;
        }
    }
}
```

```java
public class StopWatch {

    private static long start;


    public static void start() {
        start = System.currentTimeMillis();
    }


    public static double elapsedTime() {
        long now = System.currentTimeMillis();
        return (now - start) / 1000.0;
    }
}
```
