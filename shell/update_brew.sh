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
  date +%Y%m%d >~/.homebrew_updated
  if [ `date +%w` -eq 1 ]; then
    BLIST=`brew list`
    echo "Upgrading via uninstall / reinstall..."
    brew uninstall --force $BLIST >~/.homebrew_upgrade_log 2>&1
    echo "Uninstall complete..."
    brew install $BLIST >~/.homebrew_upgrade_log 2>&1
    echo "Reinstall complete..."
  fi
elif [ `date +%Y%m%d` -gt `cat ~/.homebrew_updated` ]; then
  if [ -d ~/Dropbox ]; then
    brew list >~/Dropbox/brew_list.log
  else
    brew list >~/.brew_list.log
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
    BLIST=`brew list`
    echo "Upgrading via uninstall / reinstall..."
    brew uninstall --force $BLIST >~/.homebrew_upgrade_log 2>&1
    echo "Uninstall complete..."
    brew install $BLIST >~/.homebrew_upgrade_log 2>&1
    echo "Reinstall complete..."
  fi
fi
