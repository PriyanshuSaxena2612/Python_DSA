class Solution:
    def minimumEffort(self, tasks: List[List[int]]) -> int:
        tasks.sort(key = lambda x: x[1] - x[0], reverse = True)
        total, curr = 0, 0
        for actual, minimum in tasks:
            if curr < minimum:
                extra = minimum - curr
                total += extra
                curr += extra
            curr -= actual
        return total
