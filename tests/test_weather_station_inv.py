from dataquilt.weather_station_inv import (
    the_main_function,
    load_weatherstation_inventory,
    zip2latlong,
)
import pytest

from pytest import approx


@pytest.mark.skip(
    "Data files need to be added"
)  # https://github.com/H-A-Dye/DataQuilt/issues/26
def test_the_main_function():

    the_main_function()


@pytest.mark.skip(
    "Data files need to be added"
)  # https://github.com/H-A-Dye/DataQuilt/issues/26
def test_load_weatherstation_inventory():

    my_list = load_weatherstation_inventory()

    assert type(my_list) == list


def test_zip2latlong():
    assert zip2latlong("62269") == approx((38.59, -89.92), 0.01)
