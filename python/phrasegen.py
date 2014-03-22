#!/usr/bin/env python
'''
Passphrase generator.  Uses the local dictionary to pull words or phrases.

Author: Maarten Broekman
'''
import os, sys, getopt, random, string

try:
    opts, args = getopt.getopt(sys.argv[1:],"w:l:")
except getopt.GetoptError:
    print 'phrasegen.py [-w number of words] [-l minimum character length]'
    sys.exit(2)

# Default password length
pw_length = 32
num_words = 5
password = ""

for opt, arg in opts:
    if opt == '-h':
        print 'phrasegen.py [-w number of words] [-l minimum character length]'
        print ''
        print '-l - Minimum Character length. Defaults to 32.'
        print '-w - Minimum Number of Words. Defaults to 5.'
        print '-d - Debug mode.  Print more info.'
        print ''
        sys.exit()
    if opt == '-w':
        num_words = int(arg)
    if opt == '-l':
        pw_length = int(arg)
    if opt == '-d':
        debug += 1

dictionary1 = open("/usr/share/dict/words","r")
words = dictionary1.readlines()
dictionary1.close()

dictionary2 = open("/usr/share/dict/web2a","r")
phrases = dictionary2.readlines()
dictionary2.close()

word_len = len(words)
phrase_len = len(phrases)
total_len = word_len + phrase_len
word_cnt = 0

while word_cnt < num_words or len(password) < pw_length:
    idx = random.randrange(total_len)
    use_words = 0
    if idx > phrase_len:
        idx -= phrase_len
        use_words = 1
    if len(password) == 0:
        if use_words == 1:
            password = words[idx].rstrip('\n')
        else:
            password = phrases[idx].rstrip('\n')
    else:
        if use_words == 1:
            password = password + " " + words[idx].rstrip('\n')
        else:
            password = password + " " + phrases[idx].rstrip('\n')
    word_cnt = len(password.split())


print password