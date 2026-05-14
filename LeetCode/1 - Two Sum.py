class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
      # first method
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i,j]
      # second method 
      hash_map = {}
        n = len(nums)
        for i in range(n):
            remaining = target - nums[i]
            if remaining in hash_map:
                return [hash_map[remaining],i]
            hash_map[nums[i]] = i
