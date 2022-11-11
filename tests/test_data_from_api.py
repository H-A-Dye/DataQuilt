from data_from_api import the_main_function, get_temps_weatherstation
import pytest
import pandas as pd
import pandas._testing as pdt


def test_the_main_function():

    the_main_function()


@pytest.mark.parametrize(
    "theyear, station, df_expected",
    [
        (
            "2021",
            "USW00003960",
            pd.read_csv("USW00003960.csv"),  # TODO: fill in the expected data frame
        )
    ],
)
def test_get_temps_weatherstation(theyear, station, df_expected):

    df = get_temps_weatherstation(theyear=theyear, station=station)

    assert pdt.assert_frame_equal(df, df_expected)
