class Solution:
    def findDifferentBinaryString(self, nums: List[str]) -> str:
        ans = ''
        for i in range(len(nums)):
            ans += nums[i][i]
        return "".join(['1' if c == '0' else '0' for c in ans])