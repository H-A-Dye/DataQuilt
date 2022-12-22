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
    """##### Construct a temperature quilt for a US zip code and year
            """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.sidebar.columns([1, 8, 1])
with col1:
    st.write("")
with col2:
    st.image("localpic.jpg")
with col3:
    st.write("")

st.sidebar.markdown(" ## Temperature Quilts")


prog_intro = (
    "This program makes a model of a year of "
    "maximum daily temperatures. The data is "
    "obtained from NOAA based on zip code and year."
)

st.sidebar.write(prog_intro)


st.sidebar.info(
    "More about quilting at [www.heatheranndye.com](www.heatheranndye.com)",
    icon="ℹ️",
)

zip_code = st.text_input("Enter a US zipcode", value="62269", max_chars=5)
year = st.number_input("Enter a previous year", value=2021, max_value=2021)
invlist = dw.load_weatherstation_inventory()
inv_df = pd.DataFrame(invlist)
inv_df = dw.sort_years_weatherstat(inv_df, year)
try:
    loc_lat, loc_long = dw.zip2latlong(zip_code)
except ValueError:
    st.write("Not a valid zip code")


center_heading_text = """
    <style>
        .col_heading   {text-align: center !important}
    </style>          """

center_row_text = """
    <style>
        td  {text-align: center !important}
    </style>      """

# Inject CSS with Markdown

st.markdown(center_heading_text, unsafe_allow_html=True)
st.markdown(center_row_text, unsafe_allow_html=True)

inv_df = dw.attach_distances_to_inventory(loc_lat, loc_long, inv_df)
shortlist = dw.sort_get_min_dist_weatherstat(inv_df)
st.write("### Ten Nearest Weather Stations to Zip Code")

st.dataframe(data=shortlist)

output = da.find_complete_data(shortlist, str(year))


weather_data_df, num_dates_missing = output

if num_dates_missing > 0:
    st.write("Missing Dates")

station_name = weather_data_df.STATION[0]

st.markdown("#### Data from station:")
st.write(station_name)
explain_nums = "To convert the data to Celsius, divide the data by 10."

st.write(explain_nums)
st.dataframe(data=weather_data_df)

level_df = ig.create_temp_level_df(weather_data_df)


local_image = ig.construct_image_v2(level_df)

st.write("### Sample Quilt Image")
st.image(local_image)

local_image.save("localpic.jpg")

st.write("### Color codes for fabric squares")


st.dataframe(level_df)
st.write("### Total squares by color")
bins_string = (
    "This gives information about the "
    "number of pieces in each temperature range. "
    "The last two columns give "
    "the maximum temperature for a color."
)
st.write(bins_string)
bins = ig.create_bin_list(weather_data_df)
piece_df = ig.create_piece_counter(level_df, bins)

st.dataframe(piece_df)

borb_pattern(local_image, piece_df, level_df)

the_data = open("output.pdf", "rb")

st.download_button(
    "Download PDF",
    data=the_data,
    file_name="pdf_test.pdf",
    mime="application/pdf",
)
