# Shell toys
## Description
These are code snippets from my .bashrc that I use to make my shell more useful or entertaining

## Files
* fortune.sh - Pick a random saying from your .fortune file and display it on shell startup
* sample.fortune - Example file
* update_brew.sh - Check for, and upgrade, brew-managed installs once per day

## Fortune Installation
* Copy sample.fortune to ~/.fortune
* Copy fortune.sh to ~/.fortune.sh
* Edit ~/.bashrc to include
'~/.fortune.sh'
* Add your own fortunes to ~/.fortune

## Homebrew Updater Installation
* Copy update_brew.sh to ~/.update_brew.sh
* Edit ~/.bashrc to include
'~/.update_brew.sh'
