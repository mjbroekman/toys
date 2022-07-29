#!/usr/bin/perl

use strict;
use warnings;

use Time::Piece;
use Time::Seconds qw/ ONE_DAY /;


print_print_name();

sub print_print_name {
    print_name();
}

sub print_name {
    my $name = (caller(1))[3];
    print $name . "\n";
}
