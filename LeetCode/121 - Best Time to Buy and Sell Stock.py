class Solution:
    def maxProfit(self, prices: List[int]) -> int:
      """
      Method 1: Brute Force Approach
      Logic: 
        * Move pointer i from start to end, while j from i to end
        * calculate the difference, and return the max of difference of all
      TC: O(N^2)
      SC: O(1)
      """
        max_ = float('-inf')
        for i in range(len(prices)):
            diff = 0
            for j in range(i, len(prices)):
                diff = prices[j] - prices[i]
                max_ = max(max_, diff)
        return max_
        """
        Method 2: Optimal Approach
        Logic:
          * Find the running minimum
          * If not the minimum, calculate the difference, and return the max of it
        Trap: The use of else with if, remember only to use else when either-or condition, otherwise skip else when both needed
        TC: O(N)
        SC: O(1)
        """
        max_profit = float('-inf')
        min_price = prices[0]
        current_price = 0
        for i in range(1, len(prices)):
            if prices[i] < min_price:
                min_price = prices[i]
            max_profit = max(max_profit, prices[i] - min_price)
        return max(max_profit,0)
