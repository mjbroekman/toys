#!/bin/bash
#
# Download public pastes from a user's pastebin area
#
PBIN=$1
PUSER=`echo $1 | awk -F/ '{ print $NF }' | md5`
if [ ! -d $PUSER ]; then
    mkdir $PUSER
fi
for p in `curl $PBIN | grep "Public paste" | awk -F\" '{ print $12":"$13 }' | sed -e 's/\>//g' -e 's/\<.*//g' -e 's/ /_/g'`; do
    ofile=`echo $p | awk -F: '{ print $2 }'`
    ifile=`echo $p | awk -F: '{ print $1 }'`
    curl -o $ofile http://pastebin.com/raw.php?i=${ifile//\//}
done