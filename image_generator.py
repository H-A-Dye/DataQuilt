"""Description of the module.
   This module takes a weather data frame and creates a diagram
   of a temperature quilt.
Classes:
    <class>

Functions:
    <function>

Misc. variables:
    <variable>
"""
import datetime
from collections import namedtuple
from typing import NamedTuple
from PIL import Image, ImageDraw
import pandas as pd




DayData = namedtuple("DayData","month,day")
TempData = namedtuple("TempData","lo,hi")

MYDATA = pd.read_csv("dataUSW00003960.csv")


THERANGE= max(MYDATA.TMAX) - min(MYDATA.TMAX)
THEMIN = min(MYDATA.TMAX)
BIN_SIZE = THERANGE// 15
COMMONDAYS ={1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31  }
COLORBASE=(0,0,256)
STEP = 256//15



def extract_data(x_entry: pd.Series) -> tuple[DayData, TempData]: # TODO: check whether pd.Series is correct
    """Extra TMIN and TMAX data from a row of the weather data frame

    Parameters:
        x_entry: a row of the weather data frame

    Returns:
        thedate: month and day for the weather data
        thetemp: temperature of the weather data
    """
    mydate = x_entry.DATE
    mydate = datetime.datetime.strptime(mydate, "%Y-%m-%d")
    mym = mydate.month
    myd = mydate.day
    x_tmin = x_entry.TMIN
    x_tmax = x_entry.TMAX
    thedate = DayData(mym,  myd)
    thetemp = TempData(x_tmin, x_tmax)

    return thedate, thetemp



def create_weather_dict(weather_data):
    """Description of the function/method.
    Takes a weather data frame and creates a weather dictionary 
    with the data organized as needed for the diagram
Parameters:
    <param>: Weather Data Frame

Returns:
    <variable>: Returns a weather dictionary
"""
    local_dict={}
    thelength = len(weather_data)
    for i in range(thelength):
      day_info, temp_info = extract_data(weather_data.loc[i])
      if local_dict.get(day_info) is None:
            local_dict.update({day_info:temp_info})
    return local_dict



def grade_temp(temperature: int):
    """Description of the function/method.
    Takes an integer temperature and grades it relative to
    the bin size and min temperature
Parameters:
    <param>: temperature int
Returns:
    <variable>: level int
"""
    temperature = temperature - THEMIN
    color = temperature // BIN_SIZE
    return color 

def make_color(local_level: int):
    """Description of the function/method.
    Generates a RGB color based on integer. This should get replaced 
    with swatch.
Parameters:
    <param>: Level from 0 to 14
Returns:
    <variable>: Returns an RGB value
"""
    colorrgb = (0 + local_level*STEP,255 - local_level*10,256 - local_level*5)
    return colorrgb




def add_month_to_image(weather_dict, drawobject, month_number=1):
    """Description of the function/method.
    Add each month of data to the diagram.
Parameters:
    <param>: weather_dictionary -
             month to draw
             diagram
Returns:
    <variable>: None
"""
    days = COMMONDAYS.get(month_number)
    if len(weather_dict)==366 and month_number==2:
        days = days+1
    for i in range(days):
        x_1=month_number*20
        x_2=x_1+10
        y_1=30+i*10
        y_2=y_1+10
        hitemp=weather_dict.get(DayData(month_number,i+1)).hi
        level = grade_temp(hitemp)
        if level is None:
            print("uh oh")
            level=1
        drawobject.rectangle([x_1,y_1,x_2,y_2], fill=make_color(level),outline=1)

def the_main():
    """Description of the function/method.
    Create the diagram and show
Parameters:
    <param>: none

Returns:
    <variable>: none
"""
    weather_dict = create_weather_dict(MYDATA)
    local_im = Image.new(mode="RGB", size=(270, 370), color=(256, 256, 256))
    draw = ImageDraw.Draw(local_im)
    draw.line([0, 30, 270, 30], fill=1, width=1)
    draw.line([0, 340, 270, 340], fill=1, width=1)
    for i in range(12):
        add_month_to_image(weather_dict, draw, i+1)
    local_im.show()
