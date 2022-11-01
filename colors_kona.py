import swatch
from collections import namedtuple
import pandas as pd

RGBColor = namedtuple('RGBColor', ['R','G','B'])
COLORLIST = {"Celestial": 233, "Turquoise": 1376, "Jamaica":491,
"Azure":1009, "Kiwi":1188, "Lime": 1192, "Cactus":199,
"Buttercup": 1056, "Canary":26, "Creamsicle": 185, "Watermelon":
1384, "Pomegranate": 1295, "Honeysuckle": 490,  "Cerise": 1066, "Berry":1016}

MYKONA = swatch.parse("kona365.ase")
DF_KONA = pd.json_normalize(MYKONA,record_path = ['swatches'])


def color_conversion_rgb(cmyk: list)->RGBColor:
    """Convert a CMYK color into RGB

    Args:
        cmyk (list): CMYK Color

    Returns:
        RGBColor: RGB Color
    """
    C=float(cmyk[0])
    M=float(cmyk[1])
    Y=float(cmyk[2])
    K=float(cmyk[3])
    red = round(255 *(1-C)*(1-K),0)
    green = round(255*(1-M)*(1-K),0)
    blue = round(255*(1-Y)*(1-K),0)
    return RGBColor(red, green, blue)


class Color_Information:

    def __init__(self, name: str, rgbinfo: RGBColor, bin_no: int):
        self.name = name
        self.rgbinfo = rgbinfo
        self.bin = bin_no

    def __str__(self):
        return f"{self.name}({self.rgbinfo},{self.bin_no})"
    
    def __repr__(self):
        return f"{type(self).__name__}('{self.name}','{self.rgbinfo}','{self.bin}')"