#!/usr/bin/env python3
"""
Python implementation of the 'Amazing' program found in
David Ahl's "Basic Computer Games" book published by
Workman Publishing, Copyright 1978 Creative Computing.

Original AppleBASIC program author: Jack Hauber of Windsor, Connecticut
"""
from __future__ import print_function

import inspect
import getopt
import sys
import secrets
import numpy as np


def LINE():
    """
    Return program line number
    """
    caller = inspect.stack()[1]  # 0 represents this line; 1 represents line at caller
    frame = caller[0]
    info = inspect.getframeinfo(frame)

    return info.lineno


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
walls = []
visited = []
maze = []
q = z = 0
currow = curcol = maxrow = maxcol = maxval = 0
debug = 0
c = 1


def main(args):
    """
    Main processing of arguments
    """
    global debug
    global maxcol  # horizontal
    global curcol
    global maxrow  # vertical
    global currow
    global walls
    global visited
    global maze
    global c
    global q
    global z
    global maxval

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
            maxrow = int(arg)
        if opt == "-c":
            maxcol = int(arg)

    while int(maxrow) not in range(3, 100):
        print("Enter the height (3 - 100) ", end="")
        maxrow = input()
        maxrow = int(maxrow)

    if (maxrow % 2) == 0:
        maxrow += 1

    while int(maxcol) not in range(3, 75):
        print("Enter the width (3 - 75): ", end="")
        maxcol = input()
        maxcol = int(maxcol)

    walls = np.array([[0 for x in range(maxcol + 1)] for y in range(maxrow + 1)])
    visited = np.array([[0 for x in range(maxcol + 1)] for y in range(maxrow + 1)])
    maze = np.array([[".--" for x in range(maxcol + 1)] for y in range(maxrow + 1)])

    maxval = (maxcol * maxrow) + 1
    q = z = 0  # line 160

    x = int(secrets.randbelow(maxcol))
    for i in range(0, maxcol + 1):
        for j in range(0, maxrow + 1):
            if i == x and j == 0:
                print("Setting entrance to ", j, i, "at", LINE())
                maze[j][i] = "| |"
                walls[j][i] = c
            else:
                maze[j][i] = "X"

        maze[j][maxcol] = "X"

    c += 1
    curcol = x  # line 200
    currow = 1
    twosixty()


def twoten():
    """
    line 210
    """
    global currow
    global maxcol
    global curcol
    global maxrow

    if curcol < maxcol:
        curcol += 1
        twofifty()

    if currow < maxrow:
        curcol = 0
        currow += 1
        twofifty()

    currow = 1  # line 220
    curcol = 1
    twofifty()


def twofifty():
    """
    line 250
    """
    global walls
    global currow
    global curcol

    try:
        if walls[currow][curcol] != 0:
            twoten()
    except IndexError:
        print(LINE(), walls)
        print(LINE(), maze)
        sys.exit()

    twosixty()


def twosixty():
    """
    line 260
    """
    global currow
    global walls
    global curcol
    global maxrow

    if currow - 1 == 0:  # if we're on the second row of the maze
        fivethirty()
    if walls[currow - 1][curcol] != 0:  # 265
        fivethirty()
    if curcol - 1 == 0:  # 270
        threeninety()
    if walls[currow][curcol - 1] != 0:  # 280
        threeninety()
    if curcol == maxcol:  # 290
        threethirty()
    if walls[currow + 1][curcol] != 0:  # 300
        threethirty()

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
    global maxrow
    global currow
    global q

    if currow != maxrow and (curcol < maxcol and walls[currow][curcol + 1] != 0):
        threeseventy()
    elif currow != maxrow:
        threefifty()

    if z == 1:
        threeseventy()
    q = 1
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
    global walls
    global maxrow
    global currow
    global curcol
    global q
    global z

    if curcol == maxcol:
        if currow < maxrow:
            fivehundred()
        if z == 1:
            seveninety()
        q = 1
        fivehundred()

    if walls[currow + 1][curcol] != 0:
        if currow < maxrow and (curcol < maxcol and walls[currow][curcol + 1] != 0):
            seveninety()
        elif currow < maxrow:
            fivehundred()

        if z == 1:
            seveninety()
        q = 1
        fivehundred()

    if currow < maxrow and (curcol < maxcol and walls[currow][curcol + 1] != 0):  # 405
        fourfifty()
    elif currow < maxrow:
        fourthirty()

    if z == 1:  # 410
        fourfifty()

    q = 1  # 415
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


def fivehundred():
    """
    line 500
    """
    x = int(secrets.randbelow(2))
    if x == 0:
        seveninety()

    nineten()


def fivethirty():
    """
    line 530
    """
    global walls
    global maxrow
    global currow
    global curcol
    global q
    global z

    if curcol - 1 == 0 or walls[currow][curcol - 1] != 0:
        if curcol == maxcol or (currow < maxrow and walls[currow + 1][curcol] != 0):
            if currow < maxrow and (curcol < maxcol and walls[currow][curcol + 1] != 0):
                twoten()
            elif currow != maxrow:
                nineten()

            if z == 1:
                twoten()
            q = 1
            nineten()

        if currow < maxrow and (curcol < maxcol and walls[currow][curcol + 1] != 0):
            eightsixty()
        elif currow < maxrow:
            x = int(secrets.randbelow(2))
            if x == 0:
                eightsixty()
            nineten()
        if z == 1:
            eightsixty()
        q = 1
        eightthirty()

    if curcol == maxcol or (currow < maxrow and walls[currow + 1][curcol] != 0):
        if currow != maxrow and (curcol < maxcol and walls[currow][curcol + 1] != 0):
            eighttwenty()
        elif currow != maxrow:
            sixforty()
        if z == 1:
            eighttwenty()
        q = 1
        sixforty()

    if curcol < maxcol and walls[currow][curcol + 1] != 0:
        fiveninety()
    elif curcol < maxcol:
        fiveseventy()

    if z == 1:
        fiveninety()

    q = 1
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


def sixforty():
    """
    line 640
    """
    x = int(secrets.randbelow(2))
    if x == 0:
        eighttwenty()

    nineten()


def seveninety():
    """
    line 790
    """
    global walls
    global visited
    global currow
    global curcol
    global c
    global q
    global maxval

    walls[currow - 1][curcol] = c
    c += 1  # line 800
    visited[currow - 1][curcol] = 2
    currow -= 1

    if c == maxval:  # line 810
        print_maze()

    q = 0  # line 815
    twosixty()


def eighttwenty():
    """
    line 820
    """
    global walls
    global currow
    global c
    global curcol

    walls[currow][curcol - 1] = c
    eightthirty()


def eightthirty():
    """
    line 830
    """
    global c
    global visited
    global currow
    global curcol
    global q
    global maxval

    c += 1  # line 830
    visited[currow][curcol - 1] = 1  # line 840
    curcol -= 1
    if c == maxval:
        print_maze()

    q = 0  # line 850
    twosixty()


def eightsixty():
    """
    line 860
    """
    global walls
    global visited
    global currow
    global c
    global curcol

    if currow < maxrow:
        walls[currow + 1][curcol] = c
    c += 1
    if visited[currow][curcol] == 0:
        visited[currow][curcol] = 2
    else:
        visited[currow][curcol] = 3

    currow += 1
    if currow > maxrow:
        currow = maxrow
    if c == maxval:  # line 900
        print_maze()

    fivethirty()  # line 905


def nineten():
    """
    line 910
    """
    global walls
    global visited
    global currow
    global curcol
    global c
    global q
    global z

    if q == 1:
        z = 1
        if visited[currow][curcol] == 0:  # line 970
            visited[currow][curcol] = 1
            q = 0
            currow = 0
            curcol = 0
            twofifty()
        else:
            visited[currow][curcol] = 3  # line 975
            q = 0
            twoten()

    if curcol < maxcol:
        walls[currow][curcol + 1] = c  # line 920
    c += 1
    if visited[currow][curcol] == 0:
        visited[currow][curcol] = 1
    else:
        visited[currow][curcol] = 3  # line 930

    curcol += 1
    if curcol > maxcol:
        curcol = maxcol
    if c == maxval:
        print_maze()

    twosixty()  # line 955


def print_maze():
    """
    line 1010
    """
    global visited
    global maxrow
    global maxcol
    global maze

    print(LINE(), visited)
    for j in range(0, maxrow):
        # print("I", end="")  # line 1011
        for i in range(0, maxcol):  # line 1012
            if int(visited[j][i]) < 2:  # line 1013
                maze[j][i] = "  I"
                # print("  I", end="")  # line 1030
            if int(visited[j][i]) >= 2:
                maze[j][i] = "   "
                # print("   ", end="")  # line 1020
        # print("")  # line 1041
        for i in range(0, maxcol):  # line 1043
            if int(visited[j][i]) == 0 or int(visited[j][i]) == 2:  # lines 1045, 1050
                maze[j][i] = ":--"
                # print(":--", end="")  # line 1060
            if int(visited[j][i]) != 0 and int(visited[j][i]) != 2:  # line 1051
                maze[j][i] = ":  "
                # print(":  ", end="")
        # print(".")  # line 1071

    print(maze)
    sys.exit()


if __name__ == "__main__":
    try:
        banner()
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("Aborting...")
