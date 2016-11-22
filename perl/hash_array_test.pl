#!/usr/bin/perl

use Data::Dumper;

my @no_session_uri = qw~
	/404_error.html
	/Counter.mpl
	/cgi-bin/Count.cgi
	/cgi-bin/c2countit.cgi
	/403error.html
	/404.html
~; # end list
my %no_session_uri;

@no_session_uri{ @no_session_uri } = (1) x scalar @no_session_uri;

print Dumper(@no_session_uri);

print Dumper(%no_session_uri);

