#!/usr/bin/env python3
"""madlibs.py

A Python implementation of a MadLibs-style game.
"""

import sys
import argparse
import random
import os

class MadLib:

    def __init__:
        




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--blanks", action="store", type=int, help="The number of blank spaces that need to be filled in")
    args = parser.parse_args(sys.argv[1:])

    if hasattr(args, "help"):
        parser.print_help()
        sys.exit()

    madlib = MadLib(args)
