# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="seth"
__date__ ="$Jun 29, 2012 6:33:35 PM$"


# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes
# a string as input and returns the i and j indices that
# correspond to the beginning and end indices of the longest
# palindrome in the string.
#
# Grading Notes:
#
# You will only be marked correct if your function runs
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    i, j = 0,1
    li = lj = 0
    if len(text) < 2:
        return (0,0)
    while j < len(text):
        while  i >= 0 and j < len(text) and text[i].lower() == text[j].lower():
            if (j - i) > (lj - li):
#                print 'assigning : ', (i, j)
                li, lj = i, j
            i -= 1
            j += 1
        if (j - i > 1):
            i += 1
        else:
            j += 1
        print (i, j)
#    print 'returning', (li, lj + 1)
    return (li, lj + 1)

def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print test()


if __name__ == "__main__":
    print test();



