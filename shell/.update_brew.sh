#!/bin/bash
#
# Author: Maarten Broekman
#
# Description:
#   Code snippet to keep brew installs updated on MacOS X
#
if [ ! -f ~/.homebrew_updated ]; then
    date +%Y%m%d >~/.homebrew_updated
    echo "Checking for homebrew updates"
    brew update >~/.homebrew_update_log 2>&1
    echo "Performing homebrew upgrades"
    brew upgrade >~/.homebrew_upgrade_log 2>&1
elif [ `date +%Y%m%d` -gt `cat ~/.homebrew_updated` ]; then
    date +%Y%m%d >~/.homebrew_updated
    cp ~/.homebrew_update_log ~/.homebrew_update_log.1
    cp ~/.homebrew_upgrade_log ~/.homebrew_upgrade_log.1
    echo "Checking for homebrew updates"
    brew update >~/.homebrew_update_log 2>&1
    echo "Performing homebrew upgrades"
    brew upgrade >~/.homebrew_upgrade_log 2>&1
fi
