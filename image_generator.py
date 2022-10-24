from PIL import Image, ImageDraw

import numpy as np
import pandas as pd
import datetime
from collections import namedtuple


DayData = namedtuple('month','day')
TempData = namedtuple('lo','hi')

MYDATA = pd.read_csv("dataUSW00003960.csv")


THERANGE= max(MYDATA.TMAX) - min(MYDATA.TMIN)
BIN_SIZE = THERANGE// 15
COMMONDAYS ={1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31  }




def extract_data(x_entry):
    """Description of the function/method.
    Extra TMIN and TMAX data from a row of the weather data frame
Parameters:
    <param>: Description of the parameter
    Row from a weather data frame
Returns:
    <variable>: Description of the return value
    an updated dictionary
"""
    mydate = x_entry.DATE
    mydate = datetime.datetime.strptime(mydate, "%Y-%m-%d")
    mym = mydate.month
    myd = mydate.day
    x_tmin = x_entry.TMIN
    x_tmax = x_entry.TMAX
    return DayData(mym, myd), TempData(x_tmin, x_tmax)



def create_weather_dict(weather_data):
    local_dict={}
    thelength = len(weather_data)
    for i in range(thelength):
      day_info, temp_info = extract_data(weather_data.loc[i])
      if local_dict.get(day_info) is None:
            local_dict.update({day_info:temp_info})
    return local_dict


mycolordict={}
colorscore=[]

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

