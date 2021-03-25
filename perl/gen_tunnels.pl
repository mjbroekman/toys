#!/usr/bin/env perl
#
# Script to generate local port forwarding for mysql to a target tunnel host
# 

use Getopt::Long;

my @hosts = ();
my $tunnel = "";
my $dst_port = 3306;

&GetOptions(
            "tunnel=s" => \$tunnel,
            "host=s@" => \@hosts,
            "endpoint=s@" => \@hosts,
            "port=i" => \$dst_port,
           );

if ( -z "$tunnel" ) {
    $tunnel = $ARGV[1];
}

foreach my $host ( @hosts ) {
    my $local_port = 0;
    foreach my $char ( split( //,$host ) ) {
       $local_port += ord($char);
    }
    if ( $local_port < 1000 ) {
        $local_port = "9$local_port";
    }
    print "ssh -L 127.0.0.1:$local_port:$host:$dst_port $tunnel\n";
}

