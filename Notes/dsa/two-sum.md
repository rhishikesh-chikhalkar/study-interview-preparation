# Two Sum (LeetCode 1)

Comprehensive study notes and 5 YOE senior engineering interview guide on the **Hash Map Lookup**, **Two Pointers with Sorting**, and **Complement Search** techniques for **Two Sum** (LeetCode 1).

---

## 1. Core Concepts & Mathematical Foundation

### 1.1 Problem Definition
Given an integer array `nums` and an integer `target`, return indices `[i, j]` of the two numbers such that:
- $i \neq j$
- $\text{nums}[i] + \text{nums}[j] = \text{target}$
- Exactly one valid solution exists.

$$\text{complement}_i = \text{target} - \text{nums}[i]$$

- **Constraints**:
  - $2 \le N \le 10^4$
  - $-10^9 \le \text{nums}[i] \le 10^9$
  - $-10^9 \le \text{target} \le 10^9$
  - Only one valid answer exists.

---

### 1.2 Mathematical & Algorithmic Mechanics

1. **Complement Equation**:
   - For every element $x = \text{nums}[i]$, there is an exact complementary value $y = \text{target} - x$ needed.
2. **Hash Table Lookup**:
   - Instead of scanning the remaining array linearly in $\mathcal{O}(N)$ time to find $y$, a hash map lookup checks for existence in $\mathcal{O}(1)$ average time.
3. **Single Pass Construction**:
   - Storing each element as it is visited guarantees that any element is only paired with an earlier element, naturally avoiding using the same element twice ($i \neq j$).

---

## 2. Algorithm Approaches & Complexity Analysis

### 2.1 Complexity Matrix

| Approach | Time Complexity | Auxiliary Space | Remarks |
| :--- | :--- | :--- | :--- |
| **Brute Force (Nested Loops)** | $\mathcal{O}(N^2)$ | $\mathcal{O}(1)$ | Checks all pairs $(i, j)$ where $i < j$. |
| **Two-Pass Hash Map** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Pass 1 builds index map; Pass 2 checks complement $\neq i$. |
| **Two Pointers + Sorting** | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N)$ | Sorts $(num, index)$ pairs; two pointers inward. |
| **One-Pass Hash Map (Optimal)** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Builds map dynamically and checks complement in a single pass. |

---

### 2.2 Flow Diagram (One-Pass Hash Map)

```mermaid
flowchart TD
    A[Input: nums, target] --> B[seen = empty hash map]
    B --> C[Loop i, num in enumerate nums]
    C --> D[complement = target - num]
    D --> E{complement in seen?}
    E -- Yes --> F[Return seen[complement], i]
    E -- No --> G[seen[num] = i]
    G --> H{More elements?}
    H -- Yes --> C
    H -- No --> I[Return empty list]
```

---

## 3. Reference Implementation

```python
from typing import Dict, List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        One-Pass Hash Map (Optimal).
        Time: O(N), Space: O(N)
        """
        seen: Dict[int, int] = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []

    def twoSum_two_pointers(self, nums: List[int], target: int) -> List[int]:
        """
        Two Pointers with Index Sorting.
        Time: O(N log N), Space: O(N)
        """
        indexed_nums = sorted((num, i) for i, num in enumerate(nums))
        left, right = 0, len(nums) - 1

        while left < right:
            current_sum = indexed_nums[left][0] + indexed_nums[right][0]
            if current_sum == target:
                return [indexed_nums[left][1], indexed_nums[right][1]]
            if current_sum < target:
                left += 1
            else:
                right -= 1

        return []
```

---

## 4. Common Pitfalls & Edge Cases

1. **Reusing the Same Element**:
   - If `target = 6` and `nums = [3, 2, 4]`, picking index `0` twice ($3 + 3 = 6$) is invalid.
   - Handled in One-Pass because $3$ is only inserted into the hash table *after* checking if its complement exists in `seen`.
2. **Duplicate Elements**:
   - If `target = 6` and `nums = [3, 3]`, both indices `[0, 1]` must be returned.
   - In Two-Pass, the second 3 overwrites the map's index if not carefully indexed. In One-Pass, the second 3 finds the first 3 already in `seen` and returns `[0, 1]` immediately.
3. **Integer Overflow in Other Languages**:
   - In languages like C++/Java, `target - num` could overflow if values are near `INT_MIN` or `INT_MAX`. Python handles arbitrarily large integers automatically.

---

## 5. 5 YOE Senior Interview Questions & Answers

### Q1: Why is Two Pointers not $\mathcal{O}(1)$ auxiliary space for Two Sum when index return is required?
**Answer:**
Two Pointers requires a sorted array. If we sort `nums` in place, original indices are lost. To preserve the original indices, we must allocate an array of tuples `(value, original_index)` or an index permutation array, requiring $\mathcal{O}(N)$ extra space. If the problem only asked whether a pair exists or returned the values themselves (as in LeetCode 167 - Two Sum II), Two Pointers would achieve $\mathcal{O}(1)$ auxiliary space.

### Q2: How would you scale Two Sum if `nums` contains 10 billion integers distributed across multiple nodes?
**Answer:**
For massive distributed datasets:
1. **Partitioning by Hash / Range**: Partition values by a hash function or key ranges across worker nodes.
2. **Distributed Hash Table (DHT)**:
   - For each element $x$ on a worker node, compute $y = \text{target} - x$.
   - Route lookup requests for $y$ to the partition responsible for storing key range $y$.
3. **MapReduce Approach**:
   - Map phase: Emit `(min(x, target - x), (x, original_id))` so both $x$ and its complement hash to the same reducer key.
   - Reduce phase: Reducer checks if matching pairs exist and outputs their IDs.

### Q3: What happens to the One-Pass Hash Map in the worst-case hash collision scenario?
**Answer:**
If adversarial input causes all values to collide into the same hash bucket (e.g. hash flooding), lookup degrades from $\mathcal{O}(1)$ average to $\mathcal{O}(N)$ per lookup, making total time complexity $\mathcal{O}(N^2)$.
- Modern Python (3.6+) uses SipHash / randomized hash seeds per process to mitigate predictable collisions.
- In systems where deterministic collision safety is required, balanced BSTs (like C++ `std::map`) guarantee $\mathcal{O}(N \log N)$ worst-case time.

### Q4: Follow-up: How do you extend this pattern to 3Sum, 4Sum, and k-Sum?
**Answer:**
- **3Sum**: Sort the array in $\mathcal{O}(N \log N)$, fix one element $nums[i]$, and solve Two Sum on the remaining subarray using Two Pointers in $\mathcal{O}(N)$, giving $\mathcal{O}(N^2)$ total.
- **k-Sum Generalization**: Recursively reduce $k$-Sum to $(k-1)$-Sum by fixing the outer loop element until $k=2$ (Two Sum with Two Pointers on sorted array). Time complexity is $\mathcal{O}(N^{k-1})$.
