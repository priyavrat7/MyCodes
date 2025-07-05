class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        if len(s) == 0 or len(s) == 1:
            return s

        palindrome_sub_string = ""
        def expand_around_center(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return s[left + 1:right] 
            # for "abcba" case, (left, right) -> (1, 3) -> (0, 4) -> (-1, 5)
            # for "abba" case, (left, right) -> (1, 2) -> (0, 3) -> (-1, 4)

        for i in range(len(s)):
            odd_palindrome = expand_around_center(i, i)    # "abcba"
            even_palindrome = expand_around_center(i, i+1) # "abba"

            if len(odd_palindrome) > len(palindrome_sub_string):
                palindrome_sub_string = odd_palindrome
            
            if len(even_palindrome) > len(palindrome_sub_string):
                palindrome_sub_string = even_palindrome

        return palindrome_sub_string

               