#!/usr/bin/env python3
'''
Password generator that attempts to provide some amount of complexity
 based on the number of character classes used.  Considers upper and
 lower case to be separate character classes.

Author: Maarten Broekman
'''
# from __future__ import print_function
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

debug = 0

def dbg_print(message, limit=0):
    """Only print if our debug variable exceeds the limit we set

    Args:
        message: message to print
        limit: optional debug limit for varying levels of verbosity
    
    Returns:
        None
    """
    if debug > limit:
        print(message)


def gen_pass(alphabet, class_count=4, length=64):
    """Generate a new password

    Args:
        alphabet: character set to use for creating a password
        class_count: number of required character classes (defaults to 4 classes)
        length: password length (defaults to 64 characters)
    
    Returns:
        String (password)
    """
    new_password = ""
    while chk_pass(alphabet, class_count, new_password) is False:
        new_password = ""
        password_length = length
        while password_length > 0:
            next_index = random.randrange(len(alphabet))
            new_password = new_password + alphabet[next_index]
            password_length -= 1

    return new_password


def chk_pass(alphabet, class_count, password):
    """Check to see if the new password meets the complexity requirements

    Args:
        alphabet: password character alphabet
        class_count: number of required character classes
        password: password to check
    
    Returns:
        Bool (True / False)
    """
    complexity_chk = 0
    found_classes = ""

    for char in password:
        if char in LCASE:
            if class_count > 0 and LCASE not in found_classes:
                dbg_print("Found lowercase ascii letter", 0)
                alphabet = alphabet.replace(LCASE, "")
                found_classes = found_classes + LCASE
                complexity_chk += 1

        if char in UCASE:
            if class_count > 1 and UCASE not in found_classes:
                dbg_print("Found uppercase ascii letter", 0)
                alphabet = alphabet.replace(UCASE, "")
                found_classes = found_classes + UCASE
                complexity_chk += 1

        if char in NUMS:
            if class_count > 2 and NUMS not in found_classes:
                dbg_print("Found number", 0)
                alphabet = alphabet.replace(NUMS, "")
                found_classes = found_classes + NUMS
                complexity_chk += 1

        if char in PUNCS:
            if class_count > 3 and PUNCS not in found_classes:
                dbg_print("Found punctuation", 0)
                alphabet = alphabet.replace(PUNCS, "")
                found_classes = found_classes + PUNCS
                complexity_chk += 1

        if complexity_chk >= class_count:
            dbg_print("Sufficient complexity found.", 0)
            break

    if complexity_chk < class_count:
        if len(password) > 0 and debug > 0:
            print('Password lacking complexity. ', end='')
            print('Required complexity: ' + str(class_count), end=' ')
            print(':: Found complexity: ' + str(complexity_chk))
            print('Bad Password: ' + password)

        return False

    return True


def get_alphabet(punct_list, class_count=4):
    """Get the appropriate list of characters to use for password generation

    Args:
        punct_list: List of acceptable punc
    """
    if class_count == 1:
        alphabet = LCASE
    if class_count == 2:
        alphabet = LCASE + UCASE
    if class_count == 3:
        alphabet = LCASE + UCASE + NUMS
    if class_count == 4:
        if punct_list is not None:
            alphabet = LCASE + UCASE + NUMS + punct_list
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
    global debug

    try:
        opts, args = getopt.getopt(args, "hd12345i:x:l:")
    except getopt.GetoptError:
        print('passgen.py [-x exclude_char] [-i include_char]', end=' ')
        print('[-h] [-d] [-1|2|3|4|5] [-l length]')
        sys.exit(2)

    exclude = ""
    include = ""
    punct_list = None
    complexity = 4
    for opt, arg in opts:
        if opt == '-h':
            print('passgen.py [-x exclude_char ...] [-h] [-d] [-1|2|3|4|5] [-l length]\n')
            print('-x - Exclude a character.  Can be used multiple times.')
            print('-l - Password length. Defaults to 32.')
            print('-d - Debug mode.  printmore info.')
            print('-1 - Only lowercase letters.')
            print('-2 - Uppercase and lowercase letters.')
            print('-3 - Letters and numbers.')
            print('-4 - Letters, numbers, and .,?/"\':;-_')
            print('-5 - Default. Letters, numbers, and ' + string.punctuation)
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
            punct_list = str('.,?/"\':;-_')
            complexity = 4
        if opt == '-5':
            complexity = 4
        if opt == '-l':
            pw_length = int(arg)
        if opt == '-d':
            debug += 1

    chk_length(pw_length, complexity)
    charlist = get_alphabet(punct_list, complexity)
    dbg_print(charlist, 1)
    charlist = strip_excludes(charlist, exclude)
    charlist = charlist + include
    dbg_print(charlist, 1)
    gen_pass(charlist, complexity, pw_length)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Exiting...')
