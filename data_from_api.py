"""Description of the module.
    Using the list of 10 weather stations from SetUpWeather Stations, the goal is to download 365 days of weather data
     with T-MAX and T-MIN.  The list of 10 is Shortlist.csv.  The weather data is in 
    data USW00003960.csv

    Functions:
    ----------
    read_short_list()
    write_df_to_csv()
    get_temps_weatherstation()
    create_weatherdata_dictionary()
    identify_missing_data()
    id_missing_data_dict()
    check_for_complete_stations()
    the_main_function()
    Misc. variables:
    ----------------
    LOCAL
    SHORTLIST
    STATIONID - default
    YEAR - default
    MYTOKEN
    HEAD
    """
from pathlib import Path
from collections import namedtuple
import requests
import pandas as pd
import numpy as np


LOCAL = Path.cwd()
SHORTLIST = Path.cwd().joinpath('ShortList.csv')
STATIONID ="USW00013802"
YEAR="2021"
MYTOKEN = ***REMOVED***

HEAD={"token": MYTOKEN}



DayData=namedtuple('month', 'day')


def read_short_list(file_name:str = SHORTLIST)->pd.DataFrame:
    """Reads list of 10 weather station and creates a data frame.

    Args:
        file_name (pathlib.WindowsPath, optional): file name. Defaults to SHORTLIST.

    Returns:
        pd.DataFrame: Weather Station inventory data frame.
    """
    mydf=pd.read_csv(file_name)
    return mydf


def write_df_to_csv(data_frame: pd.DataFrame, name: str):
    """Writes data frame to a file named "name

    Args:
        mydataframe (pd.DataFrame): Data frame.
        name (str): The name of file. 
    """
    data_frame.to_csv(Path.cwd().joinpath(name))



def get_temps_weatherstation(theyear:str = YEAR, station:str = STATIONID)->pd.DataFrame:
    """Requests data for given year and weather station from NOAA

    Args:
        theyear (str, optional): Year for the data. Defaults to YEAR.
        station (str, optional): Weather station id. Defaults to STATIONID.

    Returns:
        pd.DataFrame: Weather data frame for the year with TMAX and TMIN
    """
    myurllist=['https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=PRCP,SNOW,TMAX,TMIN&stations=',station,'&startDate=',theyear,'-01-01&endDate=',theyear,'-12-31&format=json']
    myurl = "".join(myurllist)
    response = requests.get(myurl, headers=HEAD).json()
    #response = response.get("results")
    mydf = pd.DataFrame(response)
    return mydf



def create_weatherdata_dictionary(ws_inv: pd.DataFrame, theyear:str = "2021")->dict:
    """Returns dictionary of weather station temperature data frames
    with key values as the station.

    Args:
        ws_df (pd.DataFrame): Weather station inventory data frame
        theyear (str, optional): Year for the weather data. Defaults to "2021".

    Returns:
        dict: A dictionary of weather station temperature data for a year with 
        station id as the keys. 
    """
    local_dict = {}
    thelength = len(ws_inv)
    for i in range(thelength):
        station_name = ws_inv.name.iloc[i]
        local_df = get_temps_weatherstation(theyear, station_name)
        local_dict.update({station_name:local_df})
    return local_dict

def identify_missing_data(data_series: pd.Series)->list:
    """Returns the indices of nan values in a pandas Data Series.

    Args:
        data_series (pd.DataSeries): pd.DataSeries
    Returns:
        list: List of indices with nan values.
    """
    local_array=np.where(data_series.isnull())
    local_list=local_array[0].tolist()
    return local_list

def id_missing_data_dict(local_weather_dict: dict)->dict:
    """Creates a dictionary of missing data for each weather station.

    Args:
        local_weather_dict (dict): Dictionary of weather stations (keys) and 
        temperature data frames

    Returns:
        dict: Dictionary of weather stations (keys) and indices of missing temperature
        data. 
    """
    thekeys = list(local_weather_dict.keys())
    missing_dict = {}
    for i in thekeys:
        local_series = local_weather_dict.get(i)
        local_list = identify_missing_data(local_series.TMAX)
        missing_dict.update({i:local_list})
    return missing_dict

def check_for_complete_stations(local_missing_dict: dict)->tuple[str, int]:
    """Returns the station id with the least missing data and the number
       of missing days. 

    Args:
        local_missing_dict (): Dictionary of station ids (keys) and list of
        missing dates. 
        
    Returns:
        str: station id
        int: number of missing dates
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
        

def the_main_function():
    """Shows how pieces work together.
    """
    mydf = read_short_list()
    myweatherstations = create_weatherdata_dictionary(mydf)
    mymissingdates = id_missing_data_dict(myweatherstations)
    stationselect, num_dates_missing = check_for_complete_stations(mymissingdates)
    if num_dates_missing>0:
        raise ValueError("Missing Dates")
    write_df_to_csv(myweatherstations.get(stationselect), stationselect+".csv")