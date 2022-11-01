import pytest
from colors_kona import *

row0=DF_KONA.iloc[0]
row1=DF_KONA.iloc[1]

def test_color_conversion():
    assert type(color_conversion_rgb([1,0,0,0]))==RGBColor