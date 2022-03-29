#!/usr/bin/env python3
"""Retrieve and print words from a UTF-8 document

Usage:
    python3 story.py <URL>
"""
import sys
from urllib.request import urlopen


def fetch_words(url):
    """Fetch a list of words from a URL

    Args:
        url: The URL to retrieve UTF-8 data from
    
    Returns:
        A list of strings that compose the URL data
    """
    story = urlopen(url)
    story_words = []

    for line in story:
        line_words = line.decode('UTF-8').split()
        for word in line_words:
            story_words.append(word)

    story.close()
    return story_words


def print_items(items):
    """Print a series of objects from an iterable
    
    Args:
        items: Iterable containing objects to print
    
    Returns:
        None
    """
    for item in items:
        print(item)


def main(url):
    """Main function print URL items from the command-line
    
    Args:
        url: The URL to pass to fetch_words()
    
    Returns:
        None
    """
    words = fetch_words(url)
    print_items(words)


if __name__ == '__main__':
    main(sys.argv[1]) # The 0th arg is the module filename
