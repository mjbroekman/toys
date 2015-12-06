#!/usr/bin/env perl

my $file = $ARGV[0];
open(FILE,"$file");
my $res = "";
my $req = "";
while ( $mount = <FILE>) {
  if ( $mount =~ /^file { \'([^\']+)\':/ ) {
    $res = "file";
    $req = $1;
  } elsif ( $mount =~ /^mount { \'([^\']+)\':/ ) {
    $res = "mount";
    $req = $1;
  }

  chomp $mount;
  if ( $line =~ /^file/ ) {
      print $mount;
      print "  path => '$req',";
  } elsif ( $mount =~ /^mount/ ) {
      print $mount;
      print "  name => '$req',";
  } elsif ( $mount !~ /}$/ ) {
    print $mount;
  } elsif ( $res =~ "file" ) {
    print $mount . "\n";
  } else {
    print "  require => File['" . $req . "'], }\n";
  }
}
