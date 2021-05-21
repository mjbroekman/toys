#!/usr/bin/env python3
"""
Python implementation of the 'Amazing' program found in
David Ahl's "Basic Computer Games" book published by
Workman Publishing, Copyright 1978 Creative Computing.

Original AppleBASIC program author: Jack Hauber of Windsor, Connecticut
"""
from __future__ import print_function

import getopt
import sys
import secrets


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
v1 = []
maze = []
q = 0
z = 0
c = 1
r = 0
s = 1
v = 0  # vertical
h = 0  # horizontal
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
    global h  # horizontal
    global v  # vertical

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
            v = int(arg)
        if opt == "-c":
            h = int(arg)

    try:
        while int(v) not in range(10, 100):
            print("Enter the height (10 - 100) ", end="")
            v = input()
            v = int(v)
    except ValueError:
        print("Really? Trying using an integer.")
        sys.exit()

    if (v % 2) == 0:
        if debug > 0:
            print("adding row to the end")
        v += 1

    try:
        while int(h) not in range(10, 75):
            print("Enter the width (10 - 75): ", end="")
            h = input()
            h = int(h)
    except ValueError:
        print("Really? Try using an integer.")
        sys.exit()

    gen_maze()


def gen_maze():
    """
    Create the maze
    """
    global w
    global v  # vertical
    global r
    global c
    global s
    global q
    global z
    global h  # horizontal
    global height
    global width
    global debug
    global maze
    global v1

    w = [["X" for x in range(h)] for y in range(v)]
    v1 = [["X" for x in range(h)] for y in range(v)]
    maze = [["X" for x in range(h)] for y in range(v)]
    q = 0  # line 160
    z = 0
    x = int(secrets.randbelow(h))
    for i in range(1, h):
        if i == x:
            print(".  ")
        print(".--")

    print(".\n")  # line 190

    w[x][1] = c
    c += 1
    r = x  # line 200
    s = 1
    twosixty()


def twoten():
    """
    line 210
    """
    global r
    global h
    global s
    global v
    if r != h:
        twoforty()
    if s != v:
        twothirty()

    twotwenty()


def twotwenty():
    """
    line 220
    """
    global r
    global s
    r = 1  # line 220
    s = 1
    twofifty()


def twothirty():
    """
    line 230
    """
    global r
    global s
    r = 1
    s += 1
    twofifty()


def twoforty():
    """
    line 240
    """
    global r
    r += 1

    twofifty()


def twofifty():
    """
    line 250
    """
    global w
    global r
    global s
    if w[r][s] != 0:
        twoten()

    twosixty()


def twosixty():
    """
    line 260
    """
    global r
    global w
    global s
    global v

    if r - 1 == 0:  # 260
        fivethirty()
    if w[r - 1][s] != 0:  # 265
        fivethirty()
    if s - 1 == 0:  # 270
        threeninety()
    if w[r][s - 1] != 0:  # 280
        threeninety()
    if r == v:  # 290
        threethirty()
    if w[r + 1][s] != 0:  # 300
        threethirty()

    threeten()


def threeten():
    """
    line 310
    """
    x = int(secrets.randbelow(3))
    if x == 0:
        seveninety()
    if x == 1:
        eighttwenty()
    eightsixty()


def threethirty():
    """
    line 330
    """
    global v
    global s
    global q

    if s != v:
        threeforty()
    if z == 1:
        threeseventy()
    q = 1
    threefifty()


def threeforty():
    """
    line 340
    """
    global w
    global r
    global s

    if w[r][s + 1] != 0:
        threeseventy()

    threefifty()


def threefifty():
    """
    line 350
    """
    x = int(secrets.randbelow(3))
    if x == 0:
        seveninety()
    if x == 1:
        eighttwenty()

    nineten()


def threeseventy():
    """
    line 370
    """
    x = int(secrets.randbelow(2))
    if x == 0:
        seveninety()

    eighttwenty()


def threeninety():
    """
    line 390
    """
    global w
    global v
    global r
    global s
    global q
    global z

    if r == v:
        fourseventy()

    if w[r + 1][s] != 0:
        fourseventy()

    if s != v:  # 405
        fourtwenty()

    if z == 1:  # 410
        fourfifty()

    q = 1  # 415
    fourthirty()


def fourtwenty():
    """
    line 420
    """
    global w
    global r
    global s

    if w[r][s + 1] != 0:
        fourfifty()

    fourthirty()


def fourthirty():
    """
    line 430
    """
    x = int(secrets.randbelow(3))
    if x == 0:
        seveninety()
    if x == 1:
        eightsixty()

    nineten()


def fourfifty():
    """
    line 450
    """
    x = int(secrets.randbelow(2))
    if x == 0:
        seveninety()

    eightsixty()


def fourseventy():
    """
    line 470
    """
    global v
    global s
    global q
    global z

    if s != v:
        fourninety()
    if z == 1:
        seveninety()
    q = 1
    fivehundred()


def fourninety():
    """
    line 490
    """
    global w
    global r
    global s

    if w[r][s + 1] != 0:
        seveninety()

    fivehundred()


def fivehundred():
    """
    line 500
    """
    x = int(secrets.randbelow(2))
    if x == 0:
        seveninety()

    nineten()


def fivetwenty():
    """
    line 520
    """
    seveninety()


def fivethirty():
    """
    line 530
    """
    global w
    global v
    global r
    global s
    global q
    global z

    if s - 1 == 0:
        sixseventy()
    if w[r][s - 1] != 0:
        sixseventy()
    if r == v:
        sixten()
    if w[r + 1][s] != 0:
        sixten()
    if s != v:
        fivesixty()
    if z == 1:
        fiveninety()
    q = 1
    fiveseventy()


def fivesixty():
    """
    line 560
    """
    global w
    global r
    global s

    if w[r][s + 1] != 0:
        fiveninety()

    fiveseventy()


def fiveseventy():
    """
    line 570
    """
    x = int(secrets.randbelow(3))
    if x == 0:
        eighttwenty()
    if x == 1:
        eightsixty()

    nineten()


def fiveninety():
    """
    line 590
    """
    x = int(secrets.randbelow(2))
    if x == 0:
        eighttwenty()

    eightsixty()


def sixten():
    """
    line 610
    """
    global v
    global s
    global q
    global z

    if s != v:
        sixthirty()
    if z == 1:
        sixsixty()
    q = 1
    sixforty()


def sixthirty():
    """
    line 630
    """
    if w[r][s + 1] != 0:
        sixsixty()

    sixforty()


def sixforty():
    """
    line 640
    """
    x = int(secrets.randbelow(2))
    if x == 0:
        eighttwenty()

    nineten()


def sixsixty():
    """
    line 660
    """
    eighttwenty()


def sixseventy():
    """
    line 670
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z

    if r == v:
        sevenforty()
    if w[r + 1][s] != 0:
        sevenforty()
    if s != v:
        sevenhundred()
    if z == 1:
        seventhirty()
    q = 1
    eightthirty()


def sevenhundred():
    """
    line 700
    """
    global w
    global r
    global s

    if w[r][s + 1] != 0:
        seventhirty()

    seventen()


def seventen():
    """
    line 710
    """
    x = int(secrets.randbelow(2))
    if x == 0:
        eightsixty()

    nineten()


def seventhirty():
    """
    line 730
    """
    eightsixty()


def sevenforty():
    """
    line 740
    """
    global v
    global s
    global q
    global z

    if s != v:
        sevensixty()
    if z == 1:
        seveneighty()
    q = 1
    sevenseventy()


def sevensixty():
    """
    line 760
    """
    global w
    global r
    global s
    if w[r][s + 1] != 0:
        seveneighty()

    sevenseventy()


def sevenseventy():
    """
    line 770
    """
    nineten()


def seveneighty():
    """
    line 780
    """
    onekay()


def seveninety():
    """
    line 790
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
    line 820
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z

    print("820")


def eightthirty():
    """
    line 830
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z

    print("830")


def eightsixty():
    """
    line 860
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z

    print("860")


def nineten():
    """
    line 910
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z

    print("910")


def onekay():
    """
    line 1000
    """
    global w
    global v
    global r
    global c
    global s
    global q
    global z
    print("1000")


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
