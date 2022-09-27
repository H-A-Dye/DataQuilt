import os
from urllib.request import urlretrieve

tmp = os.getenv
mylocal = os.getcwd()
myfile = mylocal + "\\weatherdat.csv"
mypractice = "https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-marine&dataTypes=WIND_DIR,WIND_SPEED&stations=AUCE&startDate=2016-01-01&endDate=2016-01-02&boundingBox=90,-180,-90,180"

mystartd = '2019-01-01'
myendd = '2019-12-31'

# https://www.ncdc.noaa.gov/cdo-web/webservices/v2#datasets

#documentation
def get_my_data():
    urlretrieve(mypractice, myfile)
# attempt 1: https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation

part1 = "https://www.ncei.noaa.gov/access/services/data/v1?dataset="
#p2 dataset name

#p3 datatypes

#p4 stationname

#p5 startdate
#p6 enddate


## attempt 2 based on

# https://www.ncdc.noaa.gov/cdo-web/token

mytoken = "vgMXMUXAOFMvAecQhqyKdZzwBojmbUeb"

mybaseurl = "https://www.ncei.noaa.gov/cdo-web/api/v2/{endpoint}"
