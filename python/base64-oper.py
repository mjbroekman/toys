#!/usr/bin/env python3
"""
Perform and illustrate base64 encoding / decoding

Usage:
    base64-oper.py [-e|-d] -a string_to_work_on

"""
from __future__ import print_function

import sys
import argparse
import time


def main(argv):
    """Parse command-line arguments

    Args:
        argv: sys.argv
    """

    parser = argparse.ArgumentParser(description="Perform base64 operations on arguments")
    parser.add_argument(
        "--encode",
        "-e",
        action="store_true",
        help="encode a string into base64",
    )
    parser.add_argument(
        "--decode",
        "-d",
        action="store_true",
        help="decode a string as if it was base64",
    )
    parser.add_argument(
        "--arg",
        "-a",
        action="store",
        help="argument to operate on",
    )
    args = parser.parse_args(argv)

    b64 = myBase64(args.arg)
    if args.encode:
        b64.perform_encode()
    if args.decode:
        b64.perform_decode()

class myBase64():
    """Base64 encoding / decoding class

    Usage:
        Instantiation:
            var = myBase64(arg)
        Encoding:
            var.perform_encode() 
        Decoding:
            var.perform_decode()
    """

    def __init__(self,arg):
        """Initialize the class object
        
        Args:
            self: object self-reference
            arg: command-line argument provided
        
        Returns:
            class object
        """
        self.input = arg
        self.output = ""
        self.result = []
        self.bits = []
        self.charlist = []
        self.length = 0
        self.chars = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                       'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                       'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                       'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                       '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/' ]


    def perform_encode(self):
        """Perform Base64 encoding

        Args:
            None (self-reference)
        """
        self.print_oper("encode")
        self.getbits(8)
        while len(self.bits) % 6 != 0:
            self.bits.extend([0])

        self.frombits(6)
        self.display_results()


    def perform_decode(self):
        """Perform Base64 decoding

        Args:
            None (self-reference)
        """
        self.print_oper("decode")
        self.getbits(6)
        self.frombits(8)
        self.display_results()


    def print_oper(self,operation):
        """Print operator being used

        Args:
            self: self-reference
            operation: operation to display
        """
        print("Performing", operation, "operation on\n\n",self.input + ":")


    def display_results(self):
        """Print Results of operation

        Args:
            None (self-reference)
        """
        print("\nResult is:\n",self.output)


    def getbits(self,bit_length):
        """Get the bitstring of the given text string and print out each step

        Args:
            self: self-reference
            bit_length: number of bits to retrieve
        """
        if bit_length == 8:
            for c in self.input:
                bits = bin(ord(c))[2:]
                bits = "00000000"[len(bits) :] + bits
                self.bits.extend([int(b) for b in bits])
                print(self.bits,end="\r")
                time.sleep(0.5)

        if bit_length == 6:
            for c in self.input:
                if c != "=":
                    bits = bin(self.chars.index(c))[2:]
                    while len(bits) < 6:
                        bits = "0" + bits
                    bits = "000000"[len(bits) :] + bits
                    self.bits.extend([int(b) for b in bits])
                print(self.bits,end="\r")
                time.sleep(0.5)

        print("\n")


    def frombits(self,bit_length):
        """Convert list of bits to text and print out each step

        Args:
            self: self-reference
            bit_length: length of bit chunks to process
        """
        for b in range(int(len(self.bits) / bit_length)):
            byte = self.bits[b * bit_length : (b + 1) * bit_length]
            bitval = int("".join([str(bit) for bit in byte]), 2)

            if bit_length == 8:
                print("%24s => %3d => %s" % (byte, bitval, chr(bitval)))
                self.charlist.append(chr(int("".join([str(bit) for bit in byte]), 2)))

            if bit_length == 6:
                print("%18s => %3d => %s" % (byte, bitval, self.chars[bitval]))
                self.charlist.append(self.chars[int("".join([str(bit) for bit in byte]), 2)])

            time.sleep(0.2)

        while bit_length == 6 and len(self.charlist) % 4 != 0:
            self.charlist.append("=")

        self.output = "".join(self.charlist)


if __name__ == "__main__":
    main(sys.argv[1:])
