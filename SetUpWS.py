import os
from collections import namedtuple
import math
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

WeatherStations = data_into_df(filter_ws())

def write_df_to_file(df):
    # write the short (40,0000) to a file?
    pass

# Get the zip code and convert to latitude and longitude using geocoder

#try1 using pygeocoder - this does not work.
def zip2latlong(zipcode):
    # positive lat is north, positive long is east
    geolocator = Nominatim(user_agent="my_app")
    country = 'USA'
    location = geolocator.geocode(str(zipcode)  + ',' + country)
    return location.latitude, location.longitude

# try2 use https://geopy.readthedocs.io/en/stable/#module-geopy.geocoders

# Compute the distance to each weather station and choose the top 5 or so, return to the GetData.

def convert_latlong(value):
    v2, v1 = math.modf(value)
    v2 = v2*100 / 60
    val = v1 +v2
    val=val*math.pi /180
    return val



def dist_between(lat1, long1, lat2, long2):
    # d=2*asin(sqrt((sin((lat1-lat2)/2))^2 +
    #                  cos(lat1)*cos(lat2)*(sin((lon1-lon2)/2))^2))  from edwilliams.org
    # worked example: http://edwilliams.org/avform147.htm#Example
    # convert to radians
    rho1 = convert_latlong(lat1)
    rho2 = convert_latlong(lat2)
    lam1 = convert_latlong(long1)
    lam2 = convert_latlong(long2)
    dist = 2 * math.asin(   math.sqrt((math.sin((rho1-rho2)/2))**2 + math.cos(rho1)*math.cos(rho2)*(math.sin((lam1-lam2)/2))**2))
    dist = dist*180*60/math.pi
    return dist

# my latitude and longitude for testing
mylat=38.59
mylong=-89.92


laxlat =33.57
laxlong = 118.24

#jfk = 40.38
#jfklong=73.47

#check = dist_between(laxlat, laxlong, jfk,jfklong)

def calculate_distances(lat1, long1):
    # pass the lat and long of the zip code
    # calculate distance to each weather station
    mydistances=[]
    n=len(WeatherStations)
    for i in range(n):
        lat2 = float( WeatherStations.iloc[i].lat)
        long2=float( WeatherStations.iloc[i].long)
        mydistances.append(dist_between(lat1, long1, lat2, long2))
    return mydistances

def attach_distances(thedistances):
    WeatherStations['distance']=thedistances

def sort_get_min_dist_WeatherStat():
    # sort the weather stations by distance
    # cast the type of end
    WeatherStations['end']=WeatherStations['end'].astype('int')
    datefilter = WeatherStations['end']>=2022
    FilteredStations = WeatherStations[datefilter]
    WeatherStations = WeatherStations.sort_values(by=['distance'])
    return WeatherStations[0:10]
    # find the nearest weather station by year

