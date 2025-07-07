# Time Complexity: O(n^2) which is failing on leetcode for large inputs.
class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        start = 0
        end = len(height)
        max_area = 0

        for i in range(len(height)):
            for j in range(i + 1, len(height)):
                print(i, j)
                temp_area = min(height[i], height[j]) * (j - i)
                max_area = max(max_area, temp_area)
                print(max_area)
        return max_area

            
        