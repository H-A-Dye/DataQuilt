import streamlit as st
import pandas as pd
from collections import namedtuple


import dataquilt.weather_station_inv as dw
import dataquilt.data_from_api as da
import dataquilt.image_generator as ig

from pdf_borb import borb_pattern

# python -m pip install -e .\dataquilt


DayData = namedtuple("DayData", "month,day")
TempData = namedtuple("TempData", "low_temperature,high_temperature")


st.set_page_config(
    page_title="Temperature Quilt",
    page_icon="\U0001F334",
    initial_sidebar_state="expanded",
)


st.title("Temperature Quilt")
st.markdown(
    """##### Construct a temperature quilt for a US zip code
            """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.sidebar.columns([1, 8, 1])
with col1:
    st.write("")
with col2:
    st.write("Place Holder for image")
with col3:
    st.write("")

st.sidebar.markdown(" ## Temperature Quilts")
st.sidebar.markdown("This makes a visual model of a year of temperatures")
st.sidebar.info("Read more about quilting", icon="ℹ️")

zip_code = st.text_input("Enter a US zipcode", value="62269", max_chars=5)
invlist = dw.load_weatherstation_inventory()
inv_df = pd.DataFrame(invlist)
inv_df = dw.sort_years_weatherstat(inv_df)
try:
    loc_lat, loc_long = dw.zip2latlong(zip_code)
except ValueError:
    st.write("Not a valid zip code")


inv_df = dw.attach_distances_to_inventory(loc_lat, loc_long, inv_df)
shortlist = dw.sort_get_min_dist_weatherstat(inv_df)

st.write("Top Ten Nearest Weather Stations")
st.dataframe(data=shortlist)

myweatherstations = da.create_weatherdata_dictionary(shortlist)
missingdates = da.id_missing_data_dict(myweatherstations)
output = da.check_for_complete_stations(missingdates)

st.write(output)
stationselect, num_dates_missing = output

if num_dates_missing > 0:
    raise ValueError("Missing Dates")
weather_data_df = myweatherstations.get(stationselect)

st.dataframe(data=weather_data_df)

local_im = ig.image_construct(weather_data_df)


st.image(local_im)

local_im.save("localpic.jpg")

level_df = ig.create_level_dataframe(weather_data_df)

st.dataframe(level_df)

piece_df = ig.create_piece_counter(level_df)


st.dataframe(piece_df)

borb_pattern(piece_df, level_df)
