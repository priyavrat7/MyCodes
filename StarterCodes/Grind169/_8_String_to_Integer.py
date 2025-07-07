class Solution(object):
    def myAtoi(self, s):
        """
        :type s: str
        :rtype: int
        """
        # Ascii of "0" is 48
        # Ascii of " " is 32
        # Ascii of "-" is 45
        #s = "   +0 123"
        #s = s.replace(" ", "")
        
        s = s.strip()  # Remove leading/trailing spaces
        if not s:
            return 0

        sign = 1
        idx = 0
        if s[0] == '-':
            sign = -1
            idx += 1
        elif s[0] == '+':
            idx += 1

        num = 0
        while idx < len(s) and s[idx].isdigit():
            #print(num)
            num = num * 10 + int(s[idx])
            idx += 1

        final = sign * num

        if final > 2**31 - 1:
            return 2**31 - 1
        
        elif final < -1 * (2**31):
            return -1 * (2**31)

        else:
            return sign * num        