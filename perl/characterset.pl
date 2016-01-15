#!perl

use Tie::File;
my $file = $ARGV[0];

tie my @array, 'Tie::File', $file, mode => O_RDONLY, memory => 3_000_000 or die "Unable to tie file: $!\n";
my $string = join "", @array;
untie @array;

my @chars = split //, $string;
my $charset;

foreach my $char ( @chars ) {
    $charset .= $char if ( index($charset,$char) < 0 );
}

print "Original string: '''' $string ''''\n";
print "Character set: '''' $charset ''''\n";
