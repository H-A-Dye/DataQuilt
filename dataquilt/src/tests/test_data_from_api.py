from dataquilt.data_from_api import the_main_function, identify_missing_data
import pytest
import pandas as pd

# import pandas._testing as pdt
from dataquilt import DATA_PATH


def test_the_main_function():

    the_main_function()


@pytest.mark.parametrize(
    "df_sample, num_missing",
    [
        (
            pd.read_csv(DATA_PATH / "USW00003960.csv", index_col=0),
            0,
        )
    ],
)
def test_id_missing_data(df_sample: pd.DataFrame, num_missing: int):
    """Test missing data identification"""
    local_data = df_sample.TMAX
    local_list = identify_missing_data(local_data)
    assert len(local_list) == 0


def test_find_complete_data():
    """Test the get_temps_weather station against stored csv."""
    pass
    # assert pdt.assert_frame_equal(df, df_expected)
