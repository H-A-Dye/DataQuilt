import pytest
from image_generator import *

def extract_test():
    row0 = MYDATA.iloc[0]
    days, temps = extract_data(row0)
    assert type(days)!=DayData
    assert type(temps)==TempData