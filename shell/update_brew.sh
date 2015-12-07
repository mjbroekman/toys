#!/bin/bash
#
# Author: Maarten Broekman
#
# Description:
#   Code snippet to keep brew installs updated on MacOS X
#
if [ ! -x /usr/local/bin/brew ]; then
    exit 0
fi
if [ ! -f ~/.homebrew_updated ]; then
  echo "Checking for homebrew updates"
  brew update >~/.homebrew_update_log 2>&1
#    BREW_CNT=`brew list | wc -l | awk '{ print $1 }'`
#    IDX=0
#    for f in `brew list`; do
#	IDX=$(( $IDX + 1 ))
#	printf "%s\r" "Performing homebrew update $IDX of $BREW_CNT"
#	brew upgrade $f >~/.homebrew_upgrade_log 2>&1
#    done
#    echo
elif [ `date +%Y%m%d` -gt `cat ~/.homebrew_updated` ]; then
  if [ -d ~/Dropbox ]; then
    brew list >~/Dropbox/brew_list.log
  fi
  date +%Y%m%d >~/.homebrew_updated
  if [ -f ~/.homebrew_update_log ]; then
    mv ~/.homebrew_update_log ~/.homebrew_update_log.1
  fi
  if [ -f ~/.homebrew_upgrade_log ]; then
    mv ~/.homebrew_upgrade_log ~/.homebrew_upgrade_log.1
  fi
  echo "Checking for homebrew updates"
  brew update >~/.homebrew_update_log 2>&1

  if [ `date +%w` -eq 0 ]; then
    BLIST=`brew list`
    brew uninstall --force $BLIST >~/.homebrew_upgrade_log 2>&1
    brew install $BLIST >~/.homebrew_upgrade_log 2>&1
  fi
#    BREW_CNT=`brew list | wc -l | awk '{ print $1 }'`
#    IDX=0
#    for f in `brew list`; do
#	IDX=$(( $IDX + 1 ))
#	printf "%s\r" "Performing homebrew update $IDX of $BREW_CNT"
#	brew upgrade $f >~/.homebrew_upgrade_log 2>&1
#    done
#    echo
fi
