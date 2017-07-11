#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
'''
Collatz function
'''

import sys

def collatz(number, col):
    '''
    Calculate the Collatz Sequence
    '''
    col.append(number)
    if number > 1:
        if number % 2 == 0:
            collatz(int(number / 2), col)
        else:
            collatz((3 * number) + 1, col)

    return col

def main(args):
    '''
    Main processing
    '''
    colseq = []
    number = 1

    # Get the number to start the Collatz Sequence with
    # Use the first argument on the command line or prompt for a number
    if len(args) > 0:
        number = args[0]
    else:
        print("Please enter an integer: ", end='')
        number = input()

    # Try it out...wrap in try{} because we are forcing the input to an int()
    try:
        # Print out the list of numbers in the Collatz sequence
        print(collatz(int(number), colseq))
    except ValueError:
        print("Please enter a valid integer.")

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Exiting...')
