""" 
This module selects weather stations that provide TMAX data for the requested year 
from the inventory of GHCND stations. The selected stations are sorted by 
distance and the top 10 are returned.
References:
    1: https://github.com/gojiplus/get-weather-data/blob/master/zip2ws/zip2ws.pyreference
    2: https://github.com/paulokuong/noaa
"""
import pathlib
from collections import namedtuple
from urllib.request import urlretrieve
import math
import pandas as pd
from geopy.geocoders import Nominatim

PATH = pathlib.Path().absolute()
LOCALFILE = pathlib.Path().absolute().joinpath('ghcnd-inventory.txt')

WEATHERSTATIONINVENTORY = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt'
urlretrieve(WEATHERSTATIONINVENTORY, LOCALFILE)

WEATHERSTATIONINVENTORY = LOCALFILE

Station = namedtuple("Station", {'name', 'lat', 'long', 'start', 'end'})


def load_weatherstation_inventory():
    """Description of the function/method.
    This loads the gchnd inventory of weather stations into a list
Parameters:
    <param>: none, loads local file
Returns:
    <variable>: Returns a list of named tuples of weather stations
"""
    mywslist = []
    with open(LOCALFILE, encoding='utf8') as t_file:
        mydata = t_file.readlines()
    for xline in mydata:
        if xline.find('TMAX') != -1:
            ind = xline.find(' ')
            myst = xline[0:ind]
            newv = xline[ind:].lstrip()
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


def data_into_df(list_data):
    """Description of the function/method.
        Helper function to load the list of data into a dataframe
Parameters:
    <param>: list of data

Returns:
    <variable>: returns a dataframe of the data
"""
    mydf = pd.DataFrame(list_data)
    return mydf


weatherstations_df =data_into_df(load_weatherstation_inventory())


def write_df_to_file(df, name):
    """Description of the function/method.
        Helper function to save the data frame to a local file for reuse
Parameters:
    <param>: data frame and file name

Returns:
    <variable>: Writes the data frame to a csv file
"""
    df.to_csv(name)



def zip2latlong(zipcode):
    """Description of the function/method.
    Returns latitude and longitude based on the function
Parameters:
    <param>: US based zipcode

Returns:
    <variable>: latitude and longitude
"""
    mygeolocator = Nominatim(user_agent="my_app")
    country = 'USA'
    location = mygeolocator.geocode(str(zipcode) + ',' + country)
    return location.latitude, location.longitude


def convert_latlong(value):
    """Description of the function/method.
        Converts latitude or longitude measurement to radians
    Parameters:
    <param>: latitude or longitude float

    Returns: <variable>: returns latitude or longitude in radians
    """
    v2, v1 = math.modf(value)
    v2 = v2 * 100 / 60
    val = v1 + v2
    val = val * math.pi / 180
    return val


def dist_between(lat1, long1, lat2, long2):
    """Description of the function/method.
    Computes the distance between two latitudes and longitudes
    d=2*asin(sqrt((sin((lat1-lat2)/2))^2 +
                      cos(lat1)*cos(lat2)*(sin((lon1-lon2)/2))^2))  from edwilliams.org
     worked example: http://edwilliams.org/avform147.htm#Example
    convert to radians    
Parameters:
    <param>: Two sets of latitude and longitude

Returns:
    <variable>: Distance in nautical miles
"""
    """  """
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
    """Description of the function/method.
    Calculates the distance between the given latitude and longitude for all weather stations in 
    the inventory
Parameters:
    <param>: latitude and longitude (floats)
Returns:
    <variable>: Returns a list of distances
"""
    mydistances = []
    n = len(WeatherStations_df)
    for i in range(n):
        lat2 = float(WeatherStations_df.iloc[i].lat)
        long2 = float(WeatherStations_df.iloc[i].long)
        mydistances.append(dist_between(lat1, long1, lat2, long2))
    return mydistances


def attach_distances_to_inventory(lat, long):
    """Description of the function/method.
Given a latitude and longitude, it calls the function to compute the 
list of distances between the given and each weather station. This is attached
to the weather station inventory.
Parameters:
    <param>: Latitude and longitude of a location.

Returns:
    <variable>: Distances attached to the weather station inventory.
"""
    thedistances = calculate_distances(lat, long)
    WeatherStations_df['distance'] = thedistances

def sort_years_weatherstat(year=2022):
    """Description of the function/method.
    Filters the weather stations by year - returns only weather stations that are available for 
    the given year
Parameters:
    <param>: Year 

Returns:
    <variable>: Weather Station Inventory data frame
"""
    
    WeatherStations_df['end'] = WeatherStations_df['end'].astype('int')
    datefilter = WeatherStations_df['end'] >= year and WeatherStations_df['start']<=year
    WeatherStations_df = WeatherStations_df[datefilter]


def sort_get_min_dist_weatherstat():
    """Description of the function/method.
    Sorts the weather station data frame by distance and returns 
    the top 10 closest weather stations.
Parameters:
    <param>: none

Returns:
    <variable>:  Data frame of 10 weather stations
"""
    WeatherStations_df = WeatherStations_df.sort_values(by=['distance'])
    return WeatherStations_df[0:10]
    # find the nearest weather station by year
