from ctypes.wintypes import RGB
import pytest
from colors_kona import *



row0=DF_KONA.iloc[0]
row1=DF_KONA.iloc[1]

def test_color_conversion():
    assert type(color_conversion_rgb([1,0,0,0]))==RGBColor


def test_color_conversion_red():
    assert color_conversion_rgb([0,1,1,0])==RGBColor(255,0,0)

def test_color_conversion_magenta():
    assert color_conversion_rgb([0,1,0,0])==RGBColor(255,0,255)

# TODO: Use table https://www.rapidtables.com/convert/color/cmyk-to-rgb.html    
@pytest.mark.parametrize('cmyk, expected',[([0,0,0,1], RGBColor(0,0,0)), 
                                        ([1,1,0,0],RGBColor(0,0,255))])
def test_color_conversion_mass(cmyk, expected):
    assert color_conversion_rgb(cmyk)==expected
