""" This module takes a weather data frame and creates a diagram
    of a temperature quilt.
    Classes:
    None

    Functions:
    extract_data
    create_weather_dict
    grade_temp
    make_color
    add_month_to_image
    the_main
    Misc. variables:
    COMMONDAYS - number of days in each month in a common year
    COLORBASE - RGB value
    STEP - Step of RGB values
    MYDATA - pandas data frame
    """
import datetime
from collections import namedtuple, Counter

import pandas as pd
from PIL import Image, ImageDraw

from dataquilt.colors_kona import make_color_kona, COLORENNUMERATE
from dataquilt import DATA_PATH


DayData = namedtuple("DayData", "month,day")
TempData = namedtuple("TempData", "low_temperature,high_temperature")


MYDATA = pd.read_csv(DATA_PATH / "USW00003960.csv")


COMMONDAYS = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}
COLORBASE = (0, 0, 256)
STEP = 256 // 15


def create_temp_level_df(noaa_data: pd.DataFrame = MYDATA) -> pd.DataFrame:
    """Create a weather data frame for maximum daily temperatures,
    coded as levels. The level 15 represents a null value corresponding
    to the color white.

    Args:
        noaa_data (pd.DataFrame): Data frame from raw noaa data

    Returns:
        pd.DataFrame: a 31 x 12 data frame with integer values.
    """
    my_dates = noaa_data.DATE
    the_datetimes = my_dates.apply(
        lambda x: datetime.datetime.strptime(
            x,
            "%Y-%m-%d",
        )
    )
    the_months = the_datetimes.apply(lambda x: x.month)
    the_days = the_datetimes.apply(lambda x: x.day)
    noaa_data = noaa_data.assign(days=the_days)
    noaa_data = noaa_data.assign(months=the_months)
    my_levels = noaa_data.TMAX.apply(
        lambda x: grade_temp(
            noaa_data,
            int(x),
        )
    )
    noaa_data = noaa_data.assign(levels=my_levels)
    my_small = noaa_data[["months", "days", "levels"]]
    my_reshape = my_small.pivot(
        index="days",
        columns="months",
        values="levels",
    )
    my_reshape = my_reshape.fillna(15.0)
    return my_reshape


def extract_data(x_entry: pd.Series) -> tuple[DayData, TempData]:
    """Extracts TMIN and TMAX values from a row of a data
        frame and the date in month, day format.

    Args:
        x_entry (pd.Series): Row from the weather data frame

    Returns:
        tuple[DayData, TempData]: [(month,day), (TMIN, TMAX)]
    """
    mydate = x_entry.DATE
    mydate = datetime.datetime.strptime(mydate, "%Y-%m-%d")
    mym = mydate.month
    myd = mydate.day
    x_tmin = x_entry.TMIN
    x_tmax = x_entry.TMAX
    thedate = DayData(mym, myd)
    thetemp = TempData(x_tmin, x_tmax)

    return thedate, thetemp


def create_weather_dict(weather_data: pd.DataFrame) -> dict:
    """Creates a dictionary from the pandas Data frame with DayData as
    the key and TempData as the value

    Args:
        weather_data (pandas.DataFrame): weather data

    Returns:
        dict: DayData as keys, TempData as values
    """
    local_dict = {}
    thelength = len(weather_data)
    for i in range(thelength):
        day_info, temp_info = extract_data(weather_data.loc[i])
        if local_dict.get(day_info) is None:
            local_dict.update({day_info: temp_info})
    return local_dict


def grade_temp(
    weather_data: pd.DataFrame,
    temperature: int,
) -> int:
    """Takes a temperature value and returns a color level
    integer.

    Args:
        temperature (int): temperature

    Returns:
        int: color level
    """
    weather_data.TMAX = pd.to_numeric(weather_data.TMAX, downcast="integer")
    weather_data.TMIN = pd.to_numeric(weather_data.TMIN, downcast="integer")
    temperature_range_max = max(weather_data.TMAX) - min(weather_data.TMAX)
    temperature_min = min(weather_data.TMAX)
    temperature_bin_size = temperature_range_max // 15 + 1
    temperature = temperature - temperature_min
    color = temperature // temperature_bin_size
    if color > 14:
        raise ValueError
    return color


def make_color(local_level: int) -> tuple:
    """Generates a RGB color based on integer. This should get replaced
    with swatch.

    Args:
        local_level (int): color level

    Returns:
        tuple: RGB value
    """
    color_r = 0 + local_level * STEP
    color_g = 255 - local_level * 10
    color_b = 256 - local_level * 5
    colorrgb = (color_r, color_g, color_b)
    return colorrgb


def create_month_list(
    weather_data: pd.DataFrame,
    weather_dict: dict,
    month_number: int,
) -> list[int]:
    """Creates a list with a month of quilt data

    Args:
        weather_data (pd.DataFrame): data frame from NOAA data
        weather_dict (dict): key: DayData, values: TempData
        month_number (int, optional): Number of the month Defaults to 1(JAN).
    """
    days = COMMONDAYS.get(month_number)
    if len(weather_dict) == 366 and month_number == 2:
        days = days + 1
    level_list = []
    for i in range(days):
        dict_entry = weather_dict.get(DayData(month_number, i + 1))
        high_temp = int(dict_entry.high_temperature)
        level = grade_temp(weather_data, high_temp)
        level_list.append(level)
    if len(level_list) < 31:
        for i in range(31 - len(level_list)):
            level_list.append(0)
    return level_list


def create_level_dataframe(weather_data: pd.DataFrame) -> pd.DataFrame:
    """Creates a data frame of level data for entire year

    Args:
        weather_data (pd.DataFrame): _description_
        weather_dict (dict): _description_

        month_number (int, optional): _description_. Defaults to 1.

    Returns:
        pd.DataFrame: _description_
    """
    local_dict = create_weather_dict(weather_data)
    local_df = pd.DataFrame()
    for i in range(12):
        local_df[str(i + 1)] = create_month_list(
            weather_data,
            local_dict,
            i + 1,
        )
    return local_df


def create_piece_counter(level_df: pd.DataFrame) -> Counter:
    """Flatten and count all elements in level dataframe

    Args:
        level_df (pd.DataFrame): table of levels

    Returns:
        Counter: piece count
    """
    flat_list = level_df.to_numpy().flatten()
    counts = Counter(flat_list)
    count_df = pd.DataFrame.from_dict(
        counts,
        orient="index",
        columns=["Count"],
    )
    # Remove at end of changes
    if len(count_df) < 16:
        count_df.loc[15] = [0]
    color_names = []
    color_code = []
    for key in COLORENNUMERATE:
        color_code.append(key)
        color_names.append(COLORENNUMERATE[key])
    count_df = count_df.sort_index()
    count_df = count_df.assign(code=color_code)
    count_df = count_df.assign(color=color_names)
    return count_df


def add_month_to_image_v2(
    temp_data: pd.DataFrame,
    drawobject: ImageDraw.ImageDraw,
    month_number: int = 1,
):
    """Adds a month of data to the quilt Image

    Args:
        weather_data (pd.dataFrame)
        weather_dict (dict): _description_
        drawobject (PIL.ImageDraw.ImageDraw): _description_
        month_number (int, optional): _description_. Defaults to 1.
    """
    for i in range(31):
        x_1 = month_number * 20
        x_2 = x_1 + 10
        y_1 = 30 + i * 10
        y_2 = y_1 + 10
        level = temp_data.iloc[i, month_number - 1]
        if level < 0 or level > 15:
            raise KeyError(f"{level}")
        color_tuple = make_color_kona(level)
        if level is None:
            raise KeyError("No Level")
            level = 1
        drawobject.rectangle([x_1, y_1, x_2, y_2], fill=color_tuple, outline=1)


def add_month_to_image(
    weather_data: pd.DataFrame,
    weather_dict: dict,
    drawobject: ImageDraw.ImageDraw,
    month_number: int = 1,
):
    """Adds a month of data to the quilt Image

    Args:
        weather_data (pd.dataFrame)
        weather_dict (dict): _description_
        drawobject (PIL.ImageDraw.ImageDraw): _description_
        month_number (int, optional): _description_. Defaults to 1.
    """
    days = COMMONDAYS.get(month_number)
    if len(weather_dict) == 366 and month_number == 2:
        days = days + 1
    for i in range(days):
        x_1 = month_number * 20
        x_2 = x_1 + 10
        y_1 = 30 + i * 10
        y_2 = y_1 + 10
        dict_entry = weather_dict.get(DayData(month_number, i + 1))
        high_temp = int(dict_entry.high_temperature)
        level = grade_temp(weather_data, high_temp)
        if level < 0 or level > 14:
            raise KeyError(f"{level}")
        color_tuple = make_color_kona(level)
        if level is None:
            print("uh oh")
            level = 1
        drawobject.rectangle([x_1, y_1, x_2, y_2], fill=color_tuple, outline=1)


def construct_image(weather_data: pd.DataFrame) -> Image:
    """Construct the image from the weather_data

    Args:
        weather_data (pd.DataFrame): a year of data from a weather station

    Returns:
        Image: data quilt image
    """
    weather_dict = create_weather_dict(weather_data)
    local_im = Image.new(mode="RGB", size=(270, 370), color=(256, 256, 256))
    draw = ImageDraw.Draw(local_im)
    draw.line([0, 30, 270, 30], fill=1, width=1)
    draw.line([0, 340, 270, 340], fill=1, width=1)
    for i in range(12):
        add_month_to_image(weather_data, weather_dict, draw, i + 1)
    return local_im


def construct_image_v2(temp_data: pd.DataFrame) -> Image:
    """Construct the image from the weather_data

    Args:
        temp_data (pd.DataFrame): temperature level data
        from create_temp_level_df

    Returns:
        Image: data quilt image
    """
    local_im = Image.new(mode="RGB", size=(270, 370), color=(256, 256, 256))
    draw = ImageDraw.Draw(local_im)
    draw.line([0, 30, 270, 30], fill=1, width=1)
    draw.line([0, 340, 270, 340], fill=1, width=1)
    for i in range(12):
        add_month_to_image_v2(temp_data, draw, i + 1)
    return local_im


def the_main():
    """Creates the weather dictionary and then uses add_month_to_image to
    draw an image of the quilt.
    """
    weather_dict = create_weather_dict(MYDATA)
    local_im = Image.new(mode="RGB", size=(270, 370), color=(256, 256, 256))
    draw = ImageDraw.Draw(local_im)
    draw.line([0, 30, 270, 30], fill=1, width=1)
    draw.line([0, 340, 270, 340], fill=1, width=1)
    for i in range(12):
        add_month_to_image(MYDATA, weather_dict, draw, i + 1)
    local_im.show()


if __name__ == "__main__":
    the_main()
