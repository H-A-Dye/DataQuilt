import streamlit as st
import pandas as pd

import dataquilt.weather_station_inv as dw


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
