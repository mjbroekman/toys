#!/bin/bash

if [ ! -d "$1" ]; then
    echo "$0 <base git directory>"
    exit
fi
cd $1
BASE_DIR=`pwd`

for d in `find $BASE_DIR -name .git -type d -exec dirname {} \;`
  do
    cd $d

    echo -n "Repository URL: "
    grep "url =" .git/config | awk '{ print $NF }'

    echo -n "    + Current branch: "
    git branch | grep \* | awk '{ print $NF }'

    cd $BASE_DIR
done