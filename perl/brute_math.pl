#!/usr/bin/perl

use Getopt::Long;
use Config;

exit 0;
##
## Brute force division
##  Subtract the divisor from the dividend until the dividend is less than the
##  divisor.  Then multiply the remainder by ten and repeat until the remainder
##  is zero or the desired precision is reached.
##
sub divide() {
    my($dividend,$divisor,$precision,$level) = @_;
#    print "Dividing $dividend by $divisor to $precision decimal places\n";
    my $tmp = $dividend;
    my $negate = "";
    if (($tmp < 0 && $divisor > 0) || ($tmp > 0 && $divisor < 0)) {
        $negate = "-";
        $tmp = -$tmp;
    } elsif ($tmp < 0 && $divisor < 0) {
        $tmp = -$tmp;
        $divisor = -$divisor;
    }
    my $quotient = 0;
    my $ptmp = $precision;
    my $remainder;
    while ( $tmp >= $divisor ) {
        $tmp = $tmp - $divisor;
        $quotient++;
#        print "Cycle $quotient: \$tmp = $tmp\n";
        if ( $tmp == 0 ) {
            return $negate.$quotient;
        }
    }
    $ptmp--;
    if ( $ptmp >= 0 ) {
        $tmp = &multiply( $tmp, 10 );
        $remainder = &divide($tmp,$divisor,$ptmp,1);
    }

    if (defined($level)) {
        return $negate.$quotient.$remainder;
    } else {
#        print "$dividend divided by $divisor to $precision decimal places = ";
        if ( $precision > 0 ) {
            return $negate.$quotient.".".$remainder;
        } else {
            return $negate.$quotient;
        }
#        print "\n";
    }
}

##
## Brute force multiplication
##  Add the first number a multiplier number of times to itself.
##
sub multiply() {
    my($num,$multiplier) = @_;
#    print "Multiplying $num by $multiplier = ";
    my $result = 0;

    for ($i=0;$i < $multiplier;$i++) {
        $result += $num;
    }
#    print "$result\n";
    return $result;
}

sub modulo() {
    my($dividend,$divisor) = @_;

    if ($dividend < 0) {
        $dividend = -$dividend;
    }
    while ($dividend >= $divisor) {
        $dividend -= $divisor;
    }
    return $dividend;
}

sub power() {
    my($num,$power) = @_;
    my $negate = 0;

    if (&modulo($power,2) == 0 && $num < 0) {
        $num = -$num;
    } elsif ($num < 0) {
        $negate = 1;
        $num = -$num;
    }

    my $result = $num;

    if ($power < 0) {
        $result = 1 / &power($num,-$power);
    } elsif ($power == 0) {
        $result = 1;
    } elsif ($power == 1) {
        $result = $num;
    } else {
        while ( $power > 1 ) {
            $result = &multiply($result,$num);
            $power--;
        }
    }
    if ($negate == 1) {
        $result = -$result;
    }
    return $result;
}

$dividend = -10;
$divisor = -2;
$precision = 5;
print "$dividend divided by $divisor = ".&divide($dividend,$divisor,$precision)."\n";

$num = -2;
$power = -3;
print "${num}^${power} = ".&power($num,$power)."\n";

##
## Pi calculation...brute force by Leibnitz's formula
##
# $tmp = 1;
# $idx = 1;
# $pi = 0;
# $precision = 50000000;
# while ( $idx < $precision ) {
#     if ( ($tmp % 2 ) != 0 ) {
#         if ( ($idx % 2) != 0 ) {
#             $pi += (1 / $tmp);
#         } else {
#             $pi -= (1 / $tmp);
#         }
#         $idx++;
#     }
#     $tmp++;
# }
# print "pi = ".($pi * 4)."\n";


