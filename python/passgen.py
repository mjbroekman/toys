#!/usr/bin/env python
'''
Password generator that attempts to provide some amount of complexity
 based on the number of character classes used.  Considers upper and
 lower case to be separate character classes.

Author: Maarten Broekman
'''
import os, sys, getopt, random, string

def gen_pass(alphabet,complexity,pw_length):
    mypw = ""
    while chk_pass(alphabet,complexity,mypw) < 0:
        mypw = ""
        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            mypw = mypw + alphabet[next_index]
    print mypw

def chk_pass(alphabet,complexity,password):
    chk_comp = 0
    global debug

    for c in password:
        if c in class1:
            if alphabet.find(class1) > -1:
                if debug > 0:
                    print "Found lowercase ascii letter"
                alphabet = alphabet.replace(class1,"")
                chk_comp += 1
        if c in class2:
            if alphabet.find(class2) > -1:
                if debug > 0:
                    print "Found uppercase ascii letter"
                alphabet = alphabet.replace(class2,"")
                chk_comp += 1
        if c in class3:
            if alphabet.find(class3) > -1:
                if debug > 0:
                    print "Found number"
                alphabet = alphabet.replace(class3,"")
                chk_comp += 1
        if c in class4:
            if alphabet.find(class4) > -1:
                if debug > 0:
                    print "Found punctuation"
                alphabet = alphabet.replace(class4,"")
                chk_comp += 1
        if chk_comp >= complexity:
            if debug > 0:
                print "Sufficient complexity found."
            break
    if chk_comp < complexity:
        if len(password) > 0 and debug > 0:
            print "Password lacking complexity. Required complexity: " + str(complexity) + " :: Found complexity: " + str(chk_comp)
            print "Bad Password: " + password
        return -1
    return 0


try:
    opts, args = getopt.getopt(sys.argv[1:],"hd12345x:l:")
except getopt.GetoptError:
    print 'passgen.py [-x exclude_char] [-h] [-d] [-1|2|3|4|5] [-l length]'
    sys.exit(2)

# Default password length
pw_length = 32
alphabet = ""
exclude_chars = ""
mypw = ""
class1 = string.ascii_lowercase
class2 = string.ascii_uppercase
class3 = string.digits
class4 = string.punctuation
complexity = 4
debug = 0

for opt, arg in opts:
    if opt == '-h':
        print 'passgen.py -x exclude_char [-h] [-d] [-1|2|3|4] -l length'
        print ''
        print '-x - Exclude a character.  Can be used multiple times.'
        print '-l - Password length. Defaults to 32.'
        print '-d - Debug mode.  Print more info.'
        print '-1 - Only lowercase letters.'
        print '-2 - Uppercase and lowercase letters.'
        print '-3 - Letters and numbers.'
        print '-4 - Letters, numbers, and .,?/"\':;-_'
        print '-5 - Default. Letters, numbers, and ' + string.punctuation
        print ''
        sys.exit()
    if opt == '-x':
        exclude_chars = str(arg) + str(exclude_chars)
    if opt == '-1':
        complexity = 1
    if opt == '-2':
        complexity = 2
    if opt == '-3':
        complexity = 3
    if opt == '-4':
        class4 = str('.,?/"\':;-_')
        complexity = 4
    if opt == '-5':
        complexity = 4
    if opt == '-l':
        pw_length = int(arg)
    if opt == '-d':
        debug += 1

if pw_length < complexity:
    print "Error: password length " + str(pw_length) + " isn't enough to allow for " + str(complexity) + " character classes."
    sys.exit()

if complexity == 1:
    alphabet = class1
if complexity == 2:
    alphabet = class1 + class2
if complexity == 3:
    alphabet = class1 + class2 + class3
if complexity == 4:
    alphabet = class1 + class2 + class3 + class4

if debug > 1:
    print alphabet

new_alph = alphabet
for e in exclude_chars:
    new_alph = new_alph.replace(e,"");

alphabet = new_alph

if debug > 1:
    print alphabet

gen_pass(alphabet,complexity,pw_length)