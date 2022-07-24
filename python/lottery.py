"""Lottery.py

This is a silly little lottery number generator for various lottery games

"""
import sys
import argparse
import random

# powerball is 5 numbers 1 - 69 and 1 number 1 - 26
powerball = (range(1,70), range(1,27))
# megamillions is 5 numbers 1 - 70 and 1 number 1 - 25
megamil = (range(1,71), range(1,26))
# lucky for life is 5 numbers 1 - 48 and 1 number 1 - 18
luckylife = (range(1,49), range(1,19))

parser = argparse.ArgumentParser(description="Generate numbers for a lottery game")
parser.add_argument(
    "--powerball",
    action="store",
    help="Generate Powerball numbers",
    default=0,
    type=int
)
parser.add_argument(
    "--megamil",
    "--megamillions",
    action="store",
    help="Generate MegaMillions numbers",
    default=0,
    type=int
)
parser.add_argument(
    "--luckylife",
    "--lucky",
    action="store",
    help="Generate LuckyForLife numbers",
    default=0,
    type=int
)
args = parser.parse_args(sys.argv[1:])

try:
    while args.powerball > 0:
        random.seed()
        numbers = random.sample(powerball[0],5)
        megaball = random.choice(powerball[1])
        print("Powerball Numbers: ", sorted(numbers), " Megaball: ", megaball)
        args.powerball = args.powerball - 1
    while args.megamil > 0:
        random.seed()
        numbers = random.sample(megamil[0],5)
        megaball = random.choice(megamil[1])
        print("MegaMillions Numbers: ", sorted(numbers), " Megaball: ", megaball)
        args.megamil = args.megamil - 1
    while args.luckylife > 0:
        random.seed()
        numbers = random.sample(luckylife[0],5)
        megaball = random.choice(luckylife[1])
        print("Lucky For Life Numbers: ", sorted(numbers), " Lucky Ball: ", megaball)
        args.luckylife = args.luckylife - 1
except:
    print("Encountered an exception... were you trying to be tricky?")
    
