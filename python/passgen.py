#!/usr/bin/env python
'''
Password generator that attempts to provide some amount of complexity
 based on the number of character classes used.  Considers upper and
 lower case to be separate character classes.

Author: Maarten Broekman
'''
from __future__ import print_function
# import os
import sys
import getopt
import random
import string

# Constants used to create password alphabet
LCASE = string.ascii_lowercase
UCASE = string.ascii_uppercase
NUMS = string.digits
PUNCS = string.punctuation

def dbg_print(msg, dbg, limit=0):
    """
    Only print if our debug variable exceeds the limit we set
    """
    if dbg > limit:
        print(msg)

def gen_pass(alphabet, classcnt=4, length=32, dbg=0):
    """
    Generate a new password
    """
    mypw = ""
    while chk_pass(alphabet, classcnt, mypw, dbg) < 0:
        mypw = ""
        pwlen = length
        while pwlen > 0:
            next_index = random.randrange(len(alphabet))
            mypw = mypw + alphabet[next_index]
            pwlen -= 1
    print(mypw)

def chk_pass(alphabet, classcnt, password, dbg=0):
    """
    Check to see if the new password meets the complexity requirements
    """
    chk_comp = 0
    foundclass = ""

    for char in password:
        if char in LCASE:
            if classcnt > 0 and LCASE not in foundclass:
                dbg_print("Found lowercase ascii letter", dbg, 0)
                alphabet = alphabet.replace(LCASE, "")
                foundclass = foundclass + LCASE
                chk_comp += 1
        if char in UCASE:
            if classcnt > 1 and UCASE not in foundclass:
                dbg_print("Found uppercase ascii letter", dbg, 0)
                alphabet = alphabet.replace(UCASE, "")
                foundclass = foundclass + UCASE
                chk_comp += 1
        if char in NUMS:
            if classcnt > 2 and NUMS not in foundclass:
                dbg_print("Found number", dbg, 0)
                alphabet = alphabet.replace(NUMS, "")
                foundclass = foundclass + NUMS
                chk_comp += 1
        if char in PUNCS:
            if classcnt > 3 and PUNCS not in foundclass:
                dbg_print("Found punctuation", dbg, 0)
                alphabet = alphabet.replace(PUNCS, "")
                foundclass = foundclass + PUNCS
                chk_comp += 1
        if chk_comp >= classcnt:
            dbg_print("Sufficient complexity found.", dbg, 0)
            break
    if chk_comp < classcnt:
        if len(password) > 0 and dbg > 0:
            print('Password lacking complexity. ', end='')
            print('Required complexity: ' + str(classcnt), end=' ')
            print(':: Found complexity: ' + str(chk_comp))
            print('Bad Password: ' + password)
        return -1
    return 0



def get_alphabet(my_puncs, classcnt=4):
    """
    Get the appropriate list of characters to use for password generation
    """
    if classcnt == 1:
        alphabet = LCASE
    if classcnt == 2:
        alphabet = LCASE + UCASE
    if classcnt == 3:
        alphabet = LCASE + UCASE + NUMS
    if classcnt == 4:
        if my_puncs is not None:
            alphabet = LCASE + UCASE + NUMS + my_puncs
        else:
            alphabet = LCASE + UCASE + NUMS + PUNCS

    return alphabet



def chk_length(length, comp):
    """
    Check for proper length vs complexity settings
    """
    if length < comp:
        print('Error: password length ' + str(length), end=' ')
        print('is not long enough to allow for ' + str(comp), end=' ')
        print('character classes.')
        sys.exit()



def strip_excludes(chars, remove):
    """
    Removes a list of characters from another list of characters
    """
    for exclude in remove:
        chars = chars.replace(exclude, "")

    return chars



def main(args):
    """
    Main processing
    """
    try:
        opts, args = getopt.getopt(args, "hd12345i:x:l:")
    except getopt.GetoptError:
        print('passgen.py [-x exclude_char] [-i include_char]', end=' ')
        print('[-h] [-d] [-1|2|3|4|5] [-l length]')
        sys.exit(2)

    exclude = ""
    include = ""
    my_puncs = None
    debug = 0
    for opt, arg in opts:
        if opt == '-h':
            print('passgen.py [-x exclude_char ...] [-h] [-d] [-1|2|3|4|5] [-l length]')
            print('')
            print('-x - Exclude a character.  Can be used multiple times.')
            print('-l - Password length. Defaults to 32.')
            print('-d - Debug mode.  printmore info.')
            print('-1 - Only lowercase letters.')
            print('-2 - Uppercase and lowercase letters.')
            print('-3 - Letters and numbers.')
            print('-4 - Letters, numbers, and .,?/"\':;-_')
            print('-5 - Default. Letters, numbers, and ' + string.punctuation)
            print('')
            sys.exit()
        if opt == '-x':
            exclude = str(arg) + str(exclude)
        if opt == '-i':
            include = str(arg) + str(include)
        if opt == '-1':
            complexity = 1
        if opt == '-2':
            complexity = 2
        if opt == '-3':
            complexity = 3
        if opt == '-4':
            my_puncs = str('.,?/"\':;-_')
            complexity = 4
        if opt == '-5':
            complexity = 4
        if opt == '-l':
            pw_length = int(arg)
        if opt == '-d':
            debug += 1

    chk_length(pw_length, complexity)
    charlist = get_alphabet(my_puncs, complexity)
    dbg_print(charlist, debug, 1)
    charlist = strip_excludes(charlist, exclude)
    charlist = charlist + include
    dbg_print(charlist, debug, 1)
    gen_pass(charlist, complexity, pw_length)



if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Exiting...')
