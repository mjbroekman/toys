#!/usr/bin/env perl

my $file = $ARGV[0];
open(FILE,"$file");
my $res = "";
my $req = "";
while (<FILE>) {
  if ( $_ =~ /^file { \'([^\']+)\':/ ) {
    $res = "file";
    $req = $1;
  } elsif ( $_ =~ /^mount { \'([^\']+)\':/ ) {
    $res = "mount";
    $req = $1;
  }

  chomp $_;
  if ( $_ =~ /^file/ ) {
      print $_;
      print "  path => '$req',";
  } elsif ( $_ =~ /^mount/ ) {
      print $_;
      print "  name => '$req',";
  } elsif ( $_ !~ /}$/ ) {
    print $_;
  } elsif ( $res =~ "file" ) {
    print $_ . "\n";
  } else {
    print "  require => File['" . $req . "'], }\n";
  }
}
