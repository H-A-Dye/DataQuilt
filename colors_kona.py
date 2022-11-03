    """ Creates a dictionary of Kona Cotton Colors and
    Establishes a color_info class
    """
import swatch
from collections import namedtuple
import pandas as pd

RGBColor = namedtuple("RGBColor", ["R", "G", "B"])

COLORLIST = {
    "Celestial": 233,
    "Turquoise": 1376,
    "Jamaica": 491,
    "Azure": 1009,
    "Kiwi": 1188,
    "Lime": 1192,
    "Cactus": 199,
    "Buttercup": 1056,
    "Canary": 26,
    "Creamsicle": 185,
    "Watermelon": 1384,
    "Pomegranate": 1295,
    "Honeysuckle": 490,
    "Cerise": 1066,
    "Berry": 1016,
}
COLORENNUMERATE = {
    0: "Celestial",
    1: "Turquoise",
    2: "Jamaica",
    3: "Azure",
    4: "Kiwi",
    5: "Lime",
    6: "Cactus",
    7: "Buttercup",
    8: "Canary",
    9: "Creamsicle",
    10: "Watermelon",
    11: "Pomegranate",
    12: "Honeysuckle",
    13: "Cerise",
    14: "Berry",
}

MYKONA = swatch.parse("kona365.ase")
DF_KONA = pd.json_normalize(MYKONA, record_path=["swatches"])




def color_conversion_rgb(cmyk: list) -> RGBColor:
    """Convert a CMYK color into RGB

    Args:
        cmyk (list): CMYK Color

    Returns:
        RGBColor: RGB Color
    """
    C = float(cmyk[0])
    M = float(cmyk[1])
    Y = float(cmyk[2])
    K = float(cmyk[3])
    red = int( round(255 * (1 - C) * (1 - K), 0))
    green = int( round(255 * (1 - M) * (1 - K), 0))
    blue = int(round(255 * (1 - Y) * (1 - K), 0))
    return RGBColor(red, green, blue)


class ColorInformation:
    """Color Information: Kona Color name, RGBColor, Bin_no for scaling
    Returns:
        _type_: _description_
    """

    def __init__(self, name: str, rgbinfo: RGBColor, bin_no: int):
        self.name = name
        self.rgbinfo = rgbinfo
        self.bin = bin_no

    def __str__(self):
        return f"{self.name}({self.rgbinfo},{self.bin})"

    def __repr__(self):
        return f"{type(self).__name__}('{self.name}','{self.rgbinfo}','{self.bin}')"


def make_kona_dictionary(colorlist: dict = COLORENNUMERATE) -> dict:
    """Takes a dictionary of Kona color names and number keys and returns a
    dictionary with number key and Color_Information for Pillow.

    Args:
        colorlist (dict, optional): Kona color list and keys. Defaults to COLORENNUMERATE.
    """
    color_dict = {}
    for i in list(colorlist.keys()):
        color_name = colorlist.get(i)
        local_row = DF_KONA[DF_KONA.name.str.contains(color_name)]
        cmyk = local_row.iloc[0][3]
        rgb = color_conversion_rgb(cmyk)
        kona_info = ColorInformation(color_name, rgb, i)
        color_dict.update({i: kona_info})
    return color_dict


KONA_DICT = make_kona_dictionary()


def make_color_kona(level: int) -> tuple:
    """Return a tuple from color level

    Args:
        level (int): color elver

    Returns:
        tuple: 3 tuple for Pillow
    """
    color_info = KONA_DICT.get(level)
    rgb = color_info.rgbinfo
    color_tuple = (rgb.R, rgb.G, rgb.B)
    return color_tuple
