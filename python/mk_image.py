#!/usr/bin/env python
"""
Make a random image that might or might not be suitable for a 'world map'
"""
from __future__ import print_function
import sys
import getopt

def main(argv):
    """
    Main processing of arguments
    """
    output = "testimage.png"
    x_size = 1024
    y_size = 1024
    max_land = 65
    min_land = 35
    debug = 0

    try:
        opts = getopt.getopt(argv, "hdx:y:m:n:o:")
    except getopt.GetoptError:
        print('mk_image.py ', end='')
        print('-x <image width> -y <image height> ', end='')
        print('-m <max "land"> -n <min "land"> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('mk_image.py ', end='')
            print('-x <image width> -y <image height> ', end='')
            print('-m <max "land"> -n <min "land"> -o <outputfile>')
            sys.exit()
        elif opt in "-o":
            output = arg
        elif opt in "-x":
            x_size = int(arg)
        elif opt in "-y":
            y_size = int(arg)
        elif opt in "-m":
            max_land = int(arg)
        elif opt in "-n":
            min_land = int(arg)
        elif opt in "-d":
            debug += 1

    mk_image({'output':output,
              'x_size':x_size,
              'y_size':y_size,
              'max_land':max_land,
              'min_land':min_land,
              'debug':debug})



def dbg_print(debug, dbg_limit, msg):
    """
    Print only if debug var is over the limit
    """
    if debug > dbg_limit:
        print(msg)



def bnd_check(lngt, latd, data):
    """
    Check boundary conditions
    """
    if lngt < 0:
        lngt = (lngt + data['x_size'] - 1)
    elif lngt >= data['x_size']:
        lngt = (lngt - data['x_size'])

    if latd < 0:
        latd = (latd + data['y_size'] - 1)
    elif latd >= data['y_size']:
        latd = (latd - data['y_size'])

    return (lngt, latd)



def move_cursor(lngt, latd, move, data):
    """
    Move to a new spot
    """
    import random

    # move == 0: random relocation
    # move == 1: no change (elevate)
    # move == 2 + ( x * 8 ) : south
    # move == 3 + ( x * 8 ) : north
    # move == 4 + ( x * 8 ) : west
    # move == 5 + ( x * 8 ) : east
    # move == 6 + ( x * 8 ) : southwest
    # move == 7 + ( x * 8 ) : northwest
    # move == 8 + ( x * 8 ) : northeast
    # move == 9 + ( x * 8 ) : southeast
    if move == 0 and random.randrange(1000) == 0:
        lngt = random.randrange(data['x_size'])
        latd = random.randrange(data['y_size'])
        dbg_print(data['debug'], 0, "Reset position to " + str((lngt, latd)))
    elif move == 2 or move == 10 or move == 18 or move == 26 or move == 30:
        latd -= 1
    elif move == 3 or move == 11 or move == 19 or move == 27 or move == 31:
        lngt += 1
    elif move == 4 or move == 12 or move == 20 or move == 28 or move == 32:
        lngt -= 1
    elif move == 5 or move == 13 or move == 21 or move == 29 or move == 33:
        latd += 1
    elif move == 6 or move == 14 or move == 22:
        lngt -= 1
        latd -= 1
    elif move == 7 or move == 15 or move == 23:
        lngt += 1
        latd -= 1
    elif move == 8 or move == 16 or move == 24:
        lngt += 1
        latd += 1
    elif move == 9 or move == 17 or move == 25:
        lngt -= 1
        latd += 1

    return bnd_check(lngt, latd, data)



def get_color(color_idx, colors, data):
    """
    Determine what color to make the pixel
    """
    if color_idx == 0:
        dbg_print(data['debug'], 1, "Generating land.")
        data['count'] += 1
        color_idx += 1
    elif color_idx > 0 and color_idx < (len(colors) - 3):
        dbg_print(data['debug'], 1, "Raising land")
        color_idx += 1
    if color_idx >= (len(colors) - 2):
        dbg_print(data['debug'], 1, "Removing special location.")
        color_idx = len(colors) - 2
    # elif color_idx < 0:
    #     color = colors[len(colors) - 1]

    return colors[color_idx]



def mk_image(data):
    """
    Main image generation
    """
    from PIL import Image
    from PIL import ImageDraw
    import random

    colors = [
        (0, 0, 128), # blue
        (0, 250, 0), # green
        (154, 205, 50), # yellow
        (200, 164, 96), # light brown
        (100, 42, 42), # dark brown
        (127, 127, 127), #grey
        (250, 250, 250), # white
        (0, 0, 0), # black
        (255, 0, 0) # red - special locations
        ]
    color = (0, 0, 0)

    data['total_size'] = (data['x_size'] * data['y_size'])
    data['min_area'] = int(data['total_size'] * data['min_land'] / 100)
    data['max_area'] = int(data['total_size'] * data['max_land'] / 100)
    data['count'] = 0

    dbg_print(data['debug'], 0,
              'Creating map file '+data['output']+': ')
    dbg_print(data['debug'], 0,
              'X size = '+str(data['x_size'])+', Y size = '+str(data['y_size']))
    dbg_print(data['debug'], 0,
              '\t\tMinimum landmass = '+str(data['min_land'])+'%')
    dbg_print(data['debug'], 0,
              '\t\t\t'+str(data['min_area'])+' land pixels)')
    dbg_print(data['debug'], 0,
              '\t\tMaximum landmass = '+str(data['max_land'])+'%')
    dbg_print(data['debug'], 0,
              '\t\t\t'+str(data['max_area'])+' land pixels)')
    dbg_print(data['debug'], 0,
              '\t\tTotal pixels = '+str(data['total_size']))
    dbg_print(data['debug'], 0,
              '\t\tColor depth = '+str(len(colors)))

    data['mapsize'] = (data['x_size'], data['y_size'])
    mapimage = Image.new('RGB', data['mapsize'], colors[0])

    data['start_x'] = random.randrange(data['x_size'])
    data['start_y'] = random.randrange(data['y_size'])

    lngt = data['start_x']
    latd = data['start_y']

    dbg_print(data['debug'], 0,
              'Starting at ' + str(data['start_x']) + ',' + str(data['start_y']))

    while data['count'] < data['max_area']:
        if data['count'] > data['min_area']:
            if random.randrange(50000) == 0:
                break

        mappixel = mapimage.getpixel((lngt, latd))

        try:
            color_idx = colors.index(mappixel)
        except ValueError:
            print("Error in getting color index at " + str(mappixel))

        dbg_print(data['debug'], 0,
                  "Pixel "+str((lngt, latd))+" = "+str(mappixel)+" (Index: "+str(color_idx)+")")

        color = get_color(color_idx, colors, data)

        if random.randrange(15000) == 0:
            color = colors[len(colors) - 1]
            dbg_print(data['debug'], 0, 'Special location at '+str((lngt, latd)))

        mapimage.putpixel((lngt, latd), color)

        (lngt, latd) = move_cursor(lngt, latd, random.randrange(34), data)

    pct = int(((float(data['count']) / float(data['total_size'])) * 100.0) * 100)
    pct = (float(pct) / 100.0)

    print("Created "+str(data['count'])+" land pixels.  This covers "+str(pct)+" of the world.")

    mapimage.save(data['output'], 'PNG')



if __name__ == "__main__":
    main(sys.argv[1:])


# my $pct = ( $cnt / $area ) * 100;
# print("Colored $cnt pixels, covering $pct of the background\n";
# print("Finished generating GD data.  Outputting to png\n";
# my $png_data = $myImage->png;
# open(DISPLAY,">$filename") || die;
# binmode DISPLAY;
# print(DISPLAY $png_data;
# close DISPLAY;
