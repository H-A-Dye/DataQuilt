from dataquilt.image_generator import (
    MYDATA,
    DayData,
    TempData,
    the_main,
    extract_data,
    create_month_list,
    create_weather_dict,
    create_level_dataframe,
    create_piece_counter,
    create_temp_level_df,
)
import pytest


def test_main_function():

    the_main()


def test_create_temp_level_df():
    """Test creation of a 31 x 12 data frame"""
    local_df = create_temp_level_df(MYDATA)
    assert local_df.shape == (31, 12)


def test_extract_data():
    """Test data extraction."""
    row0 = MYDATA.iloc[0]
    days, temps = extract_data(row0)
    assert type(days) == DayData
    assert type(temps) == TempData


def test_create_dict(df=MYDATA):
    """Test that a dictionary of correct length is produced."""
    the_result = create_weather_dict(df)
    assert len(the_result) == 365 or len(the_result) == 366
    assert type(the_result) == dict


@pytest.mark.parametrize("test_input,expected", [(1, 31), (2, 31), (4, 31)])
def test_create_month_list(
    test_input,
    expected,
    df=MYDATA,
):
    """Test that lists are correct length"""
    weather_dict = create_weather_dict(df)
    local_list = create_month_list(df, weather_dict, test_input)
    assert len(local_list) == expected


def test_create_level_df():
    """Test for correct shape of df"""
    local_df = create_level_dataframe(MYDATA)
    assert local_df.shape == (31, 12)


def test_create_counter():
    """Test piece counter dataframe"""
    level_df = create_level_dataframe(MYDATA)
    local_df = create_piece_counter(level_df)
    assert list(local_df.columns) == ["Count", "code", "color"]
