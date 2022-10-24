"""Description of the module.
    Using the list of 10 weather stations from SetUpWeather Stations, the goal is to download 365 days of weather data
 with T-MAX and T-MIN.  The list of 10 is Shortlist.csv.  The weather data is in 
 data USW00003960.csv
Classes:
    <class>

Functions:
    <function>

Misc. variables:
    <variable>
"""
from pathlib import Path
from collections import namedtuple
import requests
import pandas as pd
import numpy as np


LOCAL = Path.cwd()
TEMPERATUREFILE = Path.cwd().joinpath('temperature.txt')
SHORTLIST = Path.cwd().joinpath('ShortList.csv')
URLINVENTORY = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt"


STATIONID ="USW00013802"
YEAR="2021"
MYTOKEN = "vgMXMUXAOFMvAecQhqyKdZzwBojmbUeb"

head={"token": MYTOKEN}



DayData=namedtuple('month', 'day')


def read_short_list(file_name = SHORTLIST):
    """Description of the function/method.
            Reads the Shortlist.csv function created by the Get Weather Station module
Parameters:
    <param>: Reads data frame of weather stations

Returns:
    <variable>: returns a data frame
"""
    mydf=pd.read_csv(file_name)
    return mydf


def write_df_to_csv(mydataframe, name):
    """Description of the function/method.
   Helper function to store weather data
Parameters:
    <param>: data frame and file name

Returns:  
    <variable>: 
"""
    mydataframe.to_csv(Path.cwd().joinpath(name))



def get_temps_weatherstation_revised(theyear = YEAR, station = STATIONID):
    """Description of the function/method.
    Given the year and station as strings, requests data from noaa.
    https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation
    Temperature conversion: Divide your results by 10, multiply by 9/5 + 32 to convert to F (or whatever you need to do).
Parameters:
    <param>: Year and station id (strings)

Returns:
    <variable>: Returns a data frame of dates and weather information.
"""
    myurllist=['https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=PRCP,SNOW,TMAX,TMIN&stations=',station,'&startDate=',theyear,'-01-01&endDate=',theyear,'-12-31&format=json']
    myurl = "".join(myurllist)
    response = requests.get(myurl, headers=head).json()
    #response = response.get("results")
    mydf = pd.DataFrame(response)
    return mydf



def create_weatherdata_dictionary(ws_list, theyear = "2021"):
    """Description of the function/method.
    Create a dictionary of  weather data frames from the short list of weather stations 
    data frame
Parameters:
    <param>: Data frame of Weather Stations and year

Returns:
    <variable>: Dictionary of Weather Data Frames
"""
    local_dict = {}
    thelength = len(ws_list)
    for i in range(thelength):
        station_name = ws_list.name.iloc[i]
        local_df = get_temps_weatherstation_revised(theyear, station_name)
        local_dict.update({station_name:local_df})
    return local_dict

def identify_missing_data(data_series):
    """Description of the function/method.
    Given a weather data series identify the missing data
Parameters:
    <param>: Description of the parameter
    Weather Data Frame
Returns:
    <variable>: Description of the return value
    List of missing values for temperature
"""
    local_array=np.where(data_series.isnull())
    local_list=local_array[0].tolist()
    return local_list

def id_missing_data_dict(local_weather_dict):
    """Description of the function/method.
    Identify all the missing data in a weather data frame
Parameters:
    <param>: Description of the parameter
    dictionary of weather data frames
Returns:
    <variable>: Description of the return value
    dictionary of missing indices for each data frame
"""
    thekeys = list(local_weather_dict.keys())
    missing_dict = {}
    for i in thekeys:
        local_series = local_weather_dict.get(i)
        local_list = identify_missing_data(local_series.TMAX)
        missing_dict.update({i:local_list})
    return missing_dict

def check_for_complete_stations(local_missing_dict):
    """Description of the function/method.
    Find the weather data frame with the fewest missing values
Parameters:
    <param>: Dictionary of stations with lists of missing values
Returns:
    <variable>: Returns name of station with minimum missing vales and the number of missing values
"""
    thekeys = list(local_missing_dict.keys())
    minnumber=366
    for i in thekeys:
        local_list = local_missing_dict.get(i)
        if len(local_list)<minnumber:
            minnumber=len(local_list)
            minstation = i
        if len(local_list)==0:
            minnumber=0
            minstation =i
            return minstation, minnumber
    return minstation, minnumber
        

def themainfunction():
    """Description of the function/method.
    Puts all the commands in this section together and 
    saves a weather data frame as a csv. 
Parameters:
    <param>: Description of the parameter
    None
Returns:
    <variable>: Description of the return value
"""
    mydf = read_short_list()
    myweatherstations = create_weatherdata_dictionary(mydf)
    mymissingdates = id_missing_data_dict(myweatherstations)
    stationselect, num_dates_missing = check_for_complete_stations(mymissingdates)
    write_df_to_csv(myweatherstations.get(stationselect), stationselect+".csv")