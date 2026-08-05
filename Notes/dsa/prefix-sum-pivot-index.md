# Prefix Sum & Pivot Index Pattern

Detailed study notes and 5 YOE interview preparation guide on the **Prefix Sum**
technique and **Pivot Index** problem (LeetCode 724 / Equilibrium Index).

---

## 1. Core Concepts & Mathematical Foundation

### 1.1 Problem Definition
Given an array of integers `nums`, find the **leftmost pivot index** $i$ such that:

$$\sum_{k=0}^{i-1} \text{nums}[k] = \sum_{k=i+1}^{N-1} \text{nums}[k]$$

If $i = 0$, the left sum is defined as `0`. If $i = N - 1$, the right sum is defined as `0`.

---

### 1.2 Mathematical Derivation
Let $S_{\text{total}} = \sum_{k=0}^{N-1} \text{nums}[k]$ be the total sum of all elements.

For any candidate pivot index $i$:
- Let $S_{\text{left}}(i) = \sum_{k=0}^{i-1} \text{nums}[k]$.
- The sum of elements strictly to the right of $i$ is:

$$S_{\text{right}}(i) = S_{\text{total}} - S_{\text{left}}(i) - \text{nums}[i]$$

Setting $S_{\text{left}}(i) = S_{\text{right}}(i)$:

$$S_{\text{left}}(i) = S_{\text{total}} - S_{\text{left}}(i) - \text{nums}[i]$$

$$2 \times S_{\text{left}}(i) + \text{nums}[i] = S_{\text{total}}$$

This algebraic identity eliminates calculating right sums explicitly during iteration.

---

## 2. Algorithm Comparison & Visualizations

### 2.1 Complexity Matrix

| Approach | Time Complexity | Space Complexity | Notes |
| :--- | :--- | :--- | :--- |
| Brute Force | $\mathcal{O}(N^2)$ | $\mathcal{O}(1)$ | Recalculate sums for each index $i$ |
| Prefix Sum Array | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Precompute `prefix_sums[N+1]` array |
| Total Sum Accumulation | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Total sum + running left sum |

---

### 2.2 Execution Flow Diagram

```mermaid
flowchart TD
    A[Start: Array nums] --> B[Calculate Total Sum: total_sum]
    B --> C[Initialize left_sum = 0, index i = 0]
    C --> D{i < N?}
    D -- No --> E[Return -1: No Pivot Found]
    D -- Yes --> F{"Is left_sum == total_sum - left_sum - nums[i]?"}
    F -- Yes --> G[Return Pivot Index i]
    F -- No --> H[left_sum += nums[i]]
    H --> I[i += 1]
    I --> D
```

---

## 3. Python & Go Implementations

### 3.1 Python Implementation (`leetcode/0724.py`)

```python
from typing import List


class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        """
        Finds leftmost pivot index using O(1) space running sum.
        """
        total_sum = sum(nums)
        left_sum = 0

        for i, num in enumerate(nums):
            if left_sum == total_sum - left_sum - num:
                return i
            left_sum += num

        return -1
```

---

### 3.2 Go Implementation

```go
package main

// PivotIndex returns the leftmost pivot index in O(N) time and O(1) space.
func PivotIndex(nums []int) int {
	totalSum := 0
	for _, v := range nums {
		totalSum += v
	}

	leftSum := 0
	for i, num := range nums {
		if leftSum == totalSum-leftSum-num {
			return i
		}
		leftSum += num
	}

	return -1
}
```

---

## 4. Edge Cases & Common Pitfalls

1. **Edge Pivots ($i=0$ or $i=N-1$)**:
   - Array `[2, 1, -1]`: Total sum = `2`. Index 0 has $S_{\text{left}} = 0$ and
     $S_{\text{right}} = 1 + (-1) = 0$. Pivot index is `0`.
2. **Negative Numbers & Zero-Sum Arrays**:
   - `[-1, -1, 0, 1, 1, 0]`: Pivot index is `5` ($S_{\text{left}} = 0$, $S_{\text{right}} = 0$).
   - Negative elements mean prefix sums are non-monotonic; binary search does not apply.
3. **Single Element Array**:
   - `[5]`: Total sum = `5`, $S_{\text{left}} = 0$, $S_{\text{right}} = 0$. Pivot index is `0`.
4. **Integer Overflow in Statically Typed Languages**:
   - For $N = 10^5$ and $\text{nums}[i] = 10^9$, total sum exceeds 32-bit signed
     integer limits ($2^{31}-1 \approx 2.14 \times 10^9$).
     Use 64-bit integers (`int64` in Go, `long long` in C++).

---

## 5. Interview Questions & Answers (5 YOE Level)

### Question 1: Conceptual / Trade-offs
**Q**: How does Prefix Sum scale for range sum queries vs dynamic updates?
Compare $\mathcal{O}(N)$ precomputation vs. Fenwick Tree / Segment Tree.

**Answer**:
- **Static Array with Multiple Range Queries**:
  - Precomputing prefix sum array $P[i] = \sum_{k=0}^{i-1} \text{nums}[k]$ takes
    $\mathcal{O}(N)$ time and $\mathcal{O}(N)$ space.
  - Range sum query $\text{sum}(L, R)$ takes $\mathcal{O}(1)$ time: $P[R + 1] - P[L]$.
  - **Limitation**: Updating a single element in `nums` takes $\mathcal{O}(N)$ time
    to recompute the prefix array.
- **Dynamic Array (Frequent Point Updates & Range Sum Queries)**:
  - Use a **Fenwick Tree (Binary Indexed Tree)** or **Segment Tree**.
  - **Query Time**: $\mathcal{O}(\log N)$.
  - **Update Time**: $\mathcal{O}(\log N)$.
  - **Space**: $\mathcal{O}(N)$.
- **Interview Follow-up**: *How would you adapt Pivot Index if values update dynamically
  in a streaming system?*
  - Maintain a Fenwick Tree for dynamic prefix sum range queries, allowing dynamic
    pivot lookup in $\mathcal{O}(\log N)$ per search step using binary lifting.

---

### Question 2: Practical / Scenario-based
**Q**: In a distributed database partition engine, how can the Equilibrium Index
concept be applied to balance workload across worker nodes?

**Answer**:
- **Scenario**: Shards stored on nodes $0 \dots N-1$ host weights $W[i]$
  (CPU utilization or storage size).
- **Application**:
  1. Find partition point (equilibrium index) where left worker cluster sum equals
     right worker cluster sum to split tasks evenly across database replicas.
  2. If exact equality is rare, modify condition to minimize $|S_{\text{left}} - S_{\text{right}}|$
     (Subarray Sum Difference Minimization).
- **Interview Follow-up**: *What if node weights $W[i]$ can be negative?*
  - The prefix sum sequence is non-monotonic, so binary search / two-pointer
    contraction cannot be applied directly. We must use prefix sum maps or linear scans.

---

### Question 3: System Design / Architecture
**Q**: How is 2D Prefix Sum (Summed-Area Table) used in image processing and spatial
database range queries?

**Answer**:
- **Definition**: A 2D Prefix Sum array $SAT[r][c]$ stores the sum of all pixels
  in the subrectangle from $(0, 0)$ to $(r, c)$:

$$SAT[r][c] = \text{val}[r][c] + SAT[r-1][c] + SAT[r][c-1] - SAT[r-1][c-1]$$

- **Query**: The sum of subrectangle $(r1, c1)$ to $(r2, c2)$ is computed in $\mathcal{O}(1)$ time:

$$\text{Sum} = SAT[r2][c2] - SAT[r1-1][c2] - SAT[r2][c1-1] + SAT[r1-1][c1-1]$$

- **Architectural Utility**:
  - Used in computer vision (Box blur, Viola-Jones object detection).
  - Used in GIS spatial databases for rapid 2D bounding box density calculations.
- **Interview Follow-up**: *What are memory locality implications for massive datasets?*
  - Compute in block-tiled memory layouts or write chunked parallel MapReduce jobs
    to avoid cache line invalidation and page faults.

---

## 6. References & Further Reading

- [LeetCode 724: Find Pivot Index](https://leetcode.com/problems/find-pivot-index/)
- [GeeksforGeeks: Equilibrium Index](https://www.geeksforgeeks.org/equilibrium-index-of-an-array/)
- [Fenwick Tree / Binary Indexed Tree](https://cp-algorithms.com/data_structures/fenwick.html)
