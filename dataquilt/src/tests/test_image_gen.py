from dataquilt.image_generator import (
    MYDATA,
    the_main,
    create_piece_counter,
    create_bin_list,
    create_temp_level_df,
)

# import pytest


def test_main_function():

    the_main()


def test_create_temp_level_df():
    """Test creation of a 31 x 12 data frame"""
    local_df = create_temp_level_df(MYDATA)
    assert local_df.shape == (31, 12)


def test_create_counter():
    """Test piece counter dataframe"""
    level_df = create_temp_level_df(MYDATA)
    binlist = create_bin_list(MYDATA)
    local_df = create_piece_counter(level_df, binlist)
    assert list(local_df.columns) == [
        "code",
        "color",
        "count",
        "Celsius",
        "Fahrenheit",
    ]
