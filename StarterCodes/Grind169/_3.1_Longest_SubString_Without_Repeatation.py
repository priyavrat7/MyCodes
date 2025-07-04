# Time Complexity = O(n)
# At first glance it looks like it could be O(n²) if while runs many times.
# But here’s the key insight:

# 🔷 Each character is added to myset once, and removed from myset once.
# 	•	Each add and remove operation is O(1) (because set in Python is a hash set).
# 	•	Therefore the total number of add/remove operations over the whole string is at most 2n.

# ⸻

# 🔷 ⚡ Why O(n)?

# ✅ Even though the inner while seems nested, it only runs once per unique character, and each character is processed at most twice (once added, once removed).
class Solution(object):
    def lengthOfLongestSubstring(self, s):
        myset = set()
        left = 0
        max_len = 0

        for i in range(len(s)):
            while s[i] in myset:
                myset.remove(s[left])
                left += 1
            myset.add(s[i])
            max_len = max(max_len, i - left + 1)
        return(max_len)
    

