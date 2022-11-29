""" This module selects weather stations that provide TMAX data for the
    requested year from the inventory of GHCND stations. The selected
    stations are sorted by distance and the top 10 are returned.
    References:
    1: https://github.com/gojiplus/get-weather-data/blob/
        master/zip2ws/zip2ws.pyreference
    2: https://github.com/paulokuong/noaa

    Functions:
    load_weatherstation_inventory
    sort_years_weatherstat
    zip2latlong
    convert_latlong
    dist_betweenls
    calculate_distances
    attach_distances_to_inventory
    sort_get_min_dist_weatherstat
    the_main_function

    Variables:
    PATH
    LOCALFILE
    WEATHERSTATIONINVENTORY -
"""
import pathlib
from collections import namedtuple
from urllib.request import urlretrieve
import math
import pandas as pd
from geopy.geocoders import Nominatim
from dataquilt import DATA_PATH


WEATHERSTATION_INV_LOCALFILE = pathlib.Path(DATA_PATH / "ghcnd-inventory.txt")
Station = namedtuple("Station", {"name", "lat", "long", "start", "end"})


def weather_station_inv_retrieve():
    """Checks for local version of NOAA's ghcnd weather station inventory.
    If it does not exists, the function retrieves and saves inventory locally.

    Returns:
        None
    """
    WEATHERSTATIONINVENTORY_URL = (
        "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt"
    )
    urlretrieve(WEATHERSTATIONINVENTORY_URL, WEATHERSTATION_INV_LOCALFILE)


def load_weatherstation_inventory() -> list:
    """Read the weather station inventory text file into a list.

    Returns:
        list: List of NOAA weather stations with name, latitude and longitude,
        year availability.
    """
    mywslist = []
    with open(WEATHERSTATION_INV_LOCALFILE, encoding="utf8") as t_file:
        mydata = t_file.readlines()
    for xline in mydata:
        if xline.find("TMAX") != -1:
            ind = xline.find(" ")
            myst = xline[0:ind]
            newv = xline[ind:].lstrip()
            ind = newv.find(" ")
            mylat = newv[0:ind]
            newv = newv[ind:].lstrip()
            ind = newv.find(" ")
            mylong = newv[0:ind]
            newv = newv[ind:].lstrip()
            splitlist = newv.split(" ")
            mystation = Station(
                name=myst,
                lat=mylat,
                long=mylong,
                start=splitlist[1],
                end=splitlist[2].strip("\n"),
            )
            mywslist.append(mystation)
    return mywslist


def sort_years_weatherstat(
    data_frame: pd.DataFrame,
    year: int = 2021,
) -> pd.DataFrame:
    """Filters weather station inventory data frame based on year availability
    of the weather station.

    Args:
        data_frame (pd.DataFrame): Weather station inventory data frame.
        year (int, optional): Year of interest for weather data.
        Defaults to 2021.

    Returns:
        pd.DataFrame: Filtered data frame
    """
    data_frame["end"] = data_frame["end"].astype("int")
    data_frame["start"] = data_frame["start"].astype("int")
    datefilter = data_frame["end"] >= year
    data_frame = data_frame[datefilter]
    datefilter2 = data_frame["start"] <= year
    data_frame = data_frame[datefilter2]
    return data_frame


def zip2latlong(zipcodestr: str) -> tuple:
    """Returns the latitude and longitude of a US zipcode

    Args:
        zipcodestr (str): US zip code

    Returns:
        float, float: Latitude, Longitude
    """
    mygeolocator = Nominatim(user_agent="my_app")
    country = "USA"
    location = mygeolocator.geocode(str(zipcodestr) + "," + country)
    return location.latitude, location.longitude


def convert_latlong(value: float) -> float:
    """Takes a latitude or longitude value and converts the decimal part
    to radians.

    Args:
        value (): Latitude or Longitude.

    Returns:
        float: Converted value.
    """
    v2dec_part, v1int_part = math.modf(value)
    v2dec_part = v2dec_part * 100 / 60
    val = v1int_part + v2dec_part
    val = val * math.pi / 180
    return val


def dist_between(
    lat1: float,
    long1: float,
    lat2: float,
    long2: float,
) -> float:
    """Calculate the distance in nautical miles between two pairs of latitude
    and longitude

    Args:
        lat1 (float): Latitude 1.
        long1 (float): Longitude 1.
        lat2 (float): Latitude 2.
        long2 (float): Longitude 2.

    Returns:
        float: Distance in nautical miles.
    """

    rho1 = convert_latlong(lat1)
    rho2 = convert_latlong(lat2)
    lam1 = convert_latlong(long1)
    lam2 = convert_latlong(long2)
    part1 = (math.sin((rho1 - rho2) / 2)) ** 2
    part2a = math.cos(rho1) * math.cos(rho2)
    part2b = (math.sin((lam1 - lam2) / 2)) ** 2
    part2 = part2a * part2b
    dist = 2 * math.asin(math.sqrt(part1 + part2))
    dist = dist * 180 * 60 / math.pi
    return dist


def calculate_distances(
    lat1: float,
    long1: float,
    data_frame: pd.DataFrame,
) -> list:
    """Creates a list of distances based on the latitude and longitude to the
    weather stations in the weather station inventory.

    Args:
        lat1 (float): Latitude
        long1 (float): Longitude
        data_frame (pd.DataFrame): Weather station inventory dataframe

    Returns:
        list: List of distances to weather stations
    """
    mydistances = []
    thelength = len(data_frame)
    for i in range(thelength):
        lat2 = float(data_frame.iloc[i].lat)
        long2 = float(data_frame.iloc[i].long)
        mydistances.append(dist_between(lat1, long1, lat2, long2))
    return mydistances


def attach_distances_to_inventory(
    lat: float, long: float, data_frame: pd.DataFrame
) -> pd.DataFrame:
    """Attach a column of distances to weather station inventory data frame.

    Args:
        lat (float): Latitude
        long (float): Longitude
        data_frame (pd.DataFrame): Weather station inventory data frame

    Returns:
        pd.DataFrame: Weather station inventory data frame with distance column
    """
    thedistances = calculate_distances(lat, long, data_frame)
    data_frame["distance"] = thedistances
    return data_frame


def sort_get_min_dist_weatherstat(data_frame: pd.DataFrame) -> pd.DataFrame:
    """Sorts the weather station inventory data frame by ascending distance.
    Then returns 10 closest stations.

    Args:
        data_frame (pd.DataFrame): Weather station inventory with distance data
        frame.
    Returns:
        pd.DataFrame: Weather station inventory of length 10.
    """
    data_frame = data_frame.sort_values(by=["distance"])
    return data_frame[0:10]
    # find the nearest weather station by year


def the_main_function(zipcodestr: str = "62269"):
    """Runs all functions in this code.

    Args:
        zipcodestr (str, optional): US based zip code as a string.
        Defaults to "62269".
    """
    invlist = load_weatherstation_inventory()
    inv_df = pd.DataFrame(invlist)
    inv_df = sort_years_weatherstat(inv_df)
    loc_lat, loc_long = zip2latlong(zipcodestr)
    inv_df = attach_distances_to_inventory(loc_lat, loc_long, inv_df)
    shortlist = sort_get_min_dist_weatherstat(inv_df)
    shortlist.to_csv(DATA_PATH / "topten.csv")
