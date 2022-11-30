from dataquilt.data_from_api import the_main_function, get_temps_weatherstation
import pytest
import pandas as pd

# import pandas._testing as pdt
from dataquilt import DATA_PATH


@pytest.mark.skip(
    "Data files need to be added"
)  # https://github.com/H-A-Dye/DataQuilt/issues/26
def test_the_main_function():

    the_main_function()


@pytest.mark.parametrize(
    "theyear, station, df_expected",
    [
        (
            "2021",
            "USW00003960",
            pd.read_csv(DATA_PATH / "USW00003960.csv", index_col=0),
        )
    ],
)
def test_get_temps_weatherstation(theyear, station, df_expected):
    """Test the get_temps_weather station against stored csv."""
    _ = get_temps_weatherstation(theyear=theyear, station=station)

    # assert pdt.assert_frame_equal(df, df_expected)
