#!/usr/bin/perl

use strict;
use Spreadsheet::ParseExcel;
use Spreadsheet::ParseExcel::Workbook;
use Spreadsheet::ParseExcel::Worksheet;
use Spreadsheet::WriteExcel;
use Data::Dumper;
use Getopt::Long;

sub sort_net {
    my @a_net = split /\./, $a;
    my @b_net = split /\./, $b;

    $a_net[1] <=> $b_net[1] ||
	$a_net[2] <=> $b_net[2] ||
	$a_net[3] <=> $b_net[3]
}

sub usage {
    print "Available Options:\n";
    print "\t--help   : This output\n";
    print "\t--file   : Specify the Excel spreadsheet to parse\n";
    print "\t--format : Specify the format to dump data in\n";
    print "\n";
    print "Available formats:\n";
    print "\tcsv - Full dump of subnets, ip addresses, and hostnames in CSV format\n";
    print "\tdump - Full dump of Perl datastructures (uses Data::Dumper)\n";
    print "\n";
    exit;
}

my $file = "/home/mbroekman/tmp/test.xls";
my $format = "dump";
my %addrspace;
my $help;

my $result = GetOptions(
    "file=s" => \$file,
    "format=s" => \$format,
    "help" => \$help,
    );

&usage if ( $help );

my $parser = Spreadsheet::ParseExcel->new();
my $workbook = $parser->parse($file);

die $parser->error(), ".\n" if ( !defined $workbook );

for my $worksheet ( $workbook->worksheets() ) {

    my ( $row_min, $row_max ) = $worksheet->row_range();
    my ( $col_min, $col_max ) = $worksheet->col_range();

    for my $col ( $col_min .. $col_max ) {	

	my $good = 0;
	my $col2 = $col + 1;
	my $network;
	my $lasthost;

	for my $row ( $row_min .. $row_max ) {

	    my $cell = $worksheet->get_cell( $row, $col );
	    my $cell2 = $worksheet->get_cell( $row, $col2 );
	    my $ip = undef;
	    my $host = undef;
	    my $ipaddr = undef;

	    next unless $cell;
#	    next if ( $cell->value() !~ /^10\./ );
	    $network = $cell->value() if ( $cell->value() =~ /^10\./ );
	    $ip = $cell->value() if ( $cell->value() =~ /^\d+[^.]*/ );
	    $host = $cell2->value() if ( defined($cell2) && $cell2->value() =~ /[\w#]+/ );

	    $network =~ s/^\s+//;
	    $network =~ s/\s+$//;
	    $ip =~ s/^\s+//;
	    $ip =~ s/\s+$//;
	    $host =~ s/^\s+//;
	    $host =~ s/\s+$//;
	    $host = $lasthost if ( $host =~ /^\#+$/ );
	    $host =~ s/\#+/$ip/;

	    $lasthost = $host;

	    # print "$network\n$ip\n" if ( $cell->value() =~ /10\.60/ );
	    if ( $network =~ /\// && $ip eq $network ) {
		( $network, $ip ) = split /\//, $network;
		$ip = "/" . $ip;
	    }
	    # print "$network\n$ip\n" if ( $cell->value() =~ /10\.60/ );
	    
	    next if ( $network eq $ip );
	    next if ( $network =~ /^$/ || $ip =~ /^$/ );

	    $host = "" if ( ! defined($host) );

	    if ( $ip !~ /^\// ) {
		$ipaddr = "$network.$ip";
		$addrspace{$network}->{$ipaddr} = $host;
	    } else {
		$network =~ /^(\d+\.\d+)\..+/;
		$network = $1;
		
		for my $t ( 0 .. 255 ) {
		    for my $l ( 0 .. 255 ) {
			next if ( $t == 0 && $l == 0 );
			next if ( $t == 255 && $l == 255 );
			$ipaddr = "$network.$t.$l";
			$addrspace{$network}->{$ipaddr} = $host;
		    }
		}
	    }			
	}
	$col++;
    }
}

if ( $format eq "csv" ) {
    for my $s ( sort sort_net keys(%addrspace) ) {
	for my $i ( sort sort_net keys(%{$addrspace{$s}}) ) {
	    print "$s,$i," . $addrspace{$s}->{$i} . "\n";
	}
    }
}

if ( $format eq "dump" ) {
    print Dumper(%addrspace);
}

if ( $format eq "networks" ) {
    print join("\n",sort sort_net keys(%addrspace) ) , "\n";
}


