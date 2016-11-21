#!/usr/bin/env python3
'''
Retrieve and display wishlist items from Amazon
'''
from __future__ import print_function

import getopt
import os
import random
import string
import sys
import time
import requests
#import urllib2

from lxml import html


def parse_data(dtree):
    """
    Pull data out of the tree built from the webpage
    """

    print(dtree.xpath('//div[@title]'))

def main(args):
    """
    Main processing
    """

    try:
        opts, args = getopt.getopt(args, "hl:")
    except getopt.GetoptError:
        print('wishlist.py [-h] -l list_id')
        sys.exit(2)

    list_id = ""
    for opt, arg in opts:
        if opt == '-h':
            print('wishlist.py [-h] -l list_id')
            print('')
            print('  -h         => this help')
            print('  -l list_id => Amazon Wishlist ID')
            print('')
            print('Example:')
            print(' $ wishlist.py -l ABCDEFGHIJKLM')
            print(' To retrieve the wishlist from ', end='')
            print('https://www.amazon.com/gp/registry/wishlist/ABCDEFGHIJKLM')
            print('')
            sys.exit(0)
        if opt == '-l':
            list_id = arg

    if list_id == "":
        print('list_id is required.')
        print('wishlist.py [-h] -l list_id')
        sys.exit(1)

    parse_data(html.fromstring(requests.get('https://www.amazon.com/gp/registry/wishlist/'
                                            + list_id)))
# page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
# tree = html.fromstring(page.content)



if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Exiting...')
