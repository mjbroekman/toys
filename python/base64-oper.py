#!/usr/bin/env python3
"""
Perform and illustrate base64 encoding / decoding
"""
from __future__ import print_function

import sys
import argparse
import time



def main(argv):
    """
    Argument parsing
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
    """
    my base64 encoding / decoding class
    """
    def __init__(self,arg):
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
        """
        Perform base64 encode
        """
        self.print_oper("encode")

        self.getbits(8)

        while len(self.bits) % 6 != 0:
            self.bits.extend([0])

        self.frombits(6)

        self.display_results()


    def perform_decode(self):
        """
        Perform base64 decode
        """
        self.print_oper("decode")

        self.getbits(6)

        self.frombits(8)

        self.display_results()


    def print_oper(self,op):
        """
        Print wrapper
        """
        print("Performing", op, "operation on\n\n",self.input + ":")


    def display_results(self):
        """
        Results printer
        """
        print("\nResult is:\n",self.output)


    def getbits(self,bitlen):
        """
        Get the bitstring of the given text string
        """
        if bitlen == 8:
            for c in self.input:
                bits = bin(ord(c))[2:]
                bits = "00000000"[len(bits) :] + bits
                self.bits.extend([int(b) for b in bits])
                print(self.bits,end="\r")
                time.sleep(0.5)
        if bitlen == 6:
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


    def frombits(self,bitlen):
        """
        Convert list of bits to text
        """
        for b in range(int(len(self.bits) / bitlen)):
            byte = self.bits[b * bitlen : (b + 1) * bitlen]
            bitval = int("".join([str(bit) for bit in byte]), 2)
            if bitlen == 8:
                print("%24s => %3d => %s" % (byte, bitval, chr(bitval)))
                self.charlist.append(chr(int("".join([str(bit) for bit in byte]), 2)))
            if bitlen == 6:
                print("%18s => %3d => %s" % (byte, bitval, self.chars[bitval]))
                self.charlist.append(self.chars[int("".join([str(bit) for bit in byte]), 2)])
            time.sleep(0.2)

        while bitlen == 6 and len(self.charlist) % 4 != 0:
            self.charlist.append("=")

        self.output = "".join(self.charlist)


if __name__ == "__main__":
    main(sys.argv[1:])
