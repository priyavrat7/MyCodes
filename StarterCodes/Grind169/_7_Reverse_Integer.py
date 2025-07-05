class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        if x == 0:
            return 0

        elif x > 0:
            num_str = str(x)
            rev_num = num_str[::-1]
            number = int(rev_num)
        
        else:
            num_str = str(x)
            num_str = num_str[1:len(num_str)]
            rev_num = num_str[::-1]
            number = -1 * int(rev_num)
        
        print(number)
        if number > 2**31 -1 or number < ((-1) * 2**31):
            return 0
        else:
            return(number)
        