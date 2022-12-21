"""Description of the module.
Using the list of 10 weather stations from SetUpWeather Stations, the goal is
to download 365 days of weather data
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

import os
import requests
import pandas as pd
import numpy as np

from dataquilt import DATA_PATH


STATIONID = "USW00003960"
YEAR = "2021"
SHORTLIST = DATA_PATH / "topten.csv"

MYTOKEN = os.getenv("TOKEN")
HEAD = {"token": MYTOKEN}


def read_short_list(file_name: str = SHORTLIST) -> pd.DataFrame:
    """Reads list of 10 weather station and creates a data frame.

    Args:
        file_name (pathlib.WindowsPath, optional):
        file name. Defaults to SHORTLIST.

    Returns:
        pd.DataFrame: Weather Station inventory data frame.
    """
    mydf = pd.read_csv(file_name)
    return mydf


def get_temps_weatherstation(
    theyear: str = YEAR, station: str = STATIONID
) -> pd.DataFrame:
    """Requests data for given year and weather station from NOAA

    Args:
        theyear (str, optional): Year for the data. Defaults to YEAR.
        station (str, optional): Weather station id. Defaults to STATIONID.

    Returns:
        pd.DataFrame: Weather data frame for the year with TMAX and TMIN
    """
    myurllist = [
        "https://www.ncei.noaa.gov/access/services"
        "/data/v1?dataset=daily-summaries&"
        "dataTypes=PRCP,SNOW,TMAX,TMIN&stations=",
        station,
        "&startDate=",
        theyear,
        "-01-01&endDate=",
        theyear,
        "-12-31&format=json",
    ]
    myurl = "".join(myurllist)
    response = requests.get(myurl, headers=HEAD).json()
    # response = response.get("results")
    mydf = pd.DataFrame(response)
    return mydf


def identify_missing_data(
    data_series: pd.Series,
) -> list:
    """Returns the indices of nan values in a pandas Data Series.

    Args:
        data_series (pd.Series): pd.Series
    Returns:
        list: List of indices with nan values.
    """
    local_array = np.where(data_series.isnull())
    local_list = local_array[0].tolist()
    return local_list


def find_complete_data(
    ws_inv: pd.DataFrame,
    theyear: str = "2021",
) -> tuple[pd.DataFrame, int]:
    """Iterates through the list of nearby weather stations to
    find a complete data set. If none in the top ten, returns
    the station with the fewest missing days.

    Args:
        ws_inv (pd.DataFrame): weather station inventory
        theyear (str, optional): year of data. Defaults to "2021".

    Returns:
        pd.DataFrame: noaa data for the given year
    """
    missing_data = 366
    for i in range(len(ws_inv)):
        station_name = ws_inv.name.iloc[i]
        # print(f"station name {station_name}")
        local_df = get_temps_weatherstation(
            theyear,
            station_name,
        )
        data_check = identify_missing_data(local_df)
        # print(len(data_check))
        if len(data_check) == 0:
            return local_df, 0
        else:
            if len(data_check) < missing_data:
                missing_data = len(data_check)
                best_df = local_df
    return best_df, missing_data


def the_main_function():
    """Shows how pieces work together."""
    mydf = read_short_list()
    output = find_complete_data(mydf)
    noaa_df, num_dates_missing = output

    if num_dates_missing > 0:
        raise ValueError("Missing Dates")

    noaa_df.to_csv(DATA_PATH / "station.csv")
    return noaa_df
