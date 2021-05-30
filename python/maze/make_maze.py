#!/usr/bin/env python3
"""
Print out a maze
"""
import getopt
import sys
import secrets

from maze import Maze


def usage():
    """
    Usage statement
    """
    print("maze_gen.py [-r rows] [-c cols] [-h]")
    sys.exit()


def main(args):
    """
    Main processing of arguments
    """
    opts = []
    ny = 0
    nx = 0

    try:
        opts, args = getopt.getopt(args, "c:r:dh")
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt == "-h":
            usage()
        if opt == "-r":
            ny = int(arg)
        if opt == "-c":
            nx = int(arg)

    while int(ny) not in range(10, 50):
        print("Enter the height (10 - 50) ", end="")
        ny = input()
        ny = int(ny)

    if (ny % 2) == 0:
        ny += 1

    while int(nx) not in range(10, 50):
        print("Enter the width (10 - 50): ", end="")
        nx = input()
        nx = int(nx)

    maze = Maze(nx, ny, secrets.randbelow(nx), secrets.randbelow(ny))
    maze.make_maze()

    print(maze)
    # maze.write_svg('maze.svg')


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("Aborting...")
