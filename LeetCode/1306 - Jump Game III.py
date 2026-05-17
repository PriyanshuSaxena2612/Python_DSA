class Solution:
    def canReach(self, arr: List[int], start: int, visited = None) -> bool:
      """
        Logic: It's either a i + arr[i] or i - arr[i], hence a recursion tree will form
        Why visited? So it doesn't fall in an infinite loop of getting to same index again
        SC: O(n)
        TC: O(n) -> Because each node is visited once
      """
        if visited is None:
            visited = set()
        if start >= len(arr) or start < 0:
            return False
        if arr[start] == 0:
            return True
        if start in visited:
            return False
        visited.add(start)
        return (self.canReach(arr, start + arr[start], visited) or self.canReach(arr, start - arr[start], visited))
