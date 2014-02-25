#!/usr/bin/env python

import sys, getopt

def main(argv):

    x_size = 0
    y_size = 0
    min_land = 0
    max_land = 0
    output = ""

    try:
        opts, args = getopt.getopt(argv,"hx:y:m:n:o:")
    except getopt.GetoptError:
        print 'mk_image.py -x <image width> -y <image height> -m <max "land"> -n <min "land"> -o <outputfile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'mk_image.py -x <image width> -y <image height> -m <max "land"> -n <min "land"> -o <outputfile>'
            sys.exit()
        elif opt in ("-o"):
            output = arg
        elif opt in ("-x"):
            x_size = arg
        elif opt in ("-x"):
            y_size = arg
        elif opt in ("-m"):
            max_land = arg
        elif opt in ("-n"):
            min_land = arg

    mk_image( output, x_size, y_size, max_land, min_land )


def mk_image( output = "/Users/mbroekman/testimage.png" , x_size = 2048, y_size = 2048, max_land = 80, min_land = 35 ):
    from PIL import Image, ImageDraw

    blue = (0,0,128)
    green = (0,250,0)
    yellow = (154,205,50)
    ltbrown = (244,164,96)
    dkbrown = (165,42,42)
    grey = (127,127,127)
    white = (250,250,250)
    black = (0,0,0)
    red = (128,0,0)

    colors = (blue, green, yellow, ltbrown, dkbrown, grey, white, red, black)

    mapsize = ( x_size, y_size )
    mapimage = Image.new('RGB', mapsize, blue)
    mapdraw = ImageDraw.Draw(mapimage)

    label_pos = (10,10) # top-left position of our text
    label = "My New World" # text to draw

    mapdraw.text(label_pos, label, fill=black)

    del mapdraw

    mapimage.save(output, 'PNG')


if __name__ == "__main__":
   main(sys.argv[1:])

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)


# my @bitmap = ();

# $myImage->fill(0,0,$color[0]);

# my $cnt = 0;
# my $x_pos = int(rand($x_size));
# my $y_pos = int(rand($y_size));
# my $reset = 0;
# my $lastmove;

# while ( $cnt < $max_area ) {
#     if ( $cnt > $min_area ) {
#         last if ( int(rand(5000)) == 0 );
#     }
#     $color_idx = $myImage->getPixel($x_pos,$y_pos);
#     if ( ! defined($bitmap[$x_pos][$y_pos]) ) {
#         $bitmap[$x_pos][$y_pos] = 1;
#         $cnt++;
#     } elsif ( $bitmap[$x_pos][$y_pos] < 6 ) {
#         $bitmap[$x_pos][$y_pos]++;
#     } else {
#         if ( int(rand(500)) == 0 ) {
#             print "Special location $x_pos, $y_pos\n" if ( $bitmap[$x_pos][$y_pos] == 6 );
#             $bitmap[$x_pos][$y_pos]++ if ( $bitmap[$x_pos][$y_pos] == 6 );
#         }
#     }
#     $myImage->setPixel($x_pos,$y_pos,$color[$bitmap[$x_pos][$y_pos]]);
#     my $move = int(rand(34));
#     if ( $reset == 1 ) {
#         $x_pos = int(rand($x_size));
#         $y_pos = int(rand($y_size));
#         print "Reset flag set.  New position = $x_pos, $y_pos\n";
#         $reset = 0;
#     } elsif ( $move == 0 ) {
#         if ( int(rand(100)) == 0 ) {
#             $x_pos = int(rand($x_size));
#             $y_pos = int(rand($y_size));
#             print "Reset position to $x_pos, $y_pos\n";
#         }
#     } elsif ( $move == 1 ) {
#         $x_pos += 0;
#         $y_pos += 0;
#     } elsif ( $move == 2 || $move == 10 || $move == 18 || $move == 26 || $move == 30 ) {
#         $y_pos -= 1;
#     } elsif ( $move == 3 || $move == 11 || $move == 19 || $move == 27 || $move == 31 ) {
#         $x_pos += 1;
#     } elsif ( $move == 4 || $move == 12 || $move == 20 || $move == 28 || $move == 32 ) {
#         $y_pos += 1;
#     } elsif ( $move == 5 || $move == 13 || $move == 21 || $move == 29 || $move == 33 ) {
#         $x_pos -= 1;
#     } elsif ( $move == 6 || $move == 14 || $move == 22 ) {
#         $x_pos -= 1;
#         $y_pos -= 1;
#     } elsif ( $move == 7 || $move == 15 || $move == 23 ) {
#         $x_pos += 1;
#         $y_pos -= 1;
#     } elsif ( $move == 8 || $move == 16 || $move == 24 ) {
#         $x_pos += 1;
#         $y_pos += 1;
#     } elsif ( $move == 9 || $move == 17 || $move == 25 ) {
#         $x_pos -= 1;
#         $y_pos += 1;
#     }
#     if ( $x_pos < 0 ) {
#         $x_pos += $x_size;
#     } elsif ( $x_pos >= $x_size ) {
#         $x_pos -= $x_size;
#     }
#     if ( $y_pos < 0 ) {
#         $y_pos = 0;
#         $reset = 1;
#     } elsif ( $y_pos >= $y_size ) {
#         $y_pos = $y_size - 1;
#         $reset = 1;
#     }
# }

# my $pct = ( $cnt / $area ) * 100;
# print "Colored $cnt pixels, covering $pct of the background\n";
# print "Finished generating GD data.  Outputting to png\n";
# my $png_data = $myImage->png;
# open(DISPLAY,">$filename") || die;
# binmode DISPLAY;
# print DISPLAY $png_data;
# close DISPLAY;
