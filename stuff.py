# -*- coding: utf-8 -*-
"""
Created on Sun May 27 09:40:26 2018

@author: Henry
"""

def longestValidParentheses(s):
    """
    :type s: str
    :rtype: int
    """
    longest = ""

    for i in range(0, len(s)):
        for j in range(i+1, len(s)):
            temp = s[i:j+1]           
            works = True
            
            n = 0
            for x in temp:
                if x == "(":
                    n+=1
                else:
                    n-=1
                if n < 0:
                    works = False
            if not n==0:
                works = False
            if works and len(temp) > len(longest):
                longest = temp
                
    return longest

print(longestValidParentheses("(())"))