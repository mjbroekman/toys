'''
Created on Feb 13, 2010

@author: broekman
'''
import sys
import random
import tkinter

from tkinter import Canvas
from tkinter import *

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
    
def gen_map(self, mapX, mapY):
        maparea = mapX*mapY
        x=0
        startX=random.randrange(0,mapX)
        startY=random.randrange(0,mapY)
        while x < maparea:
            x = x+1
            move=random.randrange(0,30)
             

if __name__ == '__main__':
    print("Hello Map Creator\n")

mywidth, myheight = int(sys.argv[1]), int(sys.argv[2])
myarea = mywidth*myheight
print("Height =", myheight)
print("Width =", mywidth)
print("Total Area =", myarea)

# create the application
myapp = App()

print(dir(tkinter.BitmapImage))
#
# here are method calls to the window manager class
#
mytitle = "My",mywidth,"x",myheight,"Map"
myapp.master.title(mytitle)
myapp.master.minsize(mywidth, myheight)
myapp.master.maxsize(mywidth,myheight)

# start the program
# myapp.mainloop()
