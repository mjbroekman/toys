#!/usr/bin/perl -w

use strict;
use warnings;

# Set to the directory you want to have searched for photos
my $searchPath = '~/Pictures/';
# Edit to the number of seconds between photo switches
my $switchTime = 600;
my $debug = 1;

# bgotd-- background of the day  
# Written by Michael Moore, Nov. 2007, placed in the public domain 

### If the search path doesn't exist, sleep a while to see if it shows up.
sleep $switchTime while ( ! -d $searchPath );

my @photos = `find $searchPath -type f | grep [jJ][pP][eE]*[gG]`;              
chomp(@photos);
my $photo = undef;
my $cur_photo;

while(1)
{
    $cur_photo = `gconftool-2 --get /desktop/gnome/background/picture_filename`;
    chomp $cur_photo;
    print "\$cur_photo = $cur_photo\n" if ( $debug );
    while ( ( ! defined($photo) ) || ( $cur_photo eq $photo ) ) {
        $photo = $photos[rand($#photos)];
    }
    print "\$photo = $photo\n" if ( $debug );
    chomp $photo;
    my $fname = $photo;
    $fname =~ s|.+/||;
    my $orient = `jpegexiforient -n $photo`;
    print "\$orient = $orient\n" if ( $debug );
    $orient = 1 if ( ! defined($orient) || $orient eq "" );

    if ( $orient == 1 ) {
        # don't do anything.  oriented properly
    } elsif ( $orient == 2 ) {
        # oriented backwards, flip horizontal
        `jpegtran -flip horizontal -copy all -outfile /tmp/$fname $photo`;
        `jpegexiforient -1 /tmp/$fname`;
        `mv /tmp/$fname $photo`;
    } elsif ( $orient == 3 ) {
        # upside down and backwards, rotate 180
        `jpegtran -rotate 180 -copy all -outfile /tmp/$fname $photo`;
        `jpegexiforient -1 /tmp/$fname`;
        `mv /tmp/$fname $photo`;
    } elsif ( $orient == 4 ) {
        # upside down, flip vertical
        `jpegtran -flip vertical -copy all -outfile /tmp/$fname $photo`;
        `jpegexiforient -1 /tmp/$fname`;
        `mv /tmp/$fname $photo`;
    } elsif ( $orient == 5 ) {
        # backwards and rotated 90 clockwise
        `jpegtran -rotate 90 -copy all -outfile /tmp/$fname $photo`;
        `jpegtran -flip horizontal -copy all -outfile /tmp/${fname}.2 /tmp/$fname`;
        `jpegexiforient -1 /tmp/${fname}.2`;
        `mv /tmp/${fname}.2 $photo`;
        unlink("/tmp/$fname");
    } elsif ( $orient == 6 ) {
        # fallen over backwards
        `jpegtran -rotate 90 -copy all -outfile /tmp/$fname $photo`;
        `jpegexiforient -1 /tmp/$fname`;
        `mv /tmp/$fname $photo`;
    } elsif ( $orient == 7 ) {
        `jpegtran -flip horizontal -copy all -outfile /tmp/$fname $photo`;
        `jpegtran -rotate 90 -copy all -outfile /tmp/${fname}.2 /tmp/$fname`;
        `jpegexiforient -1 /tmp/${fname}.2`;
        `mv /tmp/${fname}.2 $photo`;
        unlink("/tmp/$fname");
    } elsif ( $orient == 8 ) {
        # fallen over forward
        `jpegtran -rotate 270 -copy all -outfile /tmp/$fname $photo`;
        `jpegexiforient -1 /tmp/$fname`;
        `mv /tmp/$fname $photo`;
    }
    `gconftool-2 --type string --set /desktop/gnome/background/picture_filename "$photo" --set /desktop/gnome/background/picture_options scaled`;
    sleep($switchTime);
}
