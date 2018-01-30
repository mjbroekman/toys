#!/usr/bin/env python3
'''
Python implementation of the 'Amazing' program found in
David Ahl's "Basic Computer Games" book published by
Workman Publishing, Copyright 1978 Creative Computing.
'''
from __future__ import print_function

import getopt
import sys
import random

def banner():
    '''
    Print out the banner
    '''
    print("\t\tAMAZING PROGRAM")
    print("\tCreative Computing - Morristown, New Jersey")
    print("\n\n")

def usage():
    '''
    Simple usage statement
    '''
    print('maze_gen.py [-r rows] [-c cols] [-h] [-d]')
    print('')
    print('  -h      => this help')
    print('  -d      => debug mode')
    print('')
    print('  -c cols => the number of columns in the maze')
    print('  -r rows => the number of rows in the maze')
    print('')
    print('Example:')
    print(' $ maze_gen.py -r 30 -c 30')
    print('This will create a maze that is 30 columns by 30 rows')
    print('')
    sys.exit(0)

def main(args):
    '''
    Main processing of arguments
    '''
    try:
        opts, args = getopt.getopt(args, "c:r:dh")
    except getopt.GetoptError:
        print('maze_gen.py [-r rows] [-c cols] [-h] [-d]')
        sys.exit()

    height = 0
    width = 0
    debug = 0
    for opt, arg in opts:
        if opt == '-d':
            debug = 1
        if opt == '-h':
            usage()
        if opt == '-r':
            height = int(arg)
        if opt == '-c':
            width = int(arg)

    try:
        while int(height) < 10 or int(height) > 100:
            print("Enter the height (10 - 100): ", end="")
            height = input()
            height = int(height)
    except ValueError:
        print("Really? Trying using an integer.")
        sys.exit()

    if (height % 2) == 0:
        if debug > 0:
            print("adding corridor to the end")
        height += 1

    try:
        while int(width) < 10 or int(width) > 75:
            print("Enter the width (10 - 75): ", end="")
            width = input()
            width = int(width)
    except ValueError:
        print("Really? Try using an integer.")
        sys.exit()

    gen_maze(height, width, debug)

def gen_maze(height, width, debug):
    '''
    Create the maze
    '''
    maze = [["X" for x in range(width)] for y in range(height)]
    row = 0
    while row < height:
        ran = int(random.random() * width)
        if row == 0 or row == (height - 1):
            if debug > 0:
                print('generating border row ' + str(row))
            col = 0
            while col < (width - 1):
                if col == ran:
                    maze[row][col] = ". "
                else:
                    maze[row][col] = ".-"
                col += 1
            maze[row][col] = ".\n"
        elif (row % 2) == 0:
            if debug > 0:
                print('generating wall row ' + str(row))
            maze[row][0] = ":-"
            col = 1
            while col < (width - 1):
                maze[row][col] = ":-"
                col += 1
            maze[row][col] = ":\n"
        elif (row % 2) == 1:
            if debug > 0:
                print('generating corridor row ' + str(row))
            maze[row][0] = "| "
            col = 1
            while col < (width - 1):
                maze[row][col] = "  "
                col += 1
            maze[row][col] = "|\n"
        row += 1

    print_maze(maze)

def print_maze(maze):
    '''
    Print out the maze
    '''
    row = 0
    while row < len(maze):
        col = 0
        while col < len(maze[row]):
            print(maze[row][col], end="")
            col += 1
        row += 1

if __name__ == "__main__":
    try:
        banner()
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Aborting...')
