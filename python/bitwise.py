#!/usr/bin/env python3
"""
Perform and illustrate bitwise math

Usage:
    bitwise.py [-o operation] [-s shift_count] [-1 first_arg] [-2 second_arg]

Supported Operations:
    - and    : combines two arguments using the 'and' bitwise operation
    - or     : combines two arguments using the 'or' bitwise operation
    - xor    : combined two arguments using the 'xor' bitwise operation
    - not    : uses the 'not' operation on one argument
    - lshift : shifts one argument to the left by shift_count bits
    - rshift : shifts one argument to the right by shift_count bits
"""

import sys
import argparse
import time


def main(argv):
    """Parse command-line arguments

    Args:
        argv: sys.argv
    """

    parser = argparse.ArgumentParser(description="Perform bitwise operations on arguments")
    parser.add_argument(
        "--op",
        "-o",
        action="store",
        choices=["and", "or", "xor", "not", "lshift", "left", "rshift", "right"],
        required=True,
        help="Specify the bitwise operator that you want to display the output for",
    )
    parser.add_argument(
        "--shift",
        "-s",
        type=int,
        action="store",
        required=any(x in ["lshift", "rshift", "left", "right"] for x in sys.argv),
        help="the number of bits to shift left or right",
    )
    parser.add_argument(
        "--arg1",
        "-1",
        action="store",
        help="First (or only) argument to operate on",
    )
    parser.add_argument(
        "--arg2",
        "-2",
        action="store",
        required=any(x in ["and", "or", "xor"] for x in sys.argv),
        help="Second argument to operation for and, or, and xor",
    )
    args = parser.parse_args(argv)

    if args.op == "and":
        perform_and(args.arg1, args.arg2)
    if args.op == "or":
        perform_or(args.arg1, args.arg2)
    if args.op == "xor":
        perform_xor(args.arg1, args.arg2)
    if args.op == "not":
        perform_not(args.arg1)
    if args.op in ["lshift", "left"]:
        perform_left(args.arg1, args.shift)
    if args.op in ["rshift", "right"]:
        perform_right(args.arg1, args.shift)


def perform_and(arg1, arg2):
    """Perform and illustrate the 'and' operation

    Args:
        arg1: first argument of the operation
        arg2: second argument of the operation
    """
    first = getbits(arg1)
    second = getbits(arg2)
    result = []

    while len(second) < len(first):
        second.extend([0])

    while len(first) < len(second):
        first.extend([0])

    length = len(first)

    print("Performing 'and' (&) operation on:\n")
    print(arg1 + ":\n", first)
    print(arg2 + ":\n", second)
    print("-" * 3 * (length + 1))

    for idx in range(0, length):
        if first[idx] == second[idx] and first[idx] == 1:
            result.extend([1])
        else:
            result.extend([0])
        print("", result, end="\r")
        time.sleep(0.1)
    print("\n")

    final = frombits(result)
    print("Result is:")
    print("'" + final + "'", " = ", getbits(final))


def perform_or(arg1, arg2):
    """Perform and illustrate the 'or' operation
 
    Args:
        arg1: first argument of the operation
        arg2: second argument of the operation
   """
    first = getbits(arg1)
    second = getbits(arg2)
    result = []

    while len(second) < len(first):
        second.extend([0])

    while len(first) < len(second):
        first.extend([0])

    length = len(first)

    print("Performing 'or' (|) operation on:\n")
    print(arg1 + ":\n", first)
    print(arg2 + ":\n", second)
    print("-" * 3 * (length + 1))

    for idx in range(0, length):
        if first[idx] == 1 or second[idx] == 1:
            result.extend([1])
        else:
            result.extend([0])
        print("", result, end="\r")
        time.sleep(0.1)
    print("\n")

    final = frombits(result)
    print("Result is:")
    print("'" + final + "'", " = ", getbits(final))


def perform_xor(arg1, arg2):
    """Perform and illustrate the 'xor' operation

    Args:
        arg1: first argument of the operation
        arg2: second argument of the operation
    """
    first = getbits(arg1)
    second = getbits(arg2)
    result = []

    while len(second) < len(first):
        second.extend([0])

    while len(first) < len(second):
        first.extend([0])

    length = len(first)

    print("Performing 'xor' (^) operation on:\n")
    print(arg1 + ":\n", first)
    print(arg2 + ":\n", second)
    print("-" * 3 * (length + 1))

    for idx in range(0, length):
        if first[idx] != second[idx]:
            result.extend([1])
        else:
            result.extend([0])
        print("", result, end="\r")
        time.sleep(0.1)
    print("\n")

    final = frombits(result)
    print("Result is:")
    print("'" + final + "'", " = ", getbits(final))


def perform_not(arg1):
    """Perform and illustrate the 'not' operation
    
    Args:
        arg1: first argument of the operation
    """
    first = getbits(arg1)
    result = []
    length = len(first)
    print("Performing 'not' (~) operation on:\n")
    print(arg1 + ":\n", first)
    print("-" * 3 * (length + 1))

    for idx in range(0, length):
        if first[idx] == 0:
            result.extend([1])
        else:
            result.extend([0])
        print("", result, end="\r")
        time.sleep(0.1)
    print("\n")

    final = frombits(result)
    print("Result is:")
    print("'" + final + "'", " = ", getbits(final))


def perform_left(arg1, shift):
    """Perform and illustrate the 'left shift' operation
    
    Args:
        arg1: first argument of the operation
        shift: number of bits that arg1 will be shifted left
    """
    first = getbits(arg1)
    print("Performing bitwise (logical) left shift on:\n")
    print(arg1 + ":\n", first)
    for c in arg1:
        print("'" + c + "' = ascii", ord(c), end="\t")
    print("")
    result = []
    for b in range(int(len(first) / 8)):
        shifted = first[b * 8 : (b + 1) * 8]
        print(frombits(shifted), ":")
        s = shift
        while s > 0:
            shifted = shifted[1:8]
            shifted.extend([0])
            print("", shifted, end="\r")
            time.sleep(0.1)
            s -= 1
        print("")
        result.extend(shifted)

    final = frombits(result)
    print("Result is:")
    print("'" + final + "'", " = ", getbits(final))
    for c in final:
        print("'" + c + "' = ascii", ord(c), end="\t")
    print("")


def perform_right(arg1, shift):
    """Perform and illustrate the 'right shift' operation
    
    Args:
        arg1: first argument of the operation
        shift: number of bits that arg1 will be shifted right
    """
    first = getbits(arg1)
    print("Performing bitwise (logical) right shift on:\n")
    print(arg1 + ":\n", first)
    for c in arg1:
        print("'" + c + "' = ascii", ord(c), end="\t")
    print("")
    result = []
    for b in range(int(len(first) / 8)):
        shifted = first[b * 8 : (b + 1) * 8]
        print(frombits(shifted), ":")
        s = shift
        while s > 0:
            shifted = shifted[0:7]
            shifted.insert(0, 0)
            print("", shifted)
            time.sleep(0.1)
            s -= 1
        print("")
        result.extend(shifted)

    final = frombits(result)
    print("Result is:")
    print("'" + final + "'", " = ", getbits(final))
    for c in final:
        print("'" + c + "' = ascii", ord(c), end="\t")
    print("")


def getbits(arg):
    """Get the bitstring of the given text string
    
    Args:
        arg: argument to convert to a bitstring
    """
    result = []
    for c in arg:
        bits = bin(ord(c))[2:]
        bits = "00000000"[len(bits) :] + bits
        result.extend([int(b) for b in bits])
    return result


def frombits(bits):
    """Convert list of bits to text

    Args:
        bits: bitstring to convert to text
    """
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b * 8 : (b + 1) * 8]
        chars.append(chr(int("".join([str(bit) for bit in byte]), 2)))
    return "".join(chars)


if __name__ == "__main__":
    main(sys.argv[1:])
