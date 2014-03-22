#!/usr/bin/env python

import sys, getopt

# Defaults
debug = 0

def main(argv):
    output = "testimage.png"
    x_size = 1024
    y_size = 1024
    max_land = 65
    min_land = 35

    try:
        opts, args = getopt.getopt(argv,"hdx:y:m:n:o:")
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
            x_size = int(arg)
        elif opt in ("-y"):
            y_size = int(arg)
        elif opt in ("-m"):
            max_land = int(arg)
        elif opt in ("-n"):
            min_land = int(arg)
        elif opt in ("-d"):
            global debug
            debug += 1

    mk_image( output, x_size, y_size, max_land, min_land )


def mk_image( output, x_size, y_size, max_land, min_land ):
    from PIL import Image, ImageDraw
    import random

    global debug

    blue = (0,0,128)
    green = (0,250,0)
    yellow = (154,205,50)
    ltbrown = (200,164,96)
    dkbrown = (100,42,42)
    grey = (127,127,127)
    white = (250,250,250)
    black = (0,0,0)
    red = (255,0,0)
    colors = [blue, green, yellow, ltbrown, dkbrown, grey, white, black, red]
    color = (0,0,0)

    total_size = (x_size * y_size)
    min_area = int(total_size * min_land / 100)
    max_area = int(total_size * max_land / 100)
    count = 0

    if debug > 0:
        print 'Creating map file ' + output + ': X size = ' + str(x_size) + ', Y size = ' + str(y_size)
        print '\t\t Minimum landmass = ' + str(min_land) + '% (' + str(min_area) + ' land pixels)'
        print '\t\t Maximum landmass = ' + str(max_land) + '% (' + str(max_area) + ' land pixels)'
        print '\t\t Total pixels = ' + str(total_size)
        print '\t\t Color depth = ' + str(len(colors))
        print '\t\t Color Index 0 = ' + str(colors[0])
        print '\t\t Color Index 1 = ' + str(colors[1])
        print '\t\t Color Index 2 = ' + str(colors[2])
        print '\t\t Color Index 3 = ' + str(colors[3])
        print '\t\t Color Index 4 = ' + str(colors[4])
        print '\t\t Color Index 5 = ' + str(colors[5])
        print '\t\t Color Index 6 = ' + str(colors[6])
        print '\t\t Color Index 7 = ' + str(colors[7])
        print '\t\t Color Index 8 = ' + str(colors[8])
        print '\t\t Color Length -1 = ' + str(colors[len(colors) - 1])
        print '\t\t Color Length -2 = ' + str(colors[len(colors) - 2])
        print str(len(colors) - 3)
        print str(len(colors) - 2)
        print str(len(colors) - 1)

    mapsize = (x_size,y_size)
    mapimage = Image.new('RGB', mapsize, blue)

    start_x = random.randrange(x_size)
    start_y = random.randrange(y_size)

    x = start_x
    y = start_y

    if debug > 0:
        print 'Starting at ' + str(start_x) + ',' + str(start_y)

    while count < max_area:
        if count > min_area:
            if random.randrange(50000) == 0:
                break

        mappixel = mapimage.getpixel( (x,y) )

        try:
            color_idx = colors.index( mappixel )
        except ValueError:
            print "Error in getting color index at " + str(mappixel)

        if debug > 0:
            print "Pixel " + str( (x,y) ) + " = " + str( mappixel ) + " (Index: " + str(color_idx) + ")"

        if color_idx == 0:
            if debug > 1:
                print "Generating land."
            count += 1
            color_idx += 1
        elif color_idx > 0 and color_idx < (len(colors) - 3):
            if debug > 1:
                print "Raising land"
            color_idx += 1
        if color_idx >= (len(colors) - 2):
            if debug > 1:
                print "Removing special location at " + str( (x,y) )
            color_idx = len(colors) - 2
        # elif color_idx == -1:
        #     color = red

        color = colors[color_idx]

        if random.randrange(15000) == 0:
            color = red
            if debug > 0:
                print "Special location at " + str((x,y))

        mapimage.putpixel( (x,y), color )

        # Move to a new spot
        move = random.randrange(34)
        if move == 0:
            if random.randrange(1000) == 0:
                x = random.randrange(x_size)
                y = random.randrange(y_size)
                if debug > 0:
                    print "Reset position to " + str( (x,y) )
        elif move == 1:
            x = x
            y = y
        elif move == 2 or move == 10 or move == 18 or move == 26 or move == 30:
            y -= 1
        elif move == 3 or move == 11 or move == 19 or move == 27 or move == 31:
            x += 1
        elif move == 4 or move == 12 or move == 20 or move == 28 or move == 32:
            x -= 1
        elif move == 5 or move == 13 or move == 21 or move == 29 or move == 33:
            y += 1
        elif move == 6 or move == 14 or move == 22:
            x -= 1
            y -= 1
        elif move == 7 or move == 15 or move == 23:
            x += 1
            y -= 1
        elif move == 8 or move == 16 or move == 24:
            x += 1
            y += 1
        elif move == 9 or move == 17 or move == 25:
            x -= 1
            y += 1

        if x < 0:
            x = ( x + x_size - 1 )
        elif x >= x_size:
            x = ( x - x_size )

        if y < 0:
            y = ( y + y_size - 1 )
        elif y >= y_size:
            y = ( y - y_size )

    pct = int( ( ( float(count) / float(total_size) ) * 100.0 ) * 100 )
    pct = ( float(pct) / 100.0 )

    print "Created " + str(count) + " land pixels.  This covers " + str(pct) + " of the world."

    mapimage.save(output, 'PNG')


if __name__ == "__main__":
   main(sys.argv[1:])


# my $pct = ( $cnt / $area ) * 100;
# print "Colored $cnt pixels, covering $pct of the background\n";
# print "Finished generating GD data.  Outputting to png\n";
# my $png_data = $myImage->png;
# open(DISPLAY,">$filename") || die;
# binmode DISPLAY;
# print DISPLAY $png_data;
# close DISPLAY;
