""" Using the list of 10 weather stations from SetUpWeather Stations, the goal is to download 365 days of weather data
 with T-MAX and T-MIN.  This file is a hot mess. I need to sit down and sequence the events.
"""

# create a def to download the data from NOAA
import pandas as pd
import requests
#import os
from pathlib import Path
from collections import namedtuple
import datetime

###  Need to convert this to PathLib and load in the short list
LOCAL = Path.cwd()
TEMPERATUREFILE = Path.cwd().joinpath('temperature.txt')
SHORTLIST = Path.cwd().joinpath('ShortList.csv')

URLFORSTATIONS = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt"
URLINVENTORY = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt"


# Clean this area up -  token, URL BITs, with spots for Station and YEAR
STATIONID ="USW00013802"
YEAR="2020"
ZIP="22801"
MYTOKEN = ***REMOVED***

head={"token": MYTOKEN}

#SAMPLESTATIONURL='https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&stationid=GHCND:USC00237465&startdate=2010-05-01&enddate=2010-05-30&limit=10' '

MYURLLIST= [
    'https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&stationid=GHCND:',STATIONID, '&startdate=',YEAR,'-01-01&enddate=', YEAR,'-12-31&limit=50']




DayData=namedtuple('month', 'day')

mydict = dict()

def read_short_list():
    """ get the station IDS"""
    mydf=pd.read_csv(SHORTLIST)
    return mydf


def get_temps_weatherstation(station =STATIONID, theyear=YEAR):
    """ request data from NOAA and return the response"""
    myurllist = [
    'https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&stationid=GHCND:',station,'&startdate=',theyear,'-01-01&enddate=', theyear,'-02-31&limit=400']
    myurl="".join(myurllist)
    response = requests.get(myurl, headers=head)
    response= requests.get(myurl,headers=head).json()
    response = response.get("results")
    mydf = pd.DataFrame(response)
    return mydf

def get_temps_weatherstation_revised(theyear = YEAR, station = STATIONID):
    myurllist=['https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=PRCP,SNOW,TMAX,TMIN&stations=',station,'&startDate=',theyear,'-01-01&endDate=',theyear,'-12-31&format=json']
    myurl = "".join(myurllist)
    response = requests.get(myurl, headers=head)
    response = requests.get(myurl, headers=head).json()
    #response = response.get("results")
    mydf = pd.DataFrame(response)
    return mydf



def write_df_to_csv(mydataframe, name):
    """ Helper function to store data """
    mydataframe.to_csv(Path.cwd().joinpath(name))

# https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation
# Divide your results by 10, multiply by 9/5 + 32 to convert to F (or whatever you need to do).

def get_temps_flex(startdate,edate,station=STATIONID,):
    # implement with zipcode and year options
    myurllist = [
        'https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMAX&limit=1000&stationid=GHCND:',
        station, '&startdate=', startdate ,'&enddate=', edate]
    myurl = "".join(myurllist)
    response=requests.get(myurl,headers =head)
    return(response)

def get_temps_flex2(startdate,station=STATIONID,):
    # implement with zipcode and year options
    myurllist = [
        'https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&stationid=GHCND:',
        station, '&startdate=', startdate ,'&limit=400']
    myurl = "".join(myurllist)

    response=requests.get(myurl,headers =head)
    return(response)



# putting in a these as helper functions. there was a definite pause when
# i requested the data, so having data stored to work with as I build the rest of the program will be helpful.

def get_temps_file():
    """ helper function to get temperature data from a file; need to change parameters """
    with open(temperaturefile) as text_file:
        data=text_file.read()


def write_temps_file(data):
    # write temp data to a file
    with open(temperaturefile,'a') as text_file:
        print(data,file = text_file)




def extract_data(x):
    # get date, Tmax, Tmin from an individual entry
    mydate = x.get('date')[0:10]
    # date has empty time data attached
    mytype = x.get('datatype')
    myvalue = x.get('value')
    mydate = datetime.datetime.strptime(mydate, "%Y-%m-%d")
    mym = mydate.month
    myd = mydate.day
    return DayData(mym, myd), {mytype, myvalue}


def place_into_dict(daydata, tempinfo):
    if mydict.get(daydata) is None:
        mydict.update({daydata:tempinfo})



def to_data_frame(data):
    # pass the list of dictionary records from get_temps
    tst = pd.DataFrame.from_records(data)
    return tst
