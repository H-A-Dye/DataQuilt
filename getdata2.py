# create a def to download the data from NOAA
import requests

myurl ='https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&locationid=ZIP:28801&startdate=2010-05-01&enddate=2010-05-30&limit=366'
mytoken = ***REMOVED***
head={"token": mytoken}
#response = requests.get(myurl, headers=head)
#response = response.json()
#theresults=response.get("results")
mydict = dict()

def get_temps_p(zipco, theyear):
    # implement with zipcode and year options
    pass

def get_temps():
    response= requests.get(myurl,headers=head).json()
    thedata = response.get('results')
    return thedata


def extract_data(x):
    # get date, Tmax, Tmin
    mydate = x.get('date')
    mytype = x.get('datatype')
    myvalue = x.get('value')
    return mydate, mytype, myvalue


def place_into_dict():
    # place