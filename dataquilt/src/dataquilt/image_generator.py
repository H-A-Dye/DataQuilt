""" This module takes a weather data frame and creates a diagram
    of a temperature quilt.
    Classes:
    None

    Functions:
    grade_temp
    make_kona_color
    add_month_to_image
    the_main
    Misc. variables:
    COMMONDAYS - number of days in each month in a common year
    COLORBASE - RGB value
    STEP - Step of RGB values
    MYDATA - pandas data frame
    """
import datetime
from collections import Counter

import pandas as pd
from PIL import Image, ImageDraw

from dataquilt.colors_kona import make_color_kona, COLORENNUMERATE
from dataquilt import DATA_PATH


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
    datetimes = my_dates.apply(
        lambda x: datetime.datetime.strptime(
            x,
            "%Y-%m-%d",
        )
    )
    months = datetimes.apply(lambda x: x.month)
    days = datetimes.apply(lambda x: x.day)
    noaa_data = noaa_data.assign(days=days)
    noaa_data = noaa_data.assign(months=months)
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


def create_piece_counter(
    level_df: pd.DataFrame,
    binlist: list,
) -> Counter:
    """Flatten and count all elements in level dataframe

    Args:
        level_df (pd.DataFrame): table of levels

    Returns:
        Counter: piece count
    """
    flat_list = level_df.to_numpy().flatten()
    counts = Counter(flat_list)
    # Remove at end of changes
    count_df = pd.DataFrame()
    color_names = []
    color_code = []
    square_counts = []
    for key in COLORENNUMERATE:
        color_code.append(key)
        color_names.append(COLORENNUMERATE[key])
        squares = counts[key]
        if not squares:
            squares = 0
        square_counts.append(squares)
    count_df["code"] = color_code
    count_df["color"] = color_names
    count_df["count"] = square_counts
    count_df["Celsius"] = binlist
    fahrenheit = []
    for i in range(15):
        number = round(int(binlist[i]) * 9 / 5 + 32, 1)
        fahrenheit.append(number)
    fahrenheit.append("NA")
    count_df["Fahrenheit"] = fahrenheit
    return count_df


def create_bin_list(noaa_df: pd.DataFrame) -> list:
    """Create a list of temperature ranges for the
    piece counter
    Args:
        noaa_df (pd.DataFrame): noaa dataframe
    Returns:
        list: Maximum temperature for each color code
    """
    noaa_df.TMAX = pd.to_numeric(noaa_df.TMAX, downcast="integer")
    noaa_df.TMIN = pd.to_numeric(noaa_df.TMIN, downcast="integer")
    temperature_range_max = max(noaa_df.TMAX) - min(noaa_df.TMAX)
    temperature_bound = round(min(noaa_df.TMAX) / 10, 1)
    bin_size = temperature_range_max // 15 + 1
    bin_size = round(bin_size / 10, 1)
    bin_list = []
    for i in range(15):
        temperature_bound += bin_size
        bin_list.append(round(temperature_bound, 1))
    bin_list.append("NA")
    return bin_list


def add_month_to_image_v2(
    temperature_df: pd.DataFrame,
    drawobject: ImageDraw.ImageDraw,
    month_number: int = 1,
):
    """Adds a month of data to the quilt Image
    Args:
        temperature_df: (pd.dataFrame)
        drawobject (PIL.ImageDraw.ImageDraw): _description_
        month_number (int, optional): _description_. Defaults to 1.
    """
    for i in range(31):
        x_1 = month_number * 20
        x_2 = x_1 + 10
        y_1 = 30 + i * 10
        y_2 = y_1 + 10
        level = temperature_df.iloc[i, month_number - 1]
        if level < 0 or level > 15:
            raise KeyError(f"{level}")
        color_tuple = make_color_kona(level)
        if level is None:
            raise KeyError("No Level")
            level = 1
        drawobject.rectangle([x_1, y_1, x_2, y_2], fill=color_tuple, outline=1)


def construct_image_v2(temperature_data: pd.DataFrame) -> Image:
    """Construct the image from the weather_data

    Args:
        temperature_data (pd.DataFrame): temperature level data
        from create_temp_level_df

    Returns:
        Image: data quilt image
    """
    local_image = Image.new(mode="RGB", size=(270, 370), color=(256, 256, 256))
    draw = ImageDraw.Draw(local_image)
    draw.line([0, 30, 270, 30], fill=1, width=1)
    draw.line([0, 340, 270, 340], fill=1, width=1)
    for i in range(12):
        add_month_to_image_v2(temperature_data, draw, i + 1)
    return local_image


def the_main():
    """Creates the weather dictionary and then uses add_month_to_image to
    draw an image of the quilt.
    """
    level_df = create_temp_level_df(MYDATA)
    local_image = construct_image_v2(level_df)
    local_image.show()


if __name__ == "__main__":
    the_main()
