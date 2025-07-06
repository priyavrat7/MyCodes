class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if x < 0:
            return False
        
        else:
            string = str(x)
            rev_string = string[::-1]

            if string == rev_string:
                return True
            else:
                return False
        