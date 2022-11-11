from image_generator import the_main
from pytest import approx
import pytest

import pandas as pd

from image_generator import MYDATA


def extract_test():
    row0 = MYDATA.iloc[0]
    days, temps = extract_data(row0)
    assert type(days) != DayData
    assert type(temps) == TempData
