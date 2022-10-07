# Set up to select weather station
# reference package 1: https://github.com/gojiplus/get-weather-data/blob/master/zip2ws/zip2ws.py
# reference package 2: https://github.com/paulokuong/noaa

# retrieve the list of weather stations https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt

# sort the list and reduce to contain only weather stations with TMAX - TMAX List

# Get the zip code and convert to latitude and longitude using geocoder

# Compute the distance to each weather station and choose the top 5 or so, return to the GetData.