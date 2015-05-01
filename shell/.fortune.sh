#!/bin/bash
#
# Author: Maarten Broekman
#
# Description:
#   Code snippet to parse a file of random sayings and display one each time
#    a terminal window is opened.
#

FORTUNE_FILE=~/.fortune
FORT_LINES=`cat $FORTUNE_FILE | wc -l`
FORT_IDX=0
while [ $FORT_IDX -lt 1 ]; do
  FORT_IDX=$(( `head /dev/random | strings | sed -e 's/[^0-9]//g' 2>/dev/null | grep -v ^$ | head -1` + 1 ))
  FORT_IDX=$(( $FORT_IDX % $FORT_LINES ))
done
cat $FORTUNE_FILE | head -$FORT_IDX | tail -1
