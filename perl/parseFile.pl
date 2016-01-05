#!/usr/bin/perl

use Getopt::Long;

sub parseFile {
  my $filename = shift;
  my $linecount = shift;
  my $modval = shift;

  if ( -f $filename ) {
    open(FILE,"$filename") || die "Error opening $filename\n";
    my $line = 0;
    my @lines = <FILE>;
    my $filelines = scalar( @lines );
    while ( $line < $linecount ) {
      $line++;
      my $readline = shift @lines;
      if ( $line eq 1 or $line eq $linecount or $line eq $filelines ) {
        print $readline;
      } elsif ( ( $line % $modval ) eq 0 and $readline !~ /[^a-z]skip[^a-z]/i ) {
        print $readline;
      } elsif ( ( $line % $modval ) ne 0 and $readline =~ /[^a-z]include[^a-z]/i ) {
        print $readline;
      }
    }
  }
}

GetOptions(
  "file=s" => \$file,
  "mod=i" => \$mod,
  "lines=i" => \$lines,
);

&parseFile($file,$lines,$mod);
