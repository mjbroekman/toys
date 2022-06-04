"""PySweeper Game

Author:
    Maarten Broekman - https://github.com/mjbroekman

To play:
$ python game.py --rows ?? --cols ?? --mines ??

where:
  --rows is the number of rows you want (2 to 36, depending on the height of your terminal window)
  --cols is the number of columns you want (2 to 36, depending on the width of your terminal window)
  --mines is the number of 'splody cells you want ( between 1 and (rows*cols)-1 ) (optional)
       if you don't specifiy the number of mines, the game will choose it for you....

"""

import sys
import argparse
import time

from cell import GameCell
from board import GameBoard

def main(argv):
    """Parse command-line arguments

    Args:
        argv: sys.argv
    """

    parser = argparse.ArgumentParser(description="Play MineSweeper in a Terminal window")
    parser.add_argument(
        "--rows",
        "-r",
        action="store",
        help="number of rows in the board",
        type=int
    )
    parser.add_argument(
        "--cols",
        "-c",
        action="store",
        help="number of columns in the baord",
        type=int
    )
    parser.add_argument(
        "--mines",
        "-m",
        action="store",
        help="number of mines to place",
        default=-1,
        type=int
    )
    parser.add_argument(
        "--tk",
        "--gui",
        action="store",
        help="Use a Tk GUI instead of the command-line",
        default=False,
        type=bool
    )
    args = parser.parse_args(argv)
    try:
        if args.tk:
            sys.path.insert(0,'/opt/homebrew/Cellar/python-tk@3.9/3.9.13/libexec')
            # import _tkinter, tkinter, tkinter.constants in a new GameBoard class
        else:
            board = GameBoard(args.rows,args.cols,args.mines)
            while not board.complete():
                print(board)
                print("'(o)pen r c' -> Opens the cell at row r column c")
                print("'(f)lag r c' -> Flags the cell at row r column c")
                move = input("Next move? ").split()
                if len(move) == 3 and (move[0][0] == "o" or move[0][0] == "f"):
                    if board.is_cell(move[1].upper(), move[2].upper()):
                        if move[0] == "o" or move[0] == "open":
                            if not board.open(move[1].upper(), move[2].upper()):
                                board.reveal()
                                print(board)
                                print("BOOM! You hit a mine! A condolence letter will be sent to your next of kin.")
                                print("\n\n\n")
                                exit()
                        elif move[0] == "f" or move[0] == "flag":
                            board.flag(move[1].upper(), move[2].upper())
                        else:
                            print("Invalid command '" + move + "'. Please use open (or o) and flag (or f) to play")
                    else:
                        print("Invalid coordinates: " + move[1].upper() + " " + move[2].upper())
                        time.sleep(2.0)
            
            board.reveal()
            print(board)
            print("CONGRATULATIONS! You successfully found all the mines without triggering them!")
            print("\n\n")
            exit()

    except ValueError as e:
        exit(e)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except (KeyboardInterrupt, EOFError):
        print('Exiting...')
        exit()
