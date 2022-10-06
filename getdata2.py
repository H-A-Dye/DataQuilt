# create a def to download the data from NOAA
import pandas as pd
import requests
import os
import datetime

### I will need to convert zip code to lat and long. Then find the nearest stations that have t-max and t-min.  Then I will need to download
## the data.  Some experimentation indicated that not all zip codes work.

WORKINGDir = os.getcwd()
temperaturefile = os.path.join(WORKINGDir,'temperature.txt')
tempcsv = os.path.join(WORKINGDir,'temps.csv')

URLFORSTATIONS = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt"
URLINVENTORY = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt"

ZIP = "28801"
YEAR="2020"
myurl ='https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&locationid=ZIP:52079&startdate=2010-05-01&enddate=2010-05-30&limit=750'
mytoken = ***REMOVED***
head={"token": mytoken}

myurlv2='https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&stationid=GHCND:USC00237465&startdate=2010-05-01&enddate=2010-05-30&limit=10' '

myurllist= [
    'https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&locationid=ZIP:',
    ZIP, '&startdate=',YEAR,'-01-01&enddate=', YEAR,'-12-31&limit=50']




DayData=namedtuple('month', 'day')

mydict = dict()

def get_temps_p(zipco =ZIP, theyear =YEAR):
    # implement with zipcode and year options
    myurl = ['https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&locationid=ZIP:',ZIP,'&startdate=',YEAR,'-01-01&enddate=',YEAR,'-12-31&limit=50']
    myurl ="".join(myurl)
    response=requests.get(myurl,headers =head)
    return(response)

# putting in a these as helper functions. there was a definite pause when
# i requested the data, so having data stored to work with as I build the rest of the program will be helpful.

def get_temps_file():
    # get temp data from file
    with open(temperaturefile) as text_file:
        data=text_file.read()


def write_temps_file(data):
    # write temp data to a file
    with open(temperaturefile,'a') as text_file:
        print(data,file = text_file)


def get_temps():
    response= requests.get(myurl,headers=head).json()
    response = response.get("results")
    return response


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


def place_into_dict(DayData daydata, tempinfo):
    if mydict.get(daydata) is None:
        mydict.update({daydata:tempinfo})
    else:


def to_data_frame(data):
    # pass the list of dictionary records from get_temps
    tst = pd.DataFrame.from_records(data)
    return tst

def place_data_into_df():
    pass