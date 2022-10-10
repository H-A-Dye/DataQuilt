import os
from collections import namedtuple
import csv
import pandas
import pandas as pd
import requests
from urllib.request import urlretrieve
from geopy.geocoders import Nominatim

# Set up to select weather station
# reference package 1: https://github.com/gojiplus/get-weather-data/blob/master/zip2ws/zip2ws.py
# reference package 2: https://github.com/paulokuong/noaa

# retrieve the list of weather stations

# Get the zip code and convert to latitude and longitude using geocoder
PATH = os.getcwd()
Local = os.path.join(PATH,'ws.txt')

WS = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt'
#urlretrieve(WS,Local)

WSlist=Local

Station = namedtuple("Station", {'name', 'lat', 'long', 'start','end'})
# sort the list and reduce to contain only weather stations with TMAX - TMAX List

def filter_ws():
    mywslist=[]
    with open(Local, encoding='utf8') as t_file:
        mydata = t_file.readlines()
    for x in mydata:
        if x.find('TMAX')!=-1:
            ind=x.find(' ')
            myst=x[0:ind]
            newv=x[ind:].lstrip()
            ind=newv.find(' ')
            mylat = newv[0:ind]
            newv=newv[ind: ].lstrip()
            ind=newv.find(' ')
            mylong = newv[0:ind]
            newv=newv[ind: ].lstrip()
            s=newv.split(' ')

            mystation = Station(name=myst,lat=mylat,long=mylong,start=s[1], end=s[2].strip('\n'))
            mywslist.append(mystation)


    return mywslist

def data_into_df(data):
    mydf=pd.DataFrame(data)
    return mydf

# Get the zip code and convert to latitude and longitude using geocoder

#try1 using pygeocoder - this does not work.
def zip2latlong(zipcode):
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.geocode(zipcode)
    return location.latitude, location.longitude

# try2 use https://geopy.readthedocs.io/en/stable/#module-geopy.geocoders

# Compute the distance to each weather station and choose the top 5 or so, return to the GetData.