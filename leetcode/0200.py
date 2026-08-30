"""
200. Number of Islands
Medium

Given an m x n 2D binary grid grid which represents a map of '1's (land) and
'0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands
horizontally or vertically. You may assume all four edges of the grid are all
surrounded by water.

Example 1:
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1

Example 2:
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3

Constraints:
m == grid.length
n == grid[i].length
1 <= m, n <= 300
grid[i][j] is '0' or '1'.
"""

from collections import deque
from typing import List


class UnionFind:
    """
    Disjoint Set Union (DSU) data structure with Path Compression and Union by Rank.
    """

    def __init__(self, grid: List[List[str]]) -> None:
        """
        Initializes parent and rank arrays, counting initial land components.
        """

        m, n = len(grid), len(grid[0])
        self.parent = [i for i in range(m * n)]
        self.rank = [0] * (m * n)
        self.count = 0

        for r in range(m):
            for c in range(n):
                if grid[r][c] == "1":
                    self.count += 1

    def find(self, i: int) -> int:
        """
        Finds the root representative of element i with path compression.
        """

        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> None:
        """
        Unions the sets containing elements i and j using union by rank.
        """

        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            self.count -= 1


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Counts connected land components using Depth-First Search (DFS).

        Approach:
        1. Iterate through each cell (r, c) in the m x n grid.
        2. When encountering unvisited land ('1'), increment island count.
        3. Trigger recursive DFS to traverse and mark ('sink') all connected 4-directional
           land cells to '0'.

        Time Complexity: O(M * N) where M is rows and N is cols.
        Space Complexity: O(M * N) in worst-case recursion call stack (e.g., all land grid).
        """

        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        island_count = 0

        def dfs(r: int, c: int) -> None:
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
                return
            grid[r][c] = "0"
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    island_count += 1
                    dfs(r, c)

        return island_count

    def numIslands_bfs(self, grid: List[List[str]]) -> int:
        """
        Counts connected land components using Breadth-First Search (BFS) with a queue.

        Approach:
        1. Iterate through each cell (r, c) in the m x n grid.
        2. When encountering unvisited land ('1'), increment island count.
        3. Push (r, c) into a queue and mark as '0' immediately to avoid duplicate enqueues.
        4. Drain queue while checking all 4 orthogonal directions.

        Time Complexity: O(M * N)
        Space Complexity: O(min(M, N)) queue memory for BFS boundary.
        """

        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        island_count = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    island_count += 1
                    grid[r][c] = "0"
                    queue = deque([(r, c)])

                    while queue:
                        curr_r, curr_c = queue.popleft()
                        for dr, dc in directions:
                            nr, nc = curr_r + dr, curr_c + dc
                            if (
                                0 <= nr < rows
                                and 0 <= nc < cols
                                and grid[nr][nc] == "1"
                            ):
                                grid[nr][nc] = "0"
                                queue.append((nr, nc))

        return island_count

    def numIslands_union_find(self, grid: List[List[str]]) -> int:
        """
        Counts connected land components using Disjoint Set Union (DSU / Union-Find).

        Approach:
        1. Initialize UnionFind structure with each land cell as an individual component.
        2. For each land cell, perform union with adjacent right and down land neighbors.
        3. Return final connected component count.

        Time Complexity: O(M * N * alpha(M * N)) approx O(M * N).
        Space Complexity: O(M * N) for parent and rank arrays.
        """

        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        uf = UnionFind(grid)

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    idx = r * cols + c
                    if r + 1 < rows and grid[r + 1][c] == "1":
                        uf.union(idx, (r + 1) * cols + c)
                    if c + 1 < cols and grid[r][c + 1] == "1":
                        uf.union(idx, r * cols + (c + 1))

        return uf.count


def run_test(grid: List[List[str]]) -> None:
    grid_copy = [row[:] for row in grid]
    result = Solution().numIslands(grid_copy)
    print(
        f"grid size=({len(grid)}x{len(grid[0]) if grid else 0}) --> numIslands={result}"
    )


if __name__ == "__main__":
    example1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    example2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    run_test(example1)
    run_test(example2)
