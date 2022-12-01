import streamlit as st

# from . import weather_station_inv

st.set_page_config(
    page_title="Temperature Quilt",
    page_icon="\U0001F334",
    initial_sidebar_state="expanded",
)


st.title("Temperature Quilt")
st.markdown(
    """##### <span style="color:gray">
    Construct a temperature quilt for a US zip code</span>
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

zip_code = st.text_input("Enter a US zipcode", value="60660", max_chars=5)
