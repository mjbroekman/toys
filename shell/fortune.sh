#!/bin/bash
#
# Author: Maarten Broekman
#
# Description:
#   Code snippet to parse a file of random sayings and display one each time
#    a terminal window is opened.
#

FORTUNE_FILE=~/.fortune
if [ -r $FORTUNE_FILE ]; then
    IDX=1
    declare -a FORT_LINES
    IFS="
"
    for l in `cat $FORTUNE_FILE | grep -v ^$`; do
	FORT_LINES[$IDX]=$l
	IDX=$(( $IDX + 1 ))
    done
    unset IFS
    FORT_IDX=$(( $RANDOM % $IDX ))
    if [ $FORT_IDX -eq $IDX ]; then
	echo "Your lucky number is $FORT_IDX"
    else
	echo ${FORT_LINES[$FORT_IDX]}
    fi
else
    declare -a NUM
    for (( NUMMATCH=1; $NUMMATCH != 0; )); do
	NUM[0]=$(( $RANDOM % 72 ))
	NUM[1]=$(( $RANDOM % 72 ))
	NUM[2]=$(( $RANDOM % 72 ))
	NUM[3]=$(( $RANDOM % 72 ))
	NUM[4]=$(( $RANDOM % 72 ))
	NUM[5]=$(( $RANDOM % 72 ))
	NUMMATCH=0
	I=0
	while [ $I -lt 6 ]; do
	    J=0
	    while [ $J -lt 6 ]; do
		if [ $I -eq $J ]; then
		    J=$(( $J + 1 ))
		fi
		if [ $J -ge ${#NUM[@]} ]; then
		    continue
		fi
		if [ ${NUM[$I]} -eq ${NUM[$J]} ]; then
		    NUMMATCH=1
		    break 2
		fi
		J=$(( $J + 1 ))
	    done
	    I=$(( $I + 1 ))
	done
    done
    echo "Lucky numbers: ${NUM[@]}"
fi
