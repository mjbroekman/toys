#!/bin/bash
#
# Author: Maarten Broekman
#
# Description:
#  Code snippet to parse a quote file and display one at random
#
QUOTE_FILE=~/.quotes
if [ -r $QUOTE_FILE ]; then
    IDX=0
    declare -a QUOT_LINES
    for sub in `grep ^QUOTE $QUOTE_FILE | awk -F: '{ print $2 }'`; do
        start=`grep -n "QUOTE: $sub" $QUOTE_FILE | awk -F: '{ print $1 }'`
        nend=`grep -n "END: $sub" $QUOTE_FILE | awk -F: '{ print $1 }'`
        nlines=$(( $nend - $start ))
        QUOT_LINES[$IDX]="`head -$(( $nend - 1 )) $QUOTE_FILE | tail -$(( $nlines - 1 ))`"
        IDX=$(( $IDX + 1 ))
    done
    QUOT_IDX=$(( $RANDOM % $IDX ))
    if [ $QUOT_IDX -eq $IDX ]; then
        echo "Your lucky number is $QUOT_IDX"
    else
        echo "${QUOT_LINES[$QUOT_IDX]}"
    fi
else
    echo "No notable quotes today. Have a great day."
fi
