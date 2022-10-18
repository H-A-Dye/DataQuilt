from PIL import Image, ImageDraw

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime


mydata = pd.read_csv("3077594.csv")

maxv = mydata.TMAX
minv=mydata.TMIN

therange= max(mydata.TMAX) - min(mydata.TMAX)
bin = therange// 15

mycolordict=dict()
colorscore=[]

for i,x in enumerate(mydata.TMAX[0:365]):
    newval = x - min(mydata.TMAX)
    xscore = newval//bin
    colorscore.append(xscore)
    mydate = datetime.datetime.strptime(mydata.DATE[i], "%Y-%m-%d")
    mym = mydate.month
    myd = mydate.day
    if mym=='' or myd =='':
        print(mydata.DATE[i])
        print('mym {}'.format(mym))
        print('myd {}'.format(myd))
    mycolordict.update({(mym,myd): xscore})

COLORBASE=(0,0,256)
STEP = 256/15


def make_color_list():
    colorlist=[]
    for x in range(15):
        newvalue = COLORBASE + (x*STEP,0,-x*STEP)
        colorlist.append(newvalue)
    return colorlist

im = Image.new(mode ="RGB",size=(270, 370), color=(256,256,256) )
draw=ImageDraw.Draw(im)
draw.line([0,30,270, 30], fill = 1, width=1)
draw.line([0,340,270,340],fill=1, width=1)
draw.rectangle([20,30, 30,40],fill=(0,0,255), outline=1)
# im.show()