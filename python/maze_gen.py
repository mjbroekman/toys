#!/usr/bin/env python3
"""
Python implementation of the 'Amazing' program found in
David Ahl's "Basic Computer Games" book published by
Workman Publishing, Copyright 1978 Creative Computing.
"""
from __future__ import print_function

import getopt
import sys
import random


def banner():
    """
    Print out the banner
    """
    print("\t\tAMAZING PROGRAM")
    print("\tCreative Computing - Morristown, New Jersey")
    print("\n\n")


def usage():
    """
    Simple usage statement
    """
    print("maze_gen.py [-r rows] [-c cols] [-h] [-d]")
    print("")
    print("  -h      => this help")
    print("  -d      => debug mode")
    print("")
    print("  -c cols => the number of columns in the maze")
    print("  -r rows => the number of rows in the maze")
    print("")
    print("Example:")
    print(" $ maze_gen.py -r 30 -c 30")
    print("This will create a maze that is 30 columns by 30 rows")
    print("")
    sys.exit(0)


# global variables for now since we were dealing with an AppleBASIC program to start with
w = []
v = []
maze = []
q = 0
z = 0
c = 1
r = 0
s = 1
height = 0
width = 0
debug = 0


def main(args):
    """
    Main processing of arguments
    """
    global height
    global width
    global debug

    try:
        opts, args = getopt.getopt(args, "c:r:dh")
    except getopt.GetoptError:
        print("maze_gen.py [-r rows] [-c cols] [-h] [-d]")
        sys.exit()

    for opt, arg in opts:
        if opt == "-d":
            debug = 1
        if opt == "-h":
            usage()
        if opt == "-r":
            height = int(arg)
        if opt == "-c":
            width = int(arg)

    try:
        while int(height) not in range(10, 100):
            print("Enter the height (10 - 100) ", end="")
            height = input()
            height = int(height)
    except ValueError:
        print("Really? Trying using an integer.")
        sys.exit()

    if (height % 2) == 0:
        if debug > 0:
            print("adding row to the end")
        height += 1

    try:
        while int(width) not in range(10, 75):
            print("Enter the width (10 - 75): ", end="")
            width = input()
            width = int(width)
    except ValueError:
        print("Really? Try using an integer.")
        sys.exit()

    gen_maze()


def gen_maze():
    """
    Create the maze
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z
    global height
    global width
    global debug
    global maze

    w = [["X" for x in range(width)] for y in range(height)]
    v = [["X" for x in range(width)] for y in range(height)]
    maze = [["X" for x in range(width)] for y in range(height)]
    row = 0
    x = int(random.random() * width)
    for i in range(width - 2):
        if i == x:
            maze[row][i] = ". "
        else:
            maze[row][i] = ".-"
    maze[row][width - 1] = ".\n"

    w[x][1] = c
    c += 1
    r = x
    twosixty()


def twosixty():
    """
    control loop?
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z

    if r - 1 == 0:  # 260
        fivethirty()
    if w[r - 1][s] != 0:  # 265
        fivethirty()
    if s - 1 == 0:  # 270
        threeninety()
    if w[r][s - 1] != 0:  # 280
        threeninety()
    if r == height:  # 290
        threethirty()
    if w[r + 1][s] != 0:
        threethirty()
    x = int(random.random() * width)
    if x == 0:
        seveninety()
    elif x == 1:
        eighttwenty()
    else:
        eightsixty()


def threethirty():
    """
    more control
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z

    print("330")


def fivethirty():
    """
    more controls
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z

    print("530")


def threeninety():
    """
    even more controls
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z

    print("390")


def seveninety():
    """
    control stuff
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z

    print("790")


def eighttwenty():
    """
    things
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z

    print("820")


def eightsixty():
    """
    stuff
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z

    print("860")
    # while row < height:
    #     if row in (0, height - 1):
    #         if debug > 0:
    #             print("generating border row " + str(row))
    #         col = 0
    #         while col < (width - 1):
    #             if col == ran:
    #                 maze[row][col] = ". "
    #             else:
    #                 maze[row][col] = ".-"
    #             col += 1
    #         maze[row][col] = ".\n"
    #     elif (row % 2) == 0:
    #         if debug > 0:
    #             print("generating wall row " + str(row))
    #         maze[row][0] = ":-"
    #         col = 1
    #         while col < (width - 1):
    #             maze[row][col] = ":-"
    #             col += 1
    #         maze[row][col] = ":\n"
    #     elif (row % 2) == 1:
    #         if debug > 0:
    #             print("generating corridor row " + str(row))
    #         maze[row][0] = "| "
    #         col = 1
    #         while col < (width - 1):
    #             maze[row][col] = "  "
    #             col += 1
    #         maze[row][col] = "|\n"
    #     row += 1
    #
    # print_maze(maze)


def print_maze():
    """
    Print out the maze
    """
    global maze
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
        print("Aborting...")
