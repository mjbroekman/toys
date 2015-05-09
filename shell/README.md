# Shell toys
## Description
These are code snippets from my .bashrc that I use to make my shell more useful or entertaining

## Files
* fortune.sh - Pick a random saying from your .fortune file and display it on shell startup
* sample.fortune - Example file
* update_brew.sh - Check for, and upgrade, brew-managed installs once per day

## Fortune Installation
1. Copy sample.fortune to ~/.fortune
2. Copy fortune.sh to ~/.fortune.sh
3. Edit ~/.bashrc to include: `~/.fortune.sh`
4. Add your own fortunes to ~/.fortune

## Homebrew Updater Installation
1. Copy update_brew.sh to ~/.update_brew.sh
2. Edit ~/.bashrc to include: `~/.update_brew.sh`
