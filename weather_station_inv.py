""" This module selects weather stations that provide TMAX data for the requested year 
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
            splitlist = newv.split(' ')
            mystation = Station(name=myst, lat=mylat, long=mylong, start=splitlist[1], end=splitlist[2].strip('\n'))
            mywslist.append(mystation)
    return mywslist



def write_df_to_file(data_frame, name):
    """Description of the function/method.
        Helper function to save the data frame to a local file for reuse
Parameters:
    <param>: data frame and file name

Returns:
    <variable>: Writes the data frame to a csv file
"""
    data_frame.to_csv(name)


def sort_years_weatherstat(data_frame,year=2021):
    """Description of the function/method.
    Filters the weather stations by year - returns only weather stations that are available for 
    the given year
Parameters:
    <param>: Year 
Returns:
    <variable>: Weather Station Inventory data frame
"""
    data_frame['end']=data_frame['end'].astype('int')
    data_frame['start'] = data_frame['start'].astype('int')
    datefilter =data_frame['end'] >= year 
    data_frame =data_frame[datefilter]
    datefilter2 = data_frame['start'] <= year
    data_frame = data_frame[datefilter2]
    return data_frame

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
    v2dec_part, v1int_part = math.modf(value)
    v2dec_part = v2dec_part * 100 / 60
    val = v1int_part + v2dec_part
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
    rho1 = convert_latlong(lat1)
    rho2 = convert_latlong(lat2)
    lam1 = convert_latlong(long1)
    lam2 = convert_latlong(long2)
    dist = 2 * math.asin(math.sqrt(
        (math.sin((rho1 - rho2) / 2)) ** 2 + math.cos(rho1) * math.cos(rho2) * (math.sin((lam1 - lam2) / 2)) ** 2))
    dist = dist * 180 * 60 / math.pi
    return dist


# my latitude and longitude for testing
OFLAT = 38.59
OFLONG = -89.92
LAXLAT = 33.57
LAXLONG = 118.24


def calculate_distances(lat1, long1, data_frame):
    """Description of the function/method.
    Calculates the distance between the given latitude and longitude for all weather stations in 
    the inventory.
Parameters:
    <param>: latitude and longitude (floats)
Returns:
    <variable>: Returns a list of distances
"""
    mydistances = []
    thelength = len(data_frame)
    for i in range(thelength):
        lat2 = float(data_frame.iloc[i].lat)
        long2 = float(data_frame.iloc[i].long)
        mydistances.append(dist_between(lat1, long1, lat2, long2))
    return mydistances




def attach_distances_to_inventory(lat, long, data_frame):
    """Description of the function/method.
Given a latitude and longitude, it calls the function to compute the 
list of distances between the given and each weather station. This is attached
to the weather station inventory.
Parameters:
    <param>: Latitude and longitude of a location.

Returns:
    <variable>: Distances attached to the weather station inventory.
"""
    thedistances = calculate_distances(lat, long, data_frame)
    data_frame['distance'] = thedistances
    return data_frame



def sort_get_min_dist_weatherstat(data_frame):
    """Description of the function/method.
    Sorts the weather station data frame by distance and returns 
    the top 10 closest weather stations.
Parameters:
    <param>: none

Returns:
    <variable>:  Data frame of 10 weather stations
"""
    data_frame =data_frame.sort_values(by=['distance'])
    return data_frame[0:10]
    # find the nearest weather station by year


def themainfunction(zipcodestr="62269"):
    """Description of the function/method.
    Gets the weather station inventory, sorts inventory by year,
    adds distance data and returns the top 10 closest 
    weather stations as a dataframe. 
Parameters:
    <param>: Description of the parameter

Returns:
    <variable>: Description of the return value
"""
    invlist = load_weatherstation_inventory()
    inv_df = pd.DataFrame(invlist) 
    inv_df = sort_years_weatherstat(inv_df)
    loc_lat, loc_long = zip2latlong(zipcodestr)
    inv_df = attach_distances_to_inventory(loc_lat, loc_long,inv_df)
    shortlist=sort_get_min_dist_weatherstat(inv_df) 
    write_df_to_file(shortlist, "topten.csv") 