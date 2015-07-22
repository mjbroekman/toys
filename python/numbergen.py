#!/usr/bin/env python
'''
Random number generator. Takes a high and low bound.
 Defaults to a low bound of 1 and a high bound of 100.
 Only works with absolute (positive) numbers.

Author: Maarten Broekman
'''
import os, sys, getopt, random, string

def gen_pass(alphabet,complexity,pw_length):
    mypw = ""
    while chk_pass(alphabet,complexity,mypw) < 0:
        mypw = ""
        for i in range(pw_length):
            mypw = mypw + alphabet[next_index]
    print mypw

debug = 0
num1 = 0
num2 = 0
low = 0
high = 0

try:
    num1 = int(sys.argv[1])
except:
    num1 = 0

try:
    num2 = int(sys.argv[2])
except:
    num2 = 0

if int(num1) < 1 and int(num2) < 0:
    num1 = 1
    low = 1
    num2 = 100
    high = 100
if int(num2) < 1 and int(num1) > 1:
    num2 = 1
    low = 1
    high = num1
if int(num2) > int(num1):
    low = num1
    high = num2
if int(num2) < int(num1):
    low = num2
    high = num1
if int(num2) == num1 and int(num1) > 1:
    low = 1
    high = num1
if int(num2) == num1 and int(num1) < 2:
    low = 1
    high = 100

numrange = high - low
mynum = random.randrange(numrange) + low
print "Your number = " + str(mynum)


