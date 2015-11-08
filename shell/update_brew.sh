#!/bin/bash
#
# Author: Maarten Broekman
#
# Description:
#   Code snippet to keep brew installs updated on MacOS X
#
if [ ! -x /usr/local/bin/brew ]; then
    exit 0
elif [ -d ~/Dropbox ]; then
    brew list >~/Dropbox/brew_list.log
fi
if [ ! -f ~/.homebrew_updated ]; then
    date +%Y%m%d >~/.homebrew_updated
    echo "Checking for homebrew updates"
    brew update >~/.homebrew_update_log 2>&1
    BREW_CNT=`brew list | wc -l | awk '{ print $1 }'`
    IDX=0
    for f in `brew list`; do
	IDX=$(( $IDX + 1 ))
	printf "%s\r" "Performing homebrew update $IDX of $BREW_CNT"
	brew upgrade $f >~/.homebrew_upgrade_log 2>&1
    done
    echo
elif [ `date +%Y%m%d` -gt `cat ~/.homebrew_updated` ]; then
    date +%Y%m%d >~/.homebrew_updated
    cp ~/.homebrew_update_log ~/.homebrew_update_log.1
    cp ~/.homebrew_upgrade_log ~/.homebrew_upgrade_log.1
    echo "Checking for homebrew updates"
    brew update >~/.homebrew_update_log 2>&1
    BREW_CNT=`brew list | wc -l | awk '{ print $1 }'`
    IDX=0
    for f in `brew list`; do
	IDX=$(( $IDX + 1 ))
	printf "%s\r" "Performing homebrew update $IDX of $BREW_CNT"
	brew upgrade $f >~/.homebrew_upgrade_log 2>&1
    done
    echo
fi
