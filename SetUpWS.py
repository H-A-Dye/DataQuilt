""" This module selects weather stations that provide TMAX data for the requested year from the inventory of
GHCND stations. The selected stations are sorted by distance and the top 10 are returned
reference package 1: https://github.com/gojiplus/get-weather-data/blob/master/zip2ws/zip2ws.pyreference
package 2: https://github.com/paulokuong/noaa"""
import pathlib
from collections import namedtuple
import math
import pandas as pd
from urllib.request import urlretrieve
from geopy.geocoders import Nominatim

PATH = pathlib.Path().absolute()
LOCALFILE = pathlib.Path().absolute().joinpath('ghcnd-inventory.txt')

WeatherStation = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt'
urlretrieve(WeatherStation, LOCALFILE)

WeatherStation = LOCALFILE

Station = namedtuple("Station", {'name', 'lat', 'long', 'start', 'end'})


def filter_ws():
    """Loads the weather station inventory file and places each station as a named tuple into
        a list"""
    mywslist = []
    with open(LOCALFILE, encoding='utf8') as t_file:
        mydata = t_file.readlines()
    for x in mydata:
        if x.find('TMAX') != -1:
            ind = x.find(' ')
            myst = x[0:ind]
            newv = x[ind:].lstrip()
            ind = newv.find(' ')
            mylat = newv[0:ind]
            newv = newv[ind:].lstrip()
            ind = newv.find(' ')
            mylong = newv[0:ind]
            newv = newv[ind:].lstrip()
            s = newv.split(' ')

            mystation = Station(name=myst, lat=mylat, long=mylong, start=s[1], end=s[2].strip('\n'))
            mywslist.append(mystation)
    return mywslist


def data_into_df(data):
    """ load list of stations into a data frame
    :param data: list of
    :return: 
    """
    mydf = pd.DataFrame(data)
    return mydf


WeatherStations_df = data_into_df(filter_ws())


def write_df_to_file(df, name):
    # write to file
    df.to_csv(name)


# Get the zip code and convert to latitude and longitude using geocoder

# try1 using pygeocoder - this does not work.
def zip2latlong(zipcode):
    """
    positive lat is north, positive long is east
    attempt1: pygeocoder and switched to geopy's nominatim
    """
    geolocator = Nominatim(user_agent="my_app")
    country = 'USA'
    location = geolocator.geocode(str(zipcode) + ',' + country)
    return location.latitude, location.longitude


def convert_latlong(value):
    """Converts latitude or longitude value to radians"""
    v2, v1 = math.modf(value)
    v2 = v2 * 100 / 60
    val = v1 + v2
    val = val * math.pi / 180
    return val


def dist_between(lat1, long1, lat2, long2):
    """ d=2*asin(sqrt((sin((lat1-lat2)/2))^2 +
                      cos(lat1)*cos(lat2)*(sin((lon1-lon2)/2))^2))  from edwilliams.org
     worked example: http://edwilliams.org/avform147.htm#Example
    convert to radians """
    rho1 = convert_latlong(lat1)
    rho2 = convert_latlong(lat2)
    lam1 = convert_latlong(long1)
    lam2 = convert_latlong(long2)
    dist = 2 * math.asin(math.sqrt(
        (math.sin((rho1 - rho2) / 2)) ** 2 + math.cos(rho1) * math.cos(rho2) * (math.sin((lam1 - lam2) / 2)) ** 2))
    dist = dist * 180 * 60 / math.pi
    return dist


# my latitude and longitude for testing
mylat = 38.59
mylong = -89.92

laxlat = 33.57
laxlong = 118.24


def calculate_distances(lat1, long1):
    # pass the lat and long of the zip code
    # calculate distance to each weather station
    mydistances = []
    n = len(WeatherStations_df)
    for i in range(n):
        lat2 = float(WeatherStations_df.iloc[i].lat)
        long2 = float(WeatherStations_df.iloc[i].long)
        mydistances.append(dist_between(lat1, long1, lat2, long2))
    return mydistances


def attach_distances(lat, long):
    thedistances = calculate_distances(lat, long)
    WeatherStations_df['distance'] = thedistances


def sort_get_min_dist_weatherstat():
    """  sort the weather stations by TMAX and distance
    :return:
    """
    WeatherStations_df['end'] = WeatherStations_df['end'].astype('int')
    datefilter = WeatherStations_df['end'] >= 2022
    filteredstations = WeatherStations_df[datefilter]
    filteredstations = filteredstations.sort_values(by=['distance'])
    return filteredstations[0:10]
    # find the nearest weather station by year
