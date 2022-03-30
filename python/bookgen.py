#!/usr/bin/env python
'''
Retrieve a random book from Project Gutenberg and pull a random sentence from it.

This can have interesting results if the book isn't in English.

Usage: bookgen.py

Author: Maarten Broekman
'''

from urllib.request import urlopen
from urllib.error import HTTPError
import random
import time
import re
from bs4 import BeautifulSoup

def get_random_book():
    """Retrieve something from Gutenberg eBooks

    Args:
        None

    Returns:
        Complete Gutenberg URL
    """
    baseurl = "http://www.gutenberg.org/ebooks"
    fileurl = "http://www.gutenberg.org/files"
    response = urlopen(baseurl + '/search/?sort_order=random')

    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.findAll('a'):
        m = re.search('(?<=ebooks\/)\d+', link.get('href'))
        if m is not None:
            book = m.group(0)
            break

    url = fileurl + '/' + book + '/' + book + '-0.txt'
    return url

def read_book():
    """Retrieve a book and print out a random sentence

    Args:
        None

    Returns:
        None
    """
    while 1 == 1:
        book = get_random_book()

        try:
            response = urlopen(book)
        except HTTPError:
            print("Unable to retrieve book from " + book)
        else:
            html = response.read()
            text = " ".join(html.split())
            text = text.replace('"', "")

            sentences = text.split(". ")
            print("From " + book)
            print(sentences[random.randrange(len(sentences))])

            break

        time.sleep(5)

if __name__ == "__main__":
    read_book()
