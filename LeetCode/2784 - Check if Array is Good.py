from collections import Counter
class Solution:
    def isGood(self, nums: List[int]) -> bool:
        hash_map = Counter(nums)
        n = max(nums)
        for i, c in hash_map.items():
            if i!=n and c!=1:
                return False
        if hash_map[n] != 2:
            return False
        if len(nums) != n+1:
            return False
        return True
