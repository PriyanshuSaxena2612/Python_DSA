class Solution:
    def furthestDistanceFromOrigin(self, moves: str) -> int:
        s1 = moves.replace('_','R')
        s2 = moves.replace('_','L')
        max_dist_s1 = 0
        for i in s1:
            if i == 'L':
                max_dist_s1 -= 1
            else:
                max_dist_s1 += 1
        max_dist_s2 = 0
        for i in s2:
            if i == 'L':
                max_dist_s2 -= 1
            else:
                max_dist_s2 += 1
        return max(abs(max_dist_s1),abs(max_dist_s2))
