#!/usr/bin/env python
"""
Perform and illustrate bitwise math
"""

import sys
import argparse
import time


def usage():
    """
    Usage/syntax
    """
    print("$ bitwise.py [-h] [-d|-v] [-o operator] -1 first_arg -2 second_arg")


def main(argv):
    """
    Argument parsing
    """

    parser = argparse.ArgumentParser(description="Perform bitwise operations on arguments")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument("--debug", "-d", action="count", default=0)
    parser.add_argument(
        "--op",
        "-o",
        action="store",
        choices=["and", "or", "xor", "not", "lshift", "left", "rshift", "right"],
        required=True,
        help="Specify the bitwise operator that you want to display the output for",
    )
    parser.add_argument(
        "--arg1",
        "-1",
        action="store",
        required=True,
        help="First (or only) argument to operate on",
    )
    parser.add_argument(
        "--arg2",
        "-2",
        action="store",
        help="Second argument to operation for and, or, and xor",
    )
    args = parser.parse_args(argv)
    if args.op in ["and", "xor", "or"] and args.arg2 is None:
        print("Missing second argument for '" + args.op + "' operation.")
        parser.parse_args(["-h"])

    if args.op == "and":
        perform_and(args.arg1, args.arg2)
    if args.op == "or":
        perform_or(args.arg1, args.arg2)
    if args.op == "xor":
        perform_xor(args.arg1, args.arg2)
    if args.op == "not":
        perform_not(args.arg1)
    if args.op in ["lshift", "left"]:
        perform_left(args.arg1)
    if args.op in ["rshift", "right"]:
        perform_right(args.arg1)


def perform_and(arg1, arg2):
    """
    Perform and illustrate the 'and' operation
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
        time.sleep(1)
    print("\n")

    final = frombits(result)
    print("Result is:")
    print("'" + final + "'", " = ", getbits(final))


def perform_or(arg1, arg2):
    """
    Perform and illustrate the 'or' operation
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
        time.sleep(1)
    print("\n")

    final = frombits(result)
    print("Result is:")
    print("'" + final + "'", " = ", getbits(final))


def perform_xor(arg1, arg2):
    """
    Perform and illustrate the 'xor' operation
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
        time.sleep(1)
    print("\n")

    final = frombits(result)
    print("Result is:")
    print("'" + final + "'", " = ", getbits(final))


def perform_not(arg1):
    """
    Perform and illustrate the 'not' operation
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
        time.sleep(1)
    print("\n")

    final = frombits(result)
    print("Result is:")
    print("'" + final + "'", " = ", getbits(final))


def perform_left(arg1):
    """
    Perform and illustrate the 'left shift' operation
    """
    first = getbits(arg1)
    print(first)


def perform_right(arg1):
    """
    Perform and illustrate the 'right shift' operation
    """
    first = getbits(arg1)
    print(first)


def getbits(arg):
    """
    Get the bitstring of the given text string
    """
    result = []
    for c in arg:
        bits = bin(ord(c))[2:]
        bits = "00000000"[len(bits) :] + bits
        result.extend([int(b) for b in bits])
    return result


def frombits(bits):
    """
    Convert list of bits to text
    """
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b * 8 : (b + 1) * 8]
        chars.append(chr(int("".join([str(bit) for bit in byte]), 2)))
    return "".join(chars)


if __name__ == "__main__":
    main(sys.argv[1:])
