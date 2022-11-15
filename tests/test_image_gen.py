import pytest
from image_generator import (
    MYDATA,
    DayData,
    TempData,
    the_main,
    extract_data,
    create_weather_dict,
)


def test_main_function():

    the_main()


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
