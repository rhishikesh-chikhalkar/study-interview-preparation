# Longest Substring Without Repeating Characters (LeetCode 3)

Comprehensive study notes and 5 YOE senior engineering interview guide on the **Variable-Size Sliding Window**, **Hash Set Window Contraction**, and **Hash Map Direct Pointer Jump** techniques for **Longest Substring Without Repeating Characters** (LeetCode 3).

---

## 1. Core Concepts & Mathematical Mechanics

### 1.1 Problem Definition
Given a string `s`, find the length of the longest substring without duplicate characters.

- **Constraints**:
  - $0 \le \text{len}(s) \le 5 \times 10^4$
  - `s` consists of English letters, digits, symbols, and spaces.

---

### 1.2 Sliding Window Mechanics & Invariant
A substring is defined by a contiguous slice $s[\text{left} \dots \text{right}]$.

1. **Window Invariant**:
   - At every step, the substring $s[\text{left} \dots \text{right}]$ must contain zero duplicate characters.
2. **Expansion**:
   - The `right` pointer increments by 1 at each iteration, introducing a candidate character $c = s[\text{right}]$.
3. **Contraction / Adjustment**:
   - If $c$ was already present in the active window (i.e. $\text{last\_seen}[c] \ge \text{left}$), the invariant is violated.
   - **Set Contraction**: Increment `left` one step at a time, removing $s[\text{left}]$ from the set until $c$ is eliminated. Takes at most $2N$ steps.
   - **Direct Map Jump**: Jump `left` directly to $\text{last\_seen}[c] + 1$. Takes strictly $N$ steps.
4. **Pointer Rollback Trap**:
   - For string `"abba"`, when reaching the second `'a'` at index 3:
     - `'a'` was previously seen at index 0.
     - However, the window currently starts at $\text{left} = 2$ (after seeing duplicate `'b'`).
     - Directly updating $\text{left} = \text{last\_seen}['a'] + 1 = 1$ would move the window backward!
     - Formula: $\text{left} = \max(\text{left}, \text{last\_seen}[c] + 1)$.

---

## 2. Algorithm Approaches & Complexity Analysis

### 2.1 Complexity Matrix

| Approach | Time Complexity | Auxiliary Space | Remarks |
| :--- | :--- | :--- | :--- |
| **Brute Force** | $\mathcal{O}(N^3)$ | $\mathcal{O}(\min(N, \Sigma))$ | Check all $\mathcal{O}(N^2)$ substrings for unique characters $\mathcal{O}(N)$. |
| **Sliding Window + Hash Set** | $\mathcal{O}(2N) = \mathcal{O}(N)$ | $\mathcal{O}(\min(N, \Sigma))$ | Left pointer advances incrementally; each char inserted and removed once. |
| **Direct Pointer Jump + Hash Map** | $\mathcal{O}(N)$ | $\mathcal{O}(\min(N, \Sigma))$ | Left pointer jumps immediately to $\max(\text{left}, \text{last\_seen}[c] + 1)$. |
| **Fixed Array Direct Jump** | $\mathcal{O}(N)$ | $\mathcal{O}(\Sigma)$ | For ASCII/extended ASCII ($\Sigma = 128$ or $256$), eliminates hash overhead. |

*$\Sigma$ denotes the size of the alphabet/character set.*

---

### 2.2 Flow Diagram (Direct Jump Hash Map)

```mermaid
flowchart TD
    A[Input: String s] --> B[last_seen = empty dict, left = 0, max_len = 0]
    B --> C[Loop right, char in enumerate s]
    C --> D{char in last_seen and last_seen[char] >= left?}
    D -- Yes --> E[left = last_seen[char] + 1]
    D -- No --> F[Keep left unchanged]
    E --> G[last_seen[char] = right]
    F --> G
    G --> H[max_len = max max_len, right - left + 1]
    H --> I{More characters?}
    I -- Yes --> C
    I -- No --> J[Return max_len]
```

---

## 3. Reference Implementation

```python
from typing import Dict, Set, Tuple


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Optimal Sliding Window with Hash Map (Direct Pointer Jump).
        Time: O(N), Space: O(min(N, Sigma))
        """
        last_seen: Dict[str, int] = {}
        left = 0
        max_length = 0

        for right, char in enumerate(s):
            if char in last_seen and last_seen[char] >= left:
                left = last_seen[char] + 1
            last_seen[char] = right
            current_window_len = right - left + 1
            if current_window_len > max_length:
                max_length = current_window_len

        return max_length

    def lengthOfLongestSubstring_set(self, s: str) -> int:
        """
        Sliding Window with Hash Set (Incremental Contraction).
        Time: O(2N) = O(N), Space: O(min(N, Sigma))
        """
        char_set: Set[str] = set()
        left = 0
        max_length = 0

        for right in range(len(s)):
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
            char_set.add(s[right])
            current_window_len = right - left + 1
            if current_window_len > max_length:
                max_length = current_window_len

        return max_length
```

---

## 4. Common Pitfalls & Edge Cases

1. **Window Contraction Regression (`"abba"` issue)**:
   - When a character is present in `last_seen` but outside the current window (index $< \text{left}$), never retract `left`.
2. **Empty String and Single Character**:
   - `s = ""` must return `0`.
   - `s = " "` (single space) must return `1`.
3. **Symbols and Spaces**:
   - String inputs include characters beyond standard `[a-zA-Z]`. Never assume fixed 26-lowercase alphabet unless explicitly stated in constraints.
4. **All Unique vs All Identical**:
   - `s = "abcdef"` -> `6`.
   - `s = "bbbbb"` -> `1`.

---

## 5. 5 YOE Senior Technical Interview Questions & Answers

### Q1: Compare the Set-based window contraction vs Hash Map direct jump. What are the memory and CPU trade-offs?
**Answer:**
- **Operation Count**: The set approach executes up to $2N$ pointer steps ($N$ expansions by `right`, $N$ contractions by `left`) and two hash operations per character (`add` and `remove`). The direct jump does strictly $N$ iterations and exactly one hash lookup + one insert per character.
- **Cache Locality**: For small charsets like ASCII, direct jump using a 128-element contiguous integer array `int[128]` initialized to `-1` avoids hash collisions, dynamic memory allocations, and pointer dereferences, yielding near-hardware optimal L1 cache line utilization.

### Q2: How would you modify this solution if the problem asked for the longest substring with at most $K$ distinct characters?
**Answer:**
- Maintain a frequency hash map `counts: Dict[str, int]` of characters in the current window.
- Expand `right` and increment `counts[s[right]]`.
- When `len(counts) > K`, contract `left`: decrement `counts[s[left]]`, and `del counts[s[left]]` when frequency reaches `0`.
- The direct jump optimization cannot be applied as easily because removing one character type may require shrinking past multiple distinct characters. Hence, the two-pointer contraction model is the standard approach for at most $K$ distinct characters (LeetCode 340).

### Q3: How would you process an unbounded string stream (e.g. infinite socket stream) where you must report the longest non-repeating window seen so far without storing the entire stream?
**Answer:**
- Store only the active sliding window in memory:
  1. Maintain a double-ended queue (or ring buffer) of active characters and their stream offset.
  2. Maintain a hash map of `last_seen` offsets for characters within the active window.
  3. When an incoming character causes a duplicate, pop elements from the queue front and evict them from the hash map until the duplicate is dropped.
- **Space Complexity**: Bound by the alphabet size $\mathcal{O}(\Sigma)$ rather than the stream length $\mathcal{O}(N)$. Even for Unicode, memory consumption remains strictly bounded regardless of stream duration.

### Q4: Follow-up: How do you adapt this technique to solve LeetCode 424 (Longest Repeating Character Replacement)?
**Answer:**
- Instead of requiring zero duplicates, LeetCode 424 allows replacing up to $k$ characters.
- Condition: $\text{window\_length} - \text{max\_frequency} \le k$.
- Maintain `max_freq` of any single character in the window. If $\text{current\_length} - \text{max\_freq} > k$, slide `left` by 1.
- Crucially, `max_freq` does not need to decrease when shrinking because a smaller window with equal or lesser max frequency can never beat the global maximum recorded so far.
