import pytest

from colors_kona import (ColorInformation, RGBColor, color_conversion_rgb,
                         make_kona_dictionary)


def test_color_conversion():
    assert type(color_conversion_rgb([1, 0, 0, 0])) == RGBColor


@pytest.mark.parametrize(
    "cmyk, expected",
    [
        ([0, 1, 0, 0], RGBColor(255, 0, 255)),
        ([0, 1, 1, 0], RGBColor(255, 0, 0)),
        ([0, 0, 0, 1], RGBColor(0, 0, 0)),
        ([1, 1, 0, 0], RGBColor(0, 0, 255)),
    ],
)
def test_color_conversion_mass(cmyk, expected):
    assert color_conversion_rgb(cmyk) == expected


@pytest.fixture
def color_information():
    return ColorInformation("Lilac", RGBColor(255, 0, 255), 14)


def test_color_information(color_information):
    assert isinstance(color_information, ColorInformation)


def test_string_rep(color_information):
    assert str(color_information) == "Lilac(RGBColor(R=255, G=0, B=255),14)"


@pytest.fixture
def color_dictionary():
    return make_kona_dictionary()


def test_dictionary_type(color_dictionary):
    assert isinstance(color_dictionary, dict)


def test_dictionary_entry(color_dictionary):
    assert color_dictionary.get(1) == "ColorInformation('Turquoise','RGBColor(R=58, G=193, B=225)','1') "
    
