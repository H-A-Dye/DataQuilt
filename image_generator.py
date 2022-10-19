from PIL import Image, ImageDraw

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import random


mydata = pd.read_csv("3077594.csv")

maxv = mydata.TMAX
minv=mydata.TMIN

therange= max(mydata.TMAX) - min(mydata.TMAX)
bin = therange// 15

FAKEDATA = [random.randint(0,14) for x in range(365)]

COMMONDAYS ={1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31  }

mycolordict=dict()
colorscore=[]

def create_a_color_dict_fake():
    mycolordict=dict()
    for i,x in enumerate(mydata.TMAX[0:365]):
    #newval = x - min(mydata.TMAX)
    #xscore = newval//bin
    #colorscore.append(xscore)
        mydate = datetime.datetime.strptime(mydata.DATE[i], "%Y-%m-%d")
        mym = mydate.month
        myd = mydate.day

    #mycolordict.update({(mym,myd): xscore})
        mycolordict.update({(mym, myd):FAKEDATA[i]})
    return mycolordict

COLOR_DATE_DICT=create_a_color_dict_fake()
COLORBASE=(0,0,256)
STEP = 256//15


def make_color_list():
    colorlist=[]
    for x in range(15):
        newvalue = (0 + x*STEP,0,256 - x*STEP)
        colorlist.append(newvalue)
    return colorlist

COLORLIST =make_color_list()


def add_month_to_image(drawobject, month_number=1):
    days = COMMONDAYS.get(month_number)
    if len(FAKEDATA)==366 and month_number==2:
        days = days+1
    for x in range(days):
        x1=month_number*20
        x2=x1+10
        y1=30+x*10
        y2=y1+10
        colorlevel=COLOR_DATE_DICT.get((month_number,x+1))
        if colorlevel is None:
            print("uh oh")
            colorlevel=1
        drawobject.rectangle([x1,y1,x2,y2], fill=COLORLIST[colorlevel],outline=1)


im = Image.new(mode="RGB", size=(270, 370), color=(256, 256, 256))
draw = ImageDraw.Draw(im)
draw.line([0, 30, 270, 30], fill=1, width=1)
draw.line([0, 340, 270, 340], fill=1, width=1)
for x in range(12):
    add_month_to_image(draw, x+1)

