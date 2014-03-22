#!/usr/bin/env python
'''
Retrieve a random book from Project Gutenberg and pull a random sentence from it.

This can have interesting results if the book isn't in English.

Author: Maarten Broekman
'''
import os, sys, getopt, random, string, urllib2, time
from bs4 import BeautifulSoup

def get_random_book():
    baseurl = "http://www.gutenberg.org/ebooks"
    response = urllib2.urlopen(baseurl + '/search/?sort_order=random')
    url = baseurl
    html = response.read()
    soup = BeautifulSoup(html)
    for link in soup.findAll('a'):
        if link.get('href').find('ebooks') > -1:
            if link.get('href').find('search') < 0:
                if len(link.get('href')) > 8:
                    book = link.get('href').split('/')[2]
                    break
    url = url + '/' + book + '.txt.utf-8'
    return url

def main():
    while 1 == 1:
        book = get_random_book()

        try:
            response = urllib2.urlopen(book)
        except urllib2.HTTPError:
            print "Unable to retrieve book from " + book
        else:
            html = response.read()
            text = string.join(html.split()," ")
            text = text.replace('"',"")

            sentences = text.split(". ")
            print "From " + book
            print sentences[random.randrange(len(sentences))]

            break

        time.sleep(5)

if __name__ == "__main__":
    main()
