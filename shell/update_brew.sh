#!/bin/bash
#
# Author: Maarten Broekman
#
# Description:
#   Code snippet to keep brew installs updated on MacOS X
#
BREW=`which brew`
if [ -z "$BREW" -o ! -x $BREW ]; then
    exit 0
fi
# if [ ! -z "$ITERM_PROFILE" ]; then
#     exit 0
# fi
while [ `ps -aef | grep -v grep | grep -c xcode-select` -gt 0 ]; do
  echo "Sleeping while xcode command-line tools are installed"
  sleep 1
done
if [ ! -f ~/.homebrew_updated ]; then
  echo "Checking for homebrew updates"
  brew update >~/.homebrew_update_log 2>&1
  date +%Y%m%d >~/.homebrew_updated
  if [ `date +%w` -eq 1 ]; then
    BLIST=`brew list --formula | grep -v openjdk`
    BCNT=`echo $BLIST | awk '{ print NF }'`
    echo "Upgrading $BCNT via uninstall / reinstall..."
    brew uninstall --force $BLIST >>~/.homebrew_upgrade_log 2>&1
    echo "Uninstall complete..."
    for b in $BLIST; do
      echo -n "."
      brew install $b >>~/.homebrew_upgrade_log 2>&1
    done
    echo
    echo "Reinstall complete..."
  fi
elif [ `date +%Y%m%d` -gt `cat ~/.homebrew_updated` ]; then
  if [ -d ~/Dropbox ]; then
    brew list --formula >~/Dropbox/brew_list.log
  else
    brew list --formula >~/.brew_list.log
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
  if [ `date +%w` -eq 1 ]; then
    BLIST=`brew list --formula | grep -v openjdk`
    BCNT=`echo $BLIST | awk '{ print NF }'`
    echo "Upgrading $BCNT via uninstall / reinstall..."
    brew uninstall --force $BLIST >>~/.homebrew_upgrade_log 2>&1
    echo "Uninstall complete..."
    for b in $BLIST; do
      echo -n "."
      brew install $b >>~/.homebrew_upgrade_log 2>&1
    done
    echo
    echo "Reinstall complete..."
  fi
fi
