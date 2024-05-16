#!/usr/bin/perl

use GD;

### Initialize the image
my $x_size = 512;
my $y_size = 384;
my $min_water = .60;
my $max_water = .80;
my $area = $x_size * $y_size;
my $min_area = int( $x_size * $y_size * ( 1 - $max_water ) );
my $max_area = int( $x_size * $y_size * ( 1 - $min_water ) );
print "Min land area = $min_area\n";
print "Max land area = $max_area\n";

my $filename = "test.png";
my $myImage = GD::Image->new($x_size,$y_size,1) || die;

### Colors to use (rbg.txt name)
### 0 -> blue (azure)
### 1 -> green (spring green)
### 2 -> yellow-green (yellow green)
### 3 -> light brown (sandy brown)
### 4 -> dark brown (brown)
### 5 -> grey
### 6 -> white (snow white)
### 7 -> red (red)

my @color = ();
$color[0] = $myImage->colorAllocate(0,0,128);
$color[1] = $myImage->colorAllocate(0,250,0);
$color[2] = $myImage->colorAllocate(154,205,50);
$color[3] = $myImage->colorAllocate(244,164,96);
$color[4] = $myImage->colorAllocate(165,42,42);
$color[5] = $myImage->colorAllocate(127,127,127);
$color[6] = $myImage->colorAllocate(250,250,250);
$color[7] = $myImage->colorAllocate(0,0,0);

my @bitmap = ();

$myImage->fill(0,0,$color[0]);

my $cnt = 0;
my $x_pos = int(rand($x_size));
my $y_pos = int(rand($y_size));
my $lastmove;

while ( $cnt < $max_area ) {
    if ( $cnt > $min_area ) {
        last if ( int(rand(50000)) == 0 );
    }
    $color_idx = $myImage->getPixel($x_pos,$y_pos);
    if ( ! defined($bitmap[$x_pos][$y_pos]) ) {
        $bitmap[$x_pos][$y_pos] = 1;
        $cnt++;
    } elsif ( $bitmap[$x_pos][$y_pos] < 6 ) {
        $bitmap[$x_pos][$y_pos]++;
    } else {
        if ( int(rand(5000)) == 0 ) {
            print "Special location $x_pos, $y_pos\n" if ( $bitmap[$x_pos][$y_pos] == 6 );
            $bitmap[$x_pos][$y_pos]++ if ( $bitmap[$x_pos][$y_pos] == 6 );
        }
    }
    $myImage->setPixel($x_pos,$y_pos,$color[$bitmap[$x_pos][$y_pos]]);
    my $move = int(rand(34));
    if ( $move == 0 ) {
        if ( int(rand(1000)) == 0 ) {
            $x_pos = int(rand($x_size));
            $y_pos = int(rand($y_size));
        }
    } elsif ( $move == 1 ) {
        $x_pos += 0;
        $y_pos += 0;
    } elsif ( $move == 2 || $move == 10 || $move == 18 || $move == 26 || $move == 30 ) {
        $y_pos -= 1;
    } elsif ( $move == 3 || $move == 11 || $move == 19 || $move == 27 || $move == 31 ) {
        $x_pos += 1;
    } elsif ( $move == 4 || $move == 12 || $move == 20 || $move == 28 || $move == 32 ) {
        $y_pos += 1;
    } elsif ( $move == 5 || $move == 13 || $move == 21 || $move == 29 || $move == 33 ) {
        $x_pos -= 1;
    } elsif ( $move == 6 || $move == 14 || $move == 22 ) {
        $x_pos -= 1;
        $y_pos -= 1;
    } elsif ( $move == 7 || $move == 15 || $move == 23 ) {
        $x_pos += 1;
        $y_pos -= 1;
    } elsif ( $move == 8 || $move == 16 || $move == 24 ) {
        $x_pos += 1;
        $y_pos += 1;
    } elsif ( $move == 9 || $move == 17 || $move == 25 ) {
        $x_pos -= 1;
        $y_pos += 1;
    }
    if ( $x_pos < 0 ) {
        $x_pos += $x_size;
    } elsif ( $x_pos >= $x_size ) {
        $x_pos -= $x_size;
    }
    if ( $y_pos < 0 ) {
        $y_pos += $y_size;
    } elsif ( $y_pos >= $y_size ) {
        $y_pos -= $y_size;
    }
}

my $pct = ( $cnt / $area ) * 100;
print "Colored $cnt pixels, covering $pct of the background\n";
print "Finished generating GD data.  Outputting to png\n";
my $png_data = $myImage->png;
open(DISPLAY,">$filename") || die;
binmode DISPLAY;
print DISPLAY $png_data;
close DISPLAY;
