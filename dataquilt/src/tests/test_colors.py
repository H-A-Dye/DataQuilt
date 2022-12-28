import pytest
from PIL import Image, ImageDraw
from dataquilt.colors_kona import (
    ColorInformation,
    RGBColor,
    color_conversion_rgb,
    make_kona_dictionary,
    make_color_kona,
)


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
    test_color = str(
        ColorInformation(
            "Peri",
            "RGBColor(R=62, G=41, B=241)",
            "1",
        )
    )
    assert str(color_dictionary.get(1)) == test_color


def test_color_span():
    """tests the color generation"""
    local_image = Image.new(mode="RGB", size=(200, 200), color=(256, 256, 256))
    draw = ImageDraw.Draw(local_image)
    for i in range(15):
        color = make_color_kona(i)
        draw.rectangle([i * 10, 10, i * 10 + 10, 30], fill=color, outline=1)
    local_image.show()
