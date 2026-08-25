# 3Sum (LeetCode 15)

Comprehensive study notes and 5 YOE senior engineering interview guide on the **Sort + Two Pointers** and **Hash Set Deduplication** techniques for **3Sum** (LeetCode 15).

---

## 1. Core Concepts & Mathematical Foundation

### 1.1 Problem Definition
Given an integer array `nums`, find all unique triplets `[nums[i], nums[j], nums[k]]` such that:
- $i \neq j$, $i \neq k$, and $j \neq k$
- $nums[i] + nums[j] + nums[k] = 0$
- The solution set must **not** contain duplicate triplets.

$$\{(a, b, c) \mid a + b + c = 0, \quad a, b, c \in \text{nums}, \quad a \le b \le c\}$$

- **Constraints**:
  - $3 \le N \le 3000$
  - $-10^5 \le \text{nums}[i] \le 10^5$
  - Time limit requires an $\mathcal{O}(N^2)$ algorithm (an $\mathcal{O}(N^3)$ brute force will Time Out / TLE for $N=3000$).

---

### 1.2 Mathematical & Algorithmic Mechanics

1. **Reduction to Two-Sum Target Subproblem**:
   - Fixing the first element $nums[i]$ reduces the remaining task to finding two numbers $nums[j]$ and $nums[k]$ ($j > i$) such that:
     $$nums[j] + nums[k] = -nums[i]$$
2. **Canonical Ordering for Deduplication**:
   - By sorting `nums` in non-decreasing order ($nums[0] \le nums[1] \le \dots \le nums[N-1]$), every valid triplet is generated in canonical sorted order ($nums[i] \le nums[j] \le nums[k]$).
   - Duplicate triplets are avoided by skipping consecutive duplicate values for both the pivot index $i$ and the pointer movements ($left$ and $right$).
3. **Pruning Optimizations**:
   - **Early Termination**: Because the array is sorted, if the pivot $nums[i] > 0$, any subsequent numbers $nums[j], nums[k] \ge nums[i] > 0$. Their sum can never equal zero, so we can immediately break out of the loop.
   - **Skip Identical Pivots**: If $i > 0$ and $nums[i] == nums[i-1]$, skip iteration to prevent identical triplet sets.

---

## 2. Algorithm Approaches & Complexity Analysis

### 2.1 Complexity Matrix

| Approach | Time Complexity | Auxiliary Space | Remarks |
| :--- | :--- | :--- | :--- |
| **Brute Force (3 nested loops)** | $\mathcal{O}(N^3)$ | $\mathcal{O}(1)$ or $\mathcal{O}(K)$ | Impractical for $N \ge 1000$; TLE |
| **Sort + Hash Set** | $\mathcal{O}(N^2)$ | $\mathcal{O}(N)$ | Uses extra memory for set lookups |
| **Sort + Two Pointers (Optimal)** | $\mathcal{O}(N^2)$ | $\mathcal{O}(1)$ aux ($\mathcal{O}(N)$ sort) | Standard production pattern; optimal cache locality |
| **No-Sort (Hash Map / Sets)** | $\mathcal{O}(N^2)$ | $\mathcal{O}(N)$ | Useful if input stream is immutable / non-sortable |

---

### 2.2 Execution Flow Diagram

```mermaid
flowchart TD
    A[Input: nums of length N] --> B[Sort nums in ascending order]
    B --> C[Loop i from 0 to N-3]
    C --> D{nums[i] > 0?}
    D -- Yes --> E[Break Loop: no further sum can be 0]
    D -- No --> F{i > 0 and nums[i] == nums[i-1]?}
    F -- Yes --> G[Skip to next i]
    F -- No --> H[Set left = i + 1, right = N - 1]
    H --> I{left < right?}
    I -- No --> C
    I -- Yes --> J[Compute total = nums[i] + nums[left] + nums[right]]
    J --> K{total == 0?}
    K -- Yes --> L[Append triplet, left++, right--, skip duplicates]
    L --> I
    K -- total < 0 --> M[left++]
    M --> I
    K -- total > 0 --> N[right--]
    N --> I
```

---

## 3. Implementation Patterns (Python 3.14)

### 3.1 Optimal Sort + Two Pointers Implementation

```python
from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        triplets: List[List[int]] = []

        for i in range(n - 2):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]

                if total == 0:
                    triplets.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1

                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif total < 0:
                    left += 1
                else:
                    right -= 1

        return triplets
```

---

## 4. Edge Cases & Failure Modes

1. **Array Length $< 3$**: Returns empty list `[]`.
2. **All Zeros (`[0, 0, 0, 0]`)**: Correctly returns single triplet `[[0, 0, 0]]` without duplicates.
3. **No Solution Available (`[1, 2, 3]`, `[-5, -4, -3]`)**: Early termination or loop completion returns `[]`.
4. **Heavily Duplicated Values (`[-2, 0, 0, 2, 2, 2]`)**: Duplicate skipping loops ensure only `[[-2, 0, 2]]` is emitted.
5. **Integer Overflow / Limits**: In Python integers have arbitrary precision, but in languages like C++/Java/Go, computing $a + b + c$ with values up to $10^9$ could overflow 32-bit signed integers (requires 64-bit casting).

---

## 5. 5 YOE Senior Interview Questions & Answers

### Q1: How would you generalize 3Sum to the arbitrary $K$-Sum problem ($K \ge 2$) in a production library?
**Answer**:
A production-grade $K$-Sum implementation uses a recursive reduction strategy:
1. **Base Case ($K=2$)**: Use the two-pointer approach on the sorted sub-array.
2. **Recursive Step ($K > 2$)**: Loop through possible choices for the current dimension, skipping adjacent duplicates, and recursively invoke $(K-1)$-Sum with an updated target:
   $$\text{new\_target} = \text{target} - \text{nums}[i]$$
3. **Algorithmic Bounds**:
   - For an array of size $N$, $K$-Sum runs in $\mathcal{O}(N^{K-1})$ time after an initial $\mathcal{O}(N \log N)$ sort.
   - Early pruning: If $K \times \text{nums}[\text{start}] > \text{target}$ or $K \times \text{nums}[-1] < \text{target}$, the branch can be pruned immediately.

*Follow-up*: How does this compare with the Meet-in-the-Middle technique for 4-Sum?
*Answer*: For 4-Sum ($K=4$), Meet-in-the-Middle precomputes pairwise sums into a hash map in $\mathcal{O}(N^2)$ time and queries complement pairs in $\mathcal{O}(N^2)$ average time, though handling index collisions and deduplication adds overhead compared to recursive pointer traversal.

---

### Q2: Why is sorting the array and using two pointers preferred over using a Hash Set in terms of cache hierarchy and memory allocation?
**Answer**:
1. **Memory Allocation Overhead**:
   - Hash sets dynamically allocate nodes (or expand open-addressed tables) on the heap. Allocating and garbage-collecting thousands of entries per query incurs significant memory pressure and fragmentation.
2. **L1/L2 Cache Locality**:
   - Sorting rearranges items into a contiguous array buffer. The two-pointer traversal sequentially walks memory forward (`left++`) and backward (`right--`), allowing CPU hardware prefetchers to anticipate cache lines with minimal cache misses.
3. **Deduplication Simplicity**:
   - In the two-pointer approach, skipping adjacent duplicate elements handles deduplication in $\mathcal{O}(1)$ auxiliary space without needing tuple hashing or secondary set lookups.

---

### Q3: How would you solve 3Sum if the dataset is 500GB (does not fit in RAM) and stored across a distributed cluster?
**Answer**:
1. **External Sort & Partitioning**:
   - Run a distributed Sort (e.g., in Apache Spark or MapReduce) to partition the data into ordered range buckets $[R_0, R_1, \dots, R_m]$ based on quantiles.
2. **Three-Way Join / Distributed Broadcast**:
   - Triplets can span up to 3 partition ranges $(P_a, P_b, P_c)$ where range sum spans zero: $\min(P_a) + \min(P_b) + \min(P_c) \le 0 \le \max(P_a) + \max(P_b) + \max(P_c)$.
   - Generate all candidate partition triplets $(a, b, c)$ that satisfy range overlap.
   - Replicate or stream partition chunks to worker nodes and execute local two-pointer search on partition pairs/triplets.
3. **Deduplication**:
   - Enforce partition ordering $a \le b \le c$ to prevent cross-partition duplicate generation, and aggregate final results.

---

### Q4: If the input consists of floating-point numbers (`float64`) and we seek $|a + b + c| \le \epsilon$, what numerical stability issues arise and how do you adapt the algorithm?
**Answer**:
1. **Floating-Point Representation Issues**:
   - Direct equality `a + b + c == 0` fails due to IEEE 754 precision rounding.
2. **Tolerance Window**:
   - Check condition $-\epsilon \le a + b + c \le \epsilon$.
3. **Two-Pointer Adjustment**:
   - If $|a + b + c| \le \epsilon$, record the triplet. However, because multiple nearby numbers could fall within $\epsilon$, we cannot simply skip values using strict equality; we must group values by tolerance bins or use clustering.
   - If $a + b + c < -\epsilon$, increment `left`.
   - If $a + b + c > \epsilon$, decrement `right`.
4. **Catastrophic Cancellation**:
   - Summing numbers of large magnitudes and opposite signs can lose precision. To maximize accuracy, sort by absolute value or accumulate using Kahan summation.

---

## 6. Authoritative References
- LeetCode 15: [3Sum Problem Statement](https://leetcode.com/problems/3sum/)
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. *Introduction to Algorithms (CLRS)*, 4th Edition.
- Timsort Specification & Cache-Oblivious Algorithms.
