# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="seth"
__date__ ="$Jul 11, 2012 9:30:56 PM$"


#Complete the variance function to make it return the variance of a list of numbers
data3=[13.04, 1.32, 22.65, 17.44, 29.54, 23.22, 17.65, 10.12, 26.73, 16.43]
def mean(data):
    return sum(data)/len(data)
def variance(data):
    m = mean(data)
    return sum([(d - m)**2 for d in data])/len(data)


print variance(data3)

