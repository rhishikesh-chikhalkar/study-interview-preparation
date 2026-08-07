# Running Sum of 1d Array (LeetCode 1480)

Detailed study notes and 5 YOE interview preparation guide on the **Prefix Sum Accumulation**
technique for **Running Sum of 1d Array** (LeetCode 1480).

---

## 1. Core Concepts & Mathematical Foundation

### 1.1 Problem Definition
Given an array `nums`, return the running sum of `nums` defined as:

$$\text{runningSum}[i] = \sum_{k=0}^{i} \text{nums}[k]$$

- **Constraints**:
  - $1 \le N \le 1000$
  - $-10^6 \le \text{nums}[i] \le 10^6$

---

### 1.2 Recurrence Relation & Monotonic Identity
The running sum computation satisfies the linear recurrence relation:

- $\text{runningSum}[0] = \text{nums}[0]$
- $\text{runningSum}[i] = \text{runningSum}[i-1] + \text{nums}[i]$ for $i > 0$

By leveraging the optimal substructure of partial sums, each element at index $i$ depends only
on the preceding accumulated sum $\text{runningSum}[i-1]$. This eliminates recalculating sums
from index $0$, reducing time complexity from $\mathcal{O}(N^2)$ to $\mathcal{O}(N)$.

---

## 2. Algorithm Comparison & Complexity Analysis

### 2.1 Complexity Matrix

| Approach | Time | Space | Mechanics |
| :--- | :--- | :--- | :--- |
| Brute Force | $\mathcal{O}(N^2)$ | $\mathcal{O}(1)$ | Sum slice `nums[0:i+1]` per step |
| Out-of-Place | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | New output array, single pass |
| In-Place | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Mutate input `nums[i] += nums[i-1]` |
| `itertools.accumulate` | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | C-optimized iterator stream |
| GPU Blelloch Scan | $\mathcal{O}(\log N)$ | $\mathcal{O}(N)$ | Work-efficient Up/Down Sweep |

---

### 2.2 Execution Flow Diagram

```mermaid
flowchart TD
    A[Start: Input Array nums] --> B[Init running_sum = 0, result array]
    B --> C[Loop i from 0 to N-1]
    C --> D{i < N?}
    D -- No --> E[Return result array]
    D -- Yes --> F[running_sum += nums[i]]
    F --> G["result[i] = running_sum"]
    G --> H[i += 1]
    H --> D
```

---

## 3. Implementations

### 3.1 Python Implementation

```python
from typing import List


class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        """Computes running sum in O(N) time and O(N) space without mutating input.

        Accumulates partial sums sequentially.
        """
        n = len(nums)
        result = [0] * n
        current_sum = 0

        for i in range(n):
            current_sum += nums[i]
            result[i] = current_sum

        return result

    def runningSum_inplace(self, nums: List[int]) -> List[int]:
        """Computes running sum in O(N) time and O(1) auxiliary space in-place."""

        for i in range(1, len(nums)):
            nums[i] += nums[i - 1]

        return nums
```

---

### 3.2 Go Implementation

```go
package main

// RunningSum computes running sum in-place with O(N) time and O(1) space.
func RunningSum(nums []int) []int {
	for i := 1; i < len(nums); i++ {
		nums[i] += nums[i-1]
	}
	return nums
}
```

---

## 4. Edge Cases & Pitfalls

1. **Single Element Array**: `[5]` -> returns `[5]`. Loop condition `range(1, N)` does not execute.
2. **Negative Values & Zeros**: `[3, -1, 0, -2, 4]` -> correctly yields `[3, 2, 2, 0, 4]`.
3. **Integer Overflow Constraints**:
   - Max possible sum: $1000 \times 10^6 = 10^9$.
   - $10^9$ fits safely within standard 32-bit signed integer limits ($\approx 2.14 \times 10^9$).
   - If constraints expanded to $N = 10^6$ and $\text{nums}[i] = 10^9$, sums reach $10^{15}$,
     requiring 64-bit integers (`int64` / `long long`).
4. **Input Mutation Side-Effects**:
   - In-place algorithms mutate input data, which violates immutability contracts in thread-safe
     or functional pipelines. Always clarify API expectations during interviews.

---

## 5. 5 YOE Senior Technical Interview Q&A

### Q1: How would you maintain a running sum if elements in the array are updated dynamically?
**Answer**:
If the array elements undergo frequent dynamic updates alongside range sum queries:
- A static prefix sum array requires $\mathcal{O}(N)$ time per update.
- **Fenwick Tree (Binary Indexed Tree)** or **Segment Tree** reduces both point updates and
  prefix sum queries to $\mathcal{O}(\log N)$ time.
- Space complexity remains $\mathcal{O}(N)$, making it optimal for dynamic array sum streams.

---

### Q2: What are the trade-offs between In-Place vs Out-of-Place running sum implementations?
**Answer**:
- **In-Place**: $\mathcal{O}(1)$ auxiliary space. Ideal when memory allocation overhead is costly
  and input array destruction is permitted.
- **Out-of-Place**: $\mathcal{O}(N)$ auxiliary space. Preserves original input for concurrent
  readers, telemetry, or replay buffers. Prevents subtle race conditions in multi-threaded code.

---

### Q3: How do parallel algorithms calculate prefix sums across GPU worker threads?
**Answer**:
Parallel prefix sum (Scan) uses two primary GPU algorithms:
1. **Hillis-Steele Scan**: Performs scan in $\mathcal{O}(\log N)$ steps with $\mathcal{O}(N \log N)$
   total work. Simple but work-inefficient.
2. **Blelloch Scan**: Work-efficient algorithm using two tree phases:
   - *Up-Sweep (Reduce)*: Builds partial sums bottom-up to root ($\mathcal{O}(N)$ work).
   - *Down-Sweep*: Distributes partial sums top-down to leaves ($\mathcal{O}(\log N)$ steps).
   Total work is $\mathcal{O}(N)$, matching sequential optimal complexity.

---

### Q4: How can CPU SIMD instructions accelerate prefix sum calculation?
**Answer**:
Sequential dependency ($S[i] = S[i-1] + A[i]$) limits naive vectorization. SIMD acceleration uses:
1. **Vector Shift & Add**: Perform partial additions across SIMD lanes (AVX2/AVX-512).
2. **Block Parallelization**: Divide array into chunks of size $B$, compute local SIMD prefix sums
   for each chunk in parallel, calculate chunk totals, and apply scalar offsets to chunks.

---

### Q5: What follow-up questions might an interviewer ask?
- **Follow-up 1**: How to find 2D matrix prefix sum for subgrid queries in $\mathcal{O}(1)$ time?
  - *Answer*: Use inclusion-exclusion $P[r][c] = A[r][c] + P[r-1][c] + P[r][c-1] - P[r-1][c-1]$.
- **Follow-up 2**: How to check if any contiguous subarray sums to $K$?
  - *Answer*: Store prefix sums in Hash Map; check if $(S[i] - K)$ exists in $\mathcal{O}(N)$ time.
