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

# TODO: DF_KONA[DF_KONA.name.str.contains("Cel")]


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
    red = round(255 * (1 - C) * (1 - K), 0)
    green = round(255 * (1 - M) * (1 - K), 0)
    blue = round(255 * (1 - Y) * (1 - K), 0)
    return RGBColor(red, green, blue)


class Color_Information:
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
    color_dict = dict()
    for x in list(colorlist.keys()):
        color_name = colorlist.get(x)
        local_row = DF_KONA[DF_KONA.name.str.contains(color_name)]
        cmyk = local_row.iloc[0][3]
        rgb = color_conversion_rgb(cmyk)
        kona_info = Color_Information(color_name, rgb, x)
        color_dict.update({x: kona_info})


def make_color_kona(level: int) -> RGBColor:
    """_summary_

    Args:
        level (int): _description_

    Returns:
        RGBColor: _description_
    """
    pass
