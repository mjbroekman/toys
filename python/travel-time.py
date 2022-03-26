#!/usr/bin/python3

import os
import sys
print('OS Name ' + sys.platform + "\n");
print("Hello world.\n");
au = 149600000000;
earth_au = 5.1 * au;
accel = 9.8 * 2;
time_sq = 2.0 * earth_au / accel
time_sec = time_sq ** 0.5
time_min = time_sec / 60
time_hr = time_min / 60
print("It will take " + str(time_hr) + " hours before you need to flip at " + str(accel) + "m/s^2 to cross " + str(earth_au) + "meters\n");
